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
    }
    '''
    estilos = estilos.replace('18s', f'{PERIODO_LUZ}s')
    estilos = estilos.replace('24s', f'{len(FRASES)*TIEMPO_FRASE}s')
    estilos = estilos.replace('6s', f'{TIEMPO_FRASE}s')
    partes = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-labelledby="titulo descripcion">
<title id="titulo">Owen A. Hurtado | Scientific Computing</title>
<desc id="descripcion">Physics undergraduate exploring computation, numerical methods and astrophysics. The Flamm paraboloid represents an equatorial spatial slice outside a Schwarzschild black hole's event horizon. The surface is stationary, with synchronized decorative lighting.</desc>
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
    for indice, frase in enumerate(FRASES):
        ancho = len(frase)*11.3
        partes.append(f'<clipPath id="texto-{indice}"><rect class="recorte" x="82" y="211" width="{ancho}" height="29" style="--ancho:{ancho}px;--letras:{len(frase)}"/></clipPath>')
    partes.append('''</defs>
<rect width="1200" height="360" rx="16" fill="__fondo__"/>
<rect x="28" y="30" width="632" height="296" rx="12" fill="url(#fondo-identidad)" stroke="__borde_panel__" stroke-opacity=".5"/>
<g clip-path="url(#panel-identidad)"><g class="gradiente-movil"><rect class="luz-compartida" x="-72" y="-30" width="832" height="416" fill="url(#luz-identidad)"/></g></g>
<rect x="1" y="1" width="1198" height="358" rx="15" fill="url(#cuadricula)" stroke="__borde__"/>
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
