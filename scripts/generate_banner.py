"""Genera un banner SVG autónomo; solo requiere Python 3."""

from pathlib import Path
from math import cos, sin, pi, sqrt
from html import escape
import xml.etree.ElementTree as ET

RAIZ = Path(__file__).resolve().parents[1]
PALETA = {
    'fondo': '#08070B',
    'horizonte': '#030205',
    'purpura': '#572C4B',
    'escarlata': '#B63632',
    'naranja': '#F3761B',
    'amarillo': '#F6D746',
    'amarillo_palido': '#F6DEA4',
    'texto': '#F2EEE9',
    'secundario': '#C2B6C4',
    'panel_inicio': '#25131B',
    'panel_medio': '#170E16',
    'panel_final': '#100C12',
    'borde_panel': '#49303C',
    'borde': '#302431',
    'terminal': '#17111F',
    'borde_terminal': '#352637',
}
FRASES = [
    '> Exploring the universe through computation',
    '> Computational physics & numerical methods',
    '> Astrophysics · scientific data analysis',
    '> From observations to physical understanding',
]
PERIODO_LUZ = 18
TIEMPO_FRASE = 6
TAMANO_ETIQUETA = 14
TAMANO_DETALLE = 13
TAMANO_FIRMA = 15
RADIOS = [1.04, 1.12, 1.3, 1.6, 2, 2.5, 3.1, 3.9, 4.8]
ESCALA_RADIAL = 30
ESCALA_VERTICAL = 10
# Secuencia determinista: cada cruce es breve y cada trayectoria tiene su propio ciclo.
particulas = [
    {'posicion_inicial': (44, 72), 'posicion_final': (634, 75),
     'duracion': .85, 'periodo': 47, 'retraso': 3,
     'color': 'amarillo_palido', 'opacidad': .62, 'radio': 2},
    {'posicion_inicial': (624, 275), 'posicion_final': (70, 280),
     'duracion': 1.1, 'periodo': 61, 'retraso': 16,
     'color': 'naranja', 'opacidad': .64, 'radio': 2.2},
    {'posicion_inicial': (746, 102), 'posicion_final': (1068, 186),
     'duracion': 1.3, 'periodo': 73, 'retraso': 30,
     'color': 'amarillo_palido', 'opacidad': .58, 'radio': 1.8},
    {'posicion_inicial': (1162, 88), 'posicion_final': (1092, 202),
     'duracion': 1, 'periodo': 89, 'retraso': 44,
     'color': 'naranja', 'opacidad': .62, 'radio': 2},
    {'posicion_inicial': (18, 342), 'posicion_final': (1182, 18),
     'duracion': 1.15, 'periodo': 107, 'retraso': 8,
     'color': 'amarillo_palido', 'opacidad': .56, 'radio': 1.8, 'diagonal': True},
    {'posicion_inicial': (18, 18), 'posicion_final': (1182, 342),
     'duracion': 1.3, 'periodo': 109, 'retraso': 23,
     'color': 'naranja', 'opacidad': .54, 'radio': 2, 'diagonal': True},
    {'posicion_inicial': (1182, 74), 'posicion_final': (18, 306),
     'duracion': 1.05, 'periodo': 127, 'retraso': 38,
     'color': 'amarillo_palido', 'opacidad': .58, 'radio': 1.8, 'diagonal': True},
]
# x, y, ancho, alto. Las diagonales pasan detrás de estas zonas de contenido.
zonas_protegidas = [
    (108, 41, 300, 26),   # Encabezado izquierdo.
    (54, 78, 590, 108),  # Nombre y subtítulo, incluyendo margen tipográfico.
    (58, 198, 582, 60),  # Terminal completo, cursor incluido.
    (58, 284, 452, 29),  # Pie izquierdo.
    (714, 41, 344, 28),  # Encabezado derecho.
    (982, 207, 175, 47), # Etiquetas del horizonte.
    (710, 230, 452, 114), # Ecuaciones, dominio y firma.
]


def proyectar_curvatura(radio, angulo):
    """Corte espacial de Schwarzschild: z²=4r_s(r−r_s), con r_s=1."""
    altura = 2 * sqrt(radio - 1)
    escala_altura = sqrt(ESCALA_RADIAL**2 - ESCALA_VERTICAL**2)
    x = 915 + ESCALA_RADIAL * radio * cos(angulo)
    y = 224 + ESCALA_VERTICAL * radio * sin(angulo) - escala_altura * altura
    return x, y


def dibujar_ruta(puntos):
    return 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in puntos)


def aplicar_colores(contenido):
    for nombre, color in PALETA.items():
        contenido = contenido.replace(f'__{nombre}__', color)
    return contenido


def crear_estilo_base():
    return f'''
    text {{font-family:'Segoe UI',Arial,sans-serif;fill:__texto__}}
    .mono {{font-family:Consolas,'DejaVu Sans Mono',monospace}}
    .secundario {{fill:__secundario__}}
    .etiqueta {{font-size:{TAMANO_ETIQUETA}px}}
    .detalle {{font-size:{TAMANO_DETALLE}px}}
    .firma {{font-size:{TAMANO_FIRMA}px}}
    '''


def crear_estilos_particulas():
    """Un cruce lineal por ciclo; el resto del tiempo el grupo es invisible."""
    estilos = ['''
    .particulas-estaticas {animation:ocultar-particulas .001s steps(1,end) forwards}
    @keyframes ocultar-particulas {0%,100%{opacity:0}}
    ''']
    for indice, trayectoria in enumerate(particulas):
        posicion_inicial = trayectoria['posicion_inicial']
        posicion_final = trayectoria['posicion_final']
        duracion = trayectoria['duracion']
        retraso = trayectoria['retraso']
        periodo = trayectoria['periodo']
        opacidad = trayectoria['opacidad']
        # Los porcentajes acotan la aparición, no la duración total del ciclo.
        aparicion = 100 * duracion * .1 / periodo
        desaparicion = 100 * duracion * .9 / periodo
        final = 100 * duracion / periodo
        inicio = f'translate({posicion_inicial[0]}px,{posicion_inicial[1]}px)'
        destino = f'translate({posicion_final[0]}px,{posicion_final[1]}px)'
        estilos.append(f'''
    .trayectoria-{indice} {{animation:cruzar-{indice} {periodo}s linear {retraso}s infinite}}
    @keyframes cruzar-{indice} {{
      0% {{transform:{inicio};opacity:0}}
      {aparicion:.6f}% {{opacity:{opacidad}}}
      {desaparicion:.6f}% {{opacity:{opacidad}}}
      {final:.6f}% {{transform:{destino};opacity:0}}
      100% {{transform:{destino};opacity:0}}
    }}''')
    return '\n'.join(estilos)


def dibujar_particula(trayectoria):
    """Punto y estela locales; la transformación coloca y mueve el grupo."""
    posicion_inicial = trayectoria['posicion_inicial']
    posicion_final = trayectoria['posicion_final']
    diferencia_x = posicion_final[0] - posicion_inicial[0]
    diferencia_y = posicion_final[1] - posicion_inicial[1]
    longitud = sqrt(diferencia_x**2 + diferencia_y**2)
    cola_x = -24 * diferencia_x / longitud
    cola_y = -24 * diferencia_y / longitud
    color = PALETA[trayectoria['color']]
    radio = trayectoria['radio']
    return f'''<path d="M{cola_x:.2f} {cola_y:.2f}L0 0" fill="none" stroke="{color}" stroke-width=".7" stroke-opacity=".4" stroke-linecap="round"/>
<circle r="{radio}" fill="{color}"/>'''


def generar_particulas():
    """Las diagonales recorren la tarjeta y quedan ocultas detrás del contenido."""
    partes = ['<g id="particulas" aria-hidden="true" clip-path="url(#borde-particulas)">']
    for indice, trayectoria in enumerate(particulas):
        if trayectoria.get('diagonal'):
            partes.append('<g class="diagonal-protegida" mask="url(#proteccion-particulas)">')
        partes.append(f'<g class="trayectoria trayectoria-{indice}" opacity="0">')
        partes.append(dibujar_particula(trayectoria))
        partes.append('</g>')
        if trayectoria.get('diagonal'):
            partes.append('</g>')
    # Base legible cuando las animaciones no se ejecutan: dos trazas congeladas.
    partes.append('<g class="particulas-estaticas" opacity=".32">')
    for indice in (0, 2):
        trayectoria = particulas[indice]
        posicion_inicial = trayectoria['posicion_inicial']
        posicion_final = trayectoria['posicion_final']
        x = (posicion_inicial[0] + posicion_final[0]) / 2
        y = (posicion_inicial[1] + posicion_final[1]) / 2
        partes.append(f'<g transform="translate({x} {y})">')
        partes.append(dibujar_particula(trayectoria))
        partes.append('</g>')
    partes.append('</g></g>')
    return '\n'.join(partes)


def generar_proteccion_particulas():
    """Máscara fija sobre texto; no transforma ni acorta los recorridos."""
    partes = ['''<clipPath id="borde-particulas"><rect x="2" y="2" width="1196" height="356" rx="14"/></clipPath>
<mask id="proteccion-particulas" maskUnits="userSpaceOnUse" maskContentUnits="userSpaceOnUse" x="0" y="0" width="1200" height="360">
<rect width="1200" height="360" fill="white"/>''']
    for x, y, ancho, alto in zonas_protegidas:
        partes.append(f'<rect x="{x}" y="{y}" width="{ancho}" height="{alto}" fill="black"/>')
    partes.append('</mask>')
    return '\n'.join(partes)


def generar_malla():
    """Geometría fija; la luz animada es un recurso visual, no una variación de masa."""
    partes = ['<g fill="none" stroke-linejoin="round">']
    for indice in range(24):
        angulo = 2 * pi * indice / 24
        # Se muestrea z uniformemente para resolver la pendiente junto al horizonte.
        puntos = []
        for paso in range(65):
            altura = 2 * sqrt(RADIOS[-1] - 1) * paso / 64
            radio = 1 + altura**2 / 4
            puntos.append(proyectar_curvatura(radio, angulo))
        ruta = dibujar_ruta(puntos)
        partes.append(f'<path d="{ruta}" stroke="__escarlata__" stroke-opacity=".46" stroke-width=".8"/>')
    anillos = []
    for radio in RADIOS:
        puntos = [proyectar_curvatura(radio, 2*pi*paso/96) for paso in range(97)]
        ruta = dibujar_ruta(puntos) + 'Z'
        anillos.append(ruta)
        if radio < 1.2:
            color = PALETA['amarillo']
        elif radio < 2.5:
            color = PALETA['naranja']
        elif radio < 3.9:
            color = PALETA['escarlata']
        else:
            color = PALETA['purpura']
        partes.append(f'<path d="{ruta}" stroke="{color}" stroke-width="1.1" stroke-opacity=".72"/>')
    # La misma clase sincroniza la iluminación del campo y la del nombre.
    partes.append('<g class="luz-compartida" stroke="__amarillo__" stroke-width="1.15">')
    for indice in (0, 1, 2):
        partes.append(f'<path d="{anillos[indice]}"/>')
    partes.append('</g></g>')
    partes.append('''<ellipse cx="915" cy="224" rx="30" ry="10" fill="__horizonte__" stroke="__naranja__" stroke-width="1.2"/>
<ellipse class="luz-compartida" cx="915" cy="224" rx="30" ry="10" fill="none" stroke="__amarillo__" stroke-width="1.4"/>
<path d="M945 224H978" stroke="__secundario__" stroke-opacity=".7"/>
<circle cx="945" cy="224" r="1.8" fill="__naranja__"/>
<text x="990" y="228" class="mono secundario detalle">EVENT HORIZON</text>''')
    partes.append('<text x="990" y="246" class="secundario detalle">r = rₛ</text>')
    return '\n'.join(partes)


def construir_svg():
    estilos = crear_estilo_base() + '''
    .luz-compartida {opacity:.22;animation:iluminar 18s ease-in-out infinite}
    @keyframes iluminar {0%,100%{opacity:.22}45%{opacity:.52}75%{opacity:.32}}
    .gradiente-movil {animation:desplazar-luz 18s ease-in-out infinite}
    @keyframes desplazar-luz {0%,100%{transform:translate(-100px,35px)}45%{transform:translate(60px,-30px)}75%{transform:translate(-30px,15px)}}
    .frase {opacity:0;animation:frase 24s steps(1,end) infinite}
    .frase.primero {opacity:1}
    @keyframes frase {0%,24.99%{opacity:1}25%,100%{opacity:0}}
    .recorte {animation:escribir 6s steps(var(--letras),end) infinite}
    @keyframes escribir {0%{width:0}60%,95%{width:var(--ancho)}100%{width:0}}
    .cursor {animation:cursor 1.2s steps(1,end) infinite}
    .avance {animation:avance 6s steps(var(--letras),end) infinite}
    @keyframes avance {0%{transform:translateX(0)}60%,95%{transform:translateX(var(--ancho))}100%{transform:translateX(0)}}
    @keyframes cursor {0%,60%{opacity:1}61%,100%{opacity:0}}
    @media (prefers-reduced-motion:reduce) {
      .luz-compartida,.gradiente-movil,.frase,.recorte,.cursor,.avance {animation:none!important}
      .frase {opacity:0!important}
      .primero {opacity:1!important}
      .recorte {width:var(--ancho)}
      .avance {transform:translateX(var(--ancho))}
      .trayectoria,.particulas-estaticas {animation:none!important}
      .trayectoria {opacity:0!important}
      .particulas-estaticas {opacity:.32!important}
    }
    '''
    estilos = estilos.replace('18s', f'{PERIODO_LUZ}s')
    estilos = estilos.replace('24s', f'{len(FRASES)*TIEMPO_FRASE}s')
    estilos = estilos.replace('6s', f'{TIEMPO_FRASE}s')
    estilos += crear_estilos_particulas()
    partes = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-labelledby="titulo descripcion">
<title id="titulo">Owen A. Hurtado | Scientific Computing</title>
<desc id="descripcion">Physics undergraduate exploring computation, numerical methods and astrophysics. The Flamm paraboloid represents an equatorial spatial slice outside a Schwarzschild black hole's event horizon. The surface is stationary, with synchronized decorative lighting. Occasional straight particle trails are an artistic interpretation inspired by neutrinos; their timing is deterministic.</desc>
<style>{estilos}</style>
<defs>
<linearGradient id="fondo-identidad" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="__panel_inicio__"/>
<stop offset=".55" stop-color="__panel_medio__"/>
<stop offset="1" stop-color="__panel_final__"/>
</linearGradient>
<radialGradient id="luz-identidad" cx=".75" cy=".55" r=".7">
<stop offset="0" stop-color="__amarillo__" stop-opacity=".12"/>
<stop offset=".3" stop-color="__naranja__" stop-opacity=".22"/>
<stop offset=".62" stop-color="__escarlata__" stop-opacity=".27"/>
<stop offset="1" stop-color="__escarlata__" stop-opacity="0"/>
</radialGradient>
<clipPath id="panel-identidad"><rect x="28" y="30" width="632" height="296" rx="12"/></clipPath>
<pattern id="cuadricula" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="__secundario__" stroke-opacity=".055"/></pattern>''']
    partes.append(generar_proteccion_particulas())
    for indice, frase in enumerate(FRASES):
        ancho = len(frase)*11.3
        partes.append(f'<clipPath id="texto-{indice}"><rect class="recorte" x="82" y="211" width="{ancho}" height="29" style="--ancho:{ancho}px;--letras:{len(frase)}"/></clipPath>')
    partes.append('''</defs>
<rect width="1200" height="360" rx="16" fill="__fondo__"/>
<rect x="28" y="30" width="632" height="296" rx="12" fill="url(#fondo-identidad)" stroke="__borde_panel__" stroke-opacity=".5"/>
<g clip-path="url(#panel-identidad)"><g class="gradiente-movil"><rect class="luz-compartida" x="-72" y="-30" width="832" height="416" fill="url(#luz-identidad)"/></g></g>
<rect x="1" y="1" width="1198" height="358" rx="15" fill="url(#cuadricula)" stroke="__borde__"/>
''')
    partes.append(generar_particulas())
    partes.append('''
<path d="M64 56H102" stroke="__naranja__" stroke-width="2"/>
<text x="114" y="60" class="mono secundario" font-size="11" letter-spacing="2">COMPUTATION / PHYSICS</text>
<text x="64" y="135" font-size="49" font-weight="600" letter-spacing="-1.5">Owen A. Hurtado</text>
<text x="66" y="172" class="secundario" font-size="21">Physics Undergraduate · Scientific Computing</text>
<rect x="64" y="202" width="570" height="51" rx="6" fill="__terminal__" stroke="__borde_terminal__"/>
''')
    for indice, frase in enumerate(FRASES):
        ancho = len(frase)*11.3
        clase = ' primero' if indice == 0 else ''
        demora = (len(FRASES)-indice) * TIEMPO_FRASE
        partes.append(f'<g class="frase{clase}" style="animation-delay:-{demora}s"><g clip-path="url(#texto-{indice})"><text x="82" y="233" class="mono" font-size="18.5" textLength="{ancho}" lengthAdjust="spacingAndGlyphs">{escape(frase)}</text></g><g class="avance" style="--ancho:{ancho}px;--letras:{len(frase)}"><path class="cursor" d="M85 219v17" stroke="__amarillo__" stroke-width="2"/></g></g>')
    partes.append('''<text x="66" y="303" class="mono secundario" font-size="12" letter-spacing="1">OBSERVATION → MODEL → UNDERSTANDING</text>
<path d="M686 54V306" stroke="__borde_terminal__"/>
<text x="722" y="60" class="mono secundario etiqueta" letter-spacing="1">01 / BLACK HOLE GRAVITY</text>''')
    partes.append(generar_malla())
    # Composición matemática nativa: fracción y exponentes con posiciones explícitas.
    # No requiere LaTeX, HTML ni un motor externo al abrirse como imagen en GitHub.
    partes.append('''<g role="img" aria-label="Schwarzschild radius r sub s equals two G M over c squared. Embedding height z squared equals four r sub s times r minus r sub s.">
<text x="722" y="273" font-size="26" style="font-family:'Cambria Math',Cambria,'Times New Roman',serif;font-style:italic">r<tspan dy="5" font-size="16">s</tspan><tspan dy="-5" font-size="26"> =</tspan></text>
<text x="792" y="257" font-size="23" style="font-family:'Cambria Math',Cambria,'Times New Roman',serif">2<tspan font-style="italic">GM</tspan></text>
<path d="M787 263H848" stroke="__texto__" stroke-width="1"/>
<text x="810" y="285" font-size="23" style="font-family:'Cambria Math',Cambria,'Times New Roman',serif;font-style:italic">c<tspan dy="-8" font-size="14">2</tspan></text>
<text x="890" y="273" font-size="25" style="font-family:'Cambria Math',Cambria,'Times New Roman',serif;font-style:italic">z<tspan dy="-8" font-size="14">2</tspan><tspan dy="8" font-size="25"> = 4r</tspan><tspan dy="5" font-size="15">s</tspan><tspan dy="-5" font-size="25">(r − r</tspan><tspan dy="5" font-size="15">s</tspan><tspan dy="-5" font-size="25">)</tspan></text>
</g>
<text x="722" y="309" class="mono secundario detalle">SCHWARZSCHILD · SPATIAL EMBEDDING</text>
<text x="722" y="332" class="secundario detalle">r ≥ rₛ · Equatorial slice</text>
<text x="1136" y="329" text-anchor="end" class="secundario firma">Вперёд!</text>
</svg>''')
    return aplicar_colores('\n'.join(partes))


def guardar_svg():
    destino = RAIZ / 'assets' / 'banner.svg'
    destino.parent.mkdir(exist_ok=True)
    contenido = construir_svg()
    ET.fromstring(contenido)
    destino.write_text(contenido, encoding='utf-8')
    # Alternativa sin animaciones para renderizadores que no transmiten la preferencia.
    inicio = contenido.index('<style>')
    final = contenido.index('</style>') + len('</style>')
    estilo_estatico = '<style>' + crear_estilo_base() + '''
    .frase {opacity:0}.primero {opacity:1}
    .luz-compartida {opacity:.38}
    .avance {transform:translateX(var(--ancho))}
    </style>'''
    estatico = aplicar_colores(contenido[:inicio] + estilo_estatico + contenido[final:])
    (destino.parent / 'banner-static.svg').write_text(estatico, encoding='utf-8')
    print(f'{destino}: {destino.stat().st_size:,} bytes; XML válido')


if __name__ == '__main__':
    guardar_svg()
