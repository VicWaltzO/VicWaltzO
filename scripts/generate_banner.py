"""Genera un banner SVG autónomo; solo requiere Python 3."""

from pathlib import Path
from math import cos, sin, pi, sqrt, atan2, degrees, radians
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
ESCALA_RADIAL = 40.5
ESCALA_VERTICAL = 13.5
CICLO_PARTICULAS = 28
LONGITUD_ESTELA = 36
GROSOR_ESTELA = 1.5
RAPIDEZ_PARTICULAS = 1.3
CENTRO_DESVIO = (915, 358.4)
RADIO_DESVIO = 200
ANCHO_DESVIO = 120
ANGULO_DESVIO = 5
PASOS_DESVIO = 64
COLORES_PARTICULAS = {
    'ambar': '#F5DDA7',
    'melocoton': '#F2B48C',
    'rosa': '#E5B4AC',
    'malva': '#C6ADC8',
    'crema': '#F4E7C7',
}
ALTO_BANNER = 576
DURACION_ROTACION = 30
ESTADOS_ROTACION = 120
PASOS_MERIDIANO = 32
# Once desfases, con huecos de 2–3.5 s, sin cruces simultáneos.
# La secuencia es determinista; no representa aleatoriedad ni simulación física.
# Los extremos quedan fuera de la tarjeta para entrar y salir por sus bordes.
# Duración / 1.3 equivale a un 30% más de velocidad para el recorrido completo.
particulas = [
    {'posicion_inicial': (-48, 302), 'posicion_final': (1248, 205),
     'duracion': 1.15 / RAPIDEZ_PARTICULAS, 'periodo': CICLO_PARTICULAS, 'retraso': .6,
     'color': 'ambar', 'opacidad': .84, 'radio': 3.8, 'estela': 44, 'grosor': 1.5},
    {'posicion_inicial': (1248, 215), 'posicion_final': (-48, 302),
     'duracion': 1.35 / RAPIDEZ_PARTICULAS, 'periodo': CICLO_PARTICULAS, 'retraso': 9.1,
     'color': 'melocoton', 'opacidad': .84, 'radio': 3.8, 'estela': 58, 'grosor': 1.6},
    {'posicion_inicial': (-48, 248), 'posicion_final': (1248, 328),
     'duracion': 1.4 / RAPIDEZ_PARTICULAS, 'periodo': CICLO_PARTICULAS, 'retraso': 4.6,
     'color': 'crema', 'opacidad': .84, 'radio': 3.6, 'estela': 36, 'grosor': 1.4},
    {'posicion_inicial': (1248, 270), 'posicion_final': (-48, 210),
     'duracion': 1.25 / RAPIDEZ_PARTICULAS, 'periodo': CICLO_PARTICULAS, 'retraso': 17.6,
     'color': 'malva', 'opacidad': .84, 'radio': 3.8, 'estela': 64, 'grosor': 1.5},
    {'posicion_inicial': (-48, 599.04), 'posicion_final': (1248, -23.04), 'esquina': True,
     'duracion': 1.5 / RAPIDEZ_PARTICULAS, 'periodo': CICLO_PARTICULAS, 'retraso': 12.6,
     'color': 'rosa', 'opacidad': .84, 'radio': 3.8, 'estela': 48, 'grosor': 1.6},
    {'posicion_inicial': (-48, -23.04), 'posicion_final': (1248, 599.04), 'esquina': True,
     'duracion': 1.5 / RAPIDEZ_PARTICULAS, 'periodo': CICLO_PARTICULAS, 'retraso': 25.1,
     'color': 'melocoton', 'opacidad': .84, 'radio': 3.6, 'estela': 70, 'grosor': 1.4},
    {'posicion_inicial': (1248, 310), 'posicion_final': (-48, 282),
     'duracion': 1.45 / RAPIDEZ_PARTICULAS, 'periodo': CICLO_PARTICULAS, 'retraso': 20.6,
     'color': 'ambar', 'opacidad': .84, 'radio': 3.8, 'estela': 40, 'grosor': 1.6},
    {'posicion_inicial': (1248, 599.04), 'posicion_final': (-48, -23.04), 'esquina': True,
     'duracion': 1.5 / RAPIDEZ_PARTICULAS, 'periodo': CICLO_PARTICULAS, 'retraso': 2.6,
     'color': 'malva', 'opacidad': .84, 'radio': 3.8, 'estela': 56, 'grosor': 1.4},
    {'posicion_inicial': (1248, -23.04), 'posicion_final': (-48, 599.04), 'esquina': True,
     'duracion': 1.5 / RAPIDEZ_PARTICULAS, 'periodo': CICLO_PARTICULAS, 'retraso': 6.8,
     'color': 'rosa', 'opacidad': .84, 'radio': 3.8, 'estela': 42, 'grosor': 1.5},
    {'posicion_inicial': (-48, 438), 'posicion_final': (1248, 285),
     'duracion': 1.5 / RAPIDEZ_PARTICULAS, 'periodo': CICLO_PARTICULAS, 'retraso': 15.1,
     'color': 'crema', 'opacidad': .84, 'radio': 3.6, 'estela': 62, 'grosor': 1.6},
    {'posicion_inicial': (1248, 146), 'posicion_final': (-48, 106),
     'duracion': 1.5 / RAPIDEZ_PARTICULAS, 'periodo': CICLO_PARTICULAS, 'retraso': 22.9,
     'color': 'melocoton', 'opacidad': .84, 'radio': 3.8, 'estela': 52, 'grosor': 1.5},
]
# x, y, ancho, alto. Las diagonales pasan detrás de estas zonas de contenido.
zonas_protegidas = [
    (108, 66, 300, 42),   # Encabezado izquierdo.
    (54, 125, 590, 173),  # Nombre y subtítulo, incluyendo margen tipográfico.
    (58, 317, 582, 96),  # Terminal completo, cursor incluido.
    (58, 454, 452, 46),  # Pie izquierdo.
    (714, 66, 344, 45),  # Encabezado derecho.
    (982, 331, 175, 75), # Etiquetas del horizonte.
    (710, 368, 452, 182), # Ecuaciones, dominio y firma.
]


def crear_punto(radio, angulo):
    """Paraboloide de Flamm en 3D, con r_s=1 y solamente su hoja exterior."""
    return radio * cos(angulo), radio * sin(angulo), 2 * sqrt(radio - 1)


def rotar_punto(punto, angulo):
    """Rotación alrededor del eje z antes de proyectar; conserva r y z."""
    x, y, z = punto
    return x * cos(angulo) - y * sin(angulo), x * sin(angulo) + y * cos(angulo), z


def proyectar_punto(punto):
    x, y, z = punto
    escala_altura = sqrt(ESCALA_RADIAL**2 - ESCALA_VERTICAL**2)
    return 915 + ESCALA_RADIAL * x, 358.4 + ESCALA_VERTICAL * y - escala_altura * z


def proyectar_curvatura(radio, angulo):
    return proyectar_punto(crear_punto(radio, angulo))


def crear_meridiano(angulo):
    puntos = []
    for paso in range(PASOS_MERIDIANO + 1):
        altura = 2 * sqrt(RADIOS[-1] - 1) * paso / PASOS_MERIDIANO
        radio = 1 + altura**2 / 4
        punto = rotar_punto((radio, 0, altura), angulo)
        puntos.append(proyectar_punto(punto))
    return dibujar_ruta(puntos)


def calcular_luz(angulo):
    """Normal de la superficie a r=2.5 frente a una luz direccional fija."""
    normal = rotar_punto((-1, 0, sqrt(1.5)), angulo)
    luz = (-.5, -.35, .79)
    producto = sum(a * b for a, b in zip(normal, luz))
    longitud = sqrt(sum(a * a for a in normal) * sum(a * a for a in luz))
    return .22 + .5 * max(0, producto / longitud)


def crear_estilos_rotacion():
    """Una trayectoria compartida; los 24 meridianos tienen desfases distintos."""
    estilos = [f'.meridiano {{animation:girar-meridiano {DURACION_ROTACION}s linear infinite}}',
               '.meridiano.destacado {stroke:__naranja__;stroke-width:1.3}',
               '@keyframes girar-meridiano {']
    for paso in range(ESTADOS_ROTACION + 1):
        # Reutilizar el primer ángulo garantiza igualdad exacta al cerrar la vuelta.
        angulo = 2 * pi * (paso % ESTADOS_ROTACION) / ESTADOS_ROTACION
        ruta = crear_meridiano(angulo)
        estilos.append(f'{100 * paso / ESTADOS_ROTACION:.6f}% {{d:path("{ruta}");opacity:{calcular_luz(angulo):.6f}}}')
    estilos.append('}')
    return '\n'.join(estilos)


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
    """Posición y tangente calculadas en Python; sin JavaScript en el SVG."""
    estilos = []
    for indice, trayectoria in enumerate(particulas):
        duracion = trayectoria['duracion']
        retraso = trayectoria['retraso']
        periodo = trayectoria['periodo']
        opacidad = trayectoria['opacidad']
        recorrido = crear_recorrido(trayectoria)
        estilos.append(f'.trayectoria-{indice} {{transform-origin:0 0;animation:cruzar-{indice} {periodo}s linear {retraso}s infinite}}')
        estilos.append(f'@keyframes cruzar-{indice} {{')
        for fraccion, x, y, angulo in recorrido:
            porcentaje = 100 * duracion * fraccion / periodo
            opacidad_actual = opacidad * min(1, fraccion / .1, (1 - fraccion) / .1)
            transformacion = f'translate({x:.3f}px,{y:.3f}px) rotate({angulo:.4f}deg)'
            estilos.append(f'{porcentaje:.6f}% {{transform:{transformacion};opacity:{opacidad_actual:.4f}}}')
        estilos.append(f'100% {{transform:{transformacion};opacity:0}}\n}}')
    return '\n'.join(estilos)


def crear_recorrido(trayectoria):
    """Giro artístico cerca de la malla; no integra geodésicas de Schwarzschild."""
    x, y = trayectoria['posicion_inicial']
    final_x, final_y = trayectoria['posicion_final']
    diferencia_x, diferencia_y = final_x - x, final_y - y
    longitud = sqrt(diferencia_x**2 + diferencia_y**2)
    direccion_x, direccion_y = diferencia_x / longitud, diferencia_y / longitud
    angulo_inicial = atan2(diferencia_y, diferencia_x)
    hacia_x, hacia_y = CENTRO_DESVIO[0] - x, CENTRO_DESVIO[1] - y
    cercania = hacia_x * direccion_x + hacia_y * direccion_y
    distancia = hacia_x * -direccion_y + hacia_y * direccion_x
    desvio = 0
    if not trayectoria.get('esquina') and 0 < cercania < longitud:
        signo = 1 if distancia >= 0 else -1
        desvio = signo * radians(ANGULO_DESVIO) * max(0, 1 - abs(distancia) / RADIO_DESVIO)
    if not desvio:
        return [(fraccion, x + diferencia_x * fraccion, y + diferencia_y * fraccion,
                 degrees(angulo_inicial)) for fraccion in (0, .1, .9, 1)]

    def angulo_en(posicion):
        avance = min(1, max(0, (posicion - cercania + ANCHO_DESVIO) / (2 * ANCHO_DESVIO)))
        # La derivada se anula en ambos extremos; no cambia la dirección de golpe.
        giro = avance**2 * (3 - 2 * avance)
        return angulo_inicial + desvio * giro

    recorrido = [(0, x, y, degrees(angulo_inicial))]
    paso = longitud / PASOS_DESVIO
    for indice in range(1, PASOS_DESVIO + 1):
        angulo_medio = angulo_en((indice - .5) * paso)
        x += paso * cos(angulo_medio)
        y += paso * sin(angulo_medio)
        recorrido.append((indice / PASOS_DESVIO, x, y, degrees(angulo_en(indice * paso))))
    return recorrido


def dibujar_particula(trayectoria):
    """Punto y estela locales; la transformación coloca y mueve el grupo."""
    estela = trayectoria.get('estela', LONGITUD_ESTELA)
    grosor = trayectoria.get('grosor', GROSOR_ESTELA)
    color = COLORES_PARTICULAS[trayectoria['color']]
    radio = trayectoria['radio']
    # La rotación de cada estado alinea esta estela con la tangente del recorrido.
    return f'''<path d="M{-estela:.2f} 0L0 0" fill="none" stroke="{color}" stroke-width="{grosor}" stroke-opacity=".6" stroke-linecap="round"/>
<circle r="{radio}" fill="{color}"/>'''


def generar_particulas():
    """Cuatro cruces entre esquinas y siete con ángulos moderados, todos protegidos."""
    partes = ['<g id="particulas" aria-hidden="true" clip-path="url(#borde-particulas)">']
    for indice, trayectoria in enumerate(particulas):
        partes.append('<g class="diagonal-protegida" mask="url(#proteccion-particulas)">')
        partes.append(f'<g class="trayectoria trayectoria-{indice}" opacity="0">')
        partes.append(dibujar_particula(trayectoria))
        partes.append('</g>')
        partes.append('</g>')
    partes.append('</g>')
    return '\n'.join(partes)


def generar_proteccion_particulas():
    """Máscara fija sobre texto; no transforma ni acorta los recorridos."""
    partes = ['''<clipPath id="borde-particulas"><rect x="2" y="2" width="1196" height="572" rx="14"/></clipPath>
<mask id="proteccion-particulas" maskUnits="userSpaceOnUse" maskContentUnits="userSpaceOnUse" x="0" y="0" width="1200" height="576">
<rect width="1200" height="576" fill="white"/>''']
    for x, y, ancho, alto in zonas_protegidas:
        partes.append(f'<rect x="{x}" y="{y}" width="{ancho}" height="{alto}" fill="black"/>')
    partes.append('</mask>')
    return '\n'.join(partes)


def generar_malla():
    """La malla rota en 3D; los anillos y el horizonte conservan su silueta."""
    partes = ['<g fill="none" stroke-linejoin="round">']
    for indice in range(24):
        angulo = 2 * pi * indice / 24
        ruta = crear_meridiano(angulo)
        retraso = -DURACION_ROTACION * indice / 24
        clase = 'meridiano destacado' if indice == 0 else 'meridiano'
        partes.append(f'<path class="{clase}" d="{ruta}" stroke="__escarlata__" opacity="{calcular_luz(angulo):.6f}" stroke-width=".8" style="animation-delay:{retraso}s"/>')
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
    partes.append('''<ellipse cx="915" cy="358.4" rx="40.5" ry="13.5" fill="__horizonte__" stroke="__naranja__" stroke-width="1.2"/>
<ellipse class="luz-compartida" cx="915" cy="358.4" rx="40.5" ry="13.5" fill="none" stroke="__amarillo__" stroke-width="1.4"/>
<path d="M955.5 358.4H978" stroke="__secundario__" stroke-opacity=".7"/>
<circle cx="955.5" cy="358.4" r="1.8" fill="__naranja__"/>
<text x="990" y="365" class="mono secundario detalle">EVENT HORIZON</text>''')
    partes.append('<text x="990" y="394" class="secundario detalle">r = rₛ</text>')
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
      .meridiano,.luz-compartida,.gradiente-movil,.frase,.recorte,.cursor,.avance {animation:none!important}
      .frase {opacity:0!important}
      .primero {opacity:1!important}
      .recorte {width:var(--ancho)}
      .avance {transform:translateX(var(--ancho))}
      .trayectoria {animation:none!important}
      .trayectoria {opacity:0!important}
    }
    '''
    estilos = estilos.replace('18s', f'{PERIODO_LUZ}s')
    estilos = estilos.replace('24s', f'{len(FRASES)*TIEMPO_FRASE}s')
    estilos = estilos.replace('6s', f'{TIEMPO_FRASE}s')
    estilos += crear_estilos_rotacion()
    estilos += crear_estilos_particulas()
    partes = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{ALTO_BANNER}" viewBox="0 0 1200 {ALTO_BANNER}" role="img" aria-labelledby="titulo descripcion">
<title id="titulo">Owen A. Hurtado | Scientific Computing</title>
<desc id="descripcion">Physics undergraduate exploring computation, numerical methods and astrophysics. The Flamm paraboloid represents an equatorial spatial slice outside a Schwarzschild black hole's event horizon. The meridians show a 30-second axial rotation of the 3D visualization, with directional lighting; this does not represent a rotating black hole. The equations and circular sections remain fixed. Occasional particle trails include four corner crossings and seven varied angles. Near the black hole, a subtle artistic deflection evokes gravitational lensing rather than a physical simulation; their timing is deterministic.</desc>
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
<clipPath id="panel-identidad"><rect x="28" y="48" width="632" height="474" rx="12"/></clipPath>
<pattern id="cuadricula" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="__secundario__" stroke-opacity=".055"/></pattern>''']
    partes.append(generar_proteccion_particulas())
    for indice, frase in enumerate(FRASES):
        ancho = len(frase)*11.3
        partes.append(f'<clipPath id="texto-{indice}"><rect class="recorte" x="82" y="351" width="{ancho}" height="29" style="--ancho:{ancho}px;--letras:{len(frase)}"/></clipPath>')
    partes.append('''</defs>
<rect width="1200" height="576" rx="16" fill="__fondo__"/>
<rect x="28" y="48" width="632" height="474" rx="12" fill="url(#fondo-identidad)" stroke="__borde_panel__" stroke-opacity=".5"/>
<g clip-path="url(#panel-identidad)"><g class="gradiente-movil"><rect class="luz-compartida" x="-72" y="-30" width="832" height="650" fill="url(#luz-identidad)"/></g></g>
<rect x="1" y="1" width="1198" height="574" rx="15" fill="url(#cuadricula)" stroke="__borde__"/>
''')
    partes.append(generar_particulas())
    partes.append('''
<path d="M64 90H102" stroke="__naranja__" stroke-width="2"/>
<text x="114" y="96" class="mono secundario" font-size="11" letter-spacing="2">COMPUTATION / PHYSICS</text>
<text x="64" y="216" font-size="49" font-weight="600" letter-spacing="-1.5">Owen A. Hurtado</text>
<text x="66" y="275" class="secundario" font-size="21">Physics Undergraduate · Scientific Computing</text>
<rect x="64" y="323" width="570" height="82" rx="6" fill="__terminal__" stroke="__borde_terminal__"/>
''')
    for indice, frase in enumerate(FRASES):
        ancho = len(frase)*11.3
        clase = ' primero' if indice == 0 else ''
        demora = (len(FRASES)-indice) * TIEMPO_FRASE
        partes.append(f'<g class="frase{clase}" style="animation-delay:-{demora}s"><g clip-path="url(#texto-{indice})"><text x="82" y="373" class="mono" font-size="18.5" textLength="{ancho}" lengthAdjust="spacingAndGlyphs">{escape(frase)}</text></g><g class="avance" style="--ancho:{ancho}px;--letras:{len(frase)}"><path class="cursor" d="M85 359v17" stroke="__amarillo__" stroke-width="2"/></g></g>')
    partes.append('''<text x="66" y="485" class="mono secundario" font-size="12" letter-spacing="1">OBSERVATION → MODEL → UNDERSTANDING</text>
<path d="M686 86V490" stroke="__borde_terminal__"/>
<text x="722" y="96" class="mono secundario etiqueta" letter-spacing="1">01 / BLACK HOLE GRAVITY</text>''')
    partes.append(generar_malla())
    # Composición matemática nativa: fracción y exponentes con posiciones explícitas.
    # No requiere LaTeX, HTML ni un motor externo al abrirse como imagen en GitHub.
    partes.append('''<g transform="translate(0 164)" role="img" aria-label="Schwarzschild radius r sub s equals two G M over c squared. Embedding height z squared equals four r sub s times r minus r sub s.">
<text x="722" y="273" font-size="26" style="font-family:'Cambria Math',Cambria,'Times New Roman',serif;font-style:italic">r<tspan dy="5" font-size="16">s</tspan><tspan dy="-5" font-size="26"> =</tspan></text>
<text x="792" y="257" font-size="23" style="font-family:'Cambria Math',Cambria,'Times New Roman',serif">2<tspan font-style="italic">GM</tspan></text>
<path d="M787 263H848" stroke="__texto__" stroke-width="1"/>
<text x="810" y="285" font-size="23" style="font-family:'Cambria Math',Cambria,'Times New Roman',serif;font-style:italic">c<tspan dy="-8" font-size="14">2</tspan></text>
<text x="890" y="273" font-size="25" style="font-family:'Cambria Math',Cambria,'Times New Roman',serif;font-style:italic">z<tspan dy="-8" font-size="14">2</tspan><tspan dy="8" font-size="25"> = 4r</tspan><tspan dy="5" font-size="15">s</tspan><tspan dy="-5" font-size="25">(r − r</tspan><tspan dy="5" font-size="15">s</tspan><tspan dy="-5" font-size="25">)</tspan></text>
</g>
<text x="722" y="494" class="mono secundario detalle">SCHWARZSCHILD · SPATIAL EMBEDDING</text>
<text x="722" y="531" class="secundario detalle">r ≥ rₛ · Equatorial slice</text>
<text x="1136" y="526" text-anchor="end" class="secundario firma">Вперёд!</text>
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
