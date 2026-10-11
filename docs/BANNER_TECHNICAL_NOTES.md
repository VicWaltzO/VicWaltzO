# Banner INFERNO

Implementación para Owen A. Hurtado en el repositorio especial `VicWaltzO/VicWaltzO`.
La versión 1.2 refina el banner y reemplaza el saludo genérico del README con una
presentación y proyectos verificados, con autorización expresa del titular.

## Regeneración

Desde la raíz: `python scripts/generate_banner.py`. Requiere Python 3, sin paquetes
adicionales. FRASES, PALETA, RADIOS y los tamaños de etiquetas están al principio
del generador. PERIODO_LUZ cambia conjuntamente el degradado y la iluminación
de la malla. TIEMPO_FRASE controla cada frase; el ciclo completo dura cuatro
veces ese valor. ESCALA_RADIAL y ESCALA_VERTICAL controlan la cámara.
La lista `particulas` configura las posiciones, duración del cruce, periodo,
retraso, color, opacidad y radio de cada trayectoria.

## Campo gravitacional

La visualización representa un corte ecuatorial espacial del exterior de un
agujero negro de Schwarzschild: esférico, sin carga y sin rotación. Se usa el
paraboloide de Flamm, z² = 4r_s(r−r_s), para r ≥ r_s. El radio del horizonte
es r_s = 2GM/c². El cálculo usa r_s=1 y termina en r=4.8r_s. Se proyectan
24 meridianos y nueve anillos con una cámara ortográfica inclinada; cada
meridiano se muestrea uniformemente en z para resolver la pendiente del borde.

Es una representación de curvatura espacial, no una imagen de la sombra, un
disco de acreción o una simulación de radiación. La altura z es una coordenada
de embedding; no representa una dirección física de caída. Se muestra solamente
la hoja exterior, sin añadir una segunda hoja o representar el interior del horizonte.

Referencias del modelo: [radio de Schwarzschild, Einstein Online](https://www.einstein-online.info/en/explandict/schwarzschild-radius/),
[geometría de Schwarzschild, JILA](https://jila.colorado.edu/~ajsh/bh/schwp.html) y
[ecuación del paraboloide, Princeton / Journal of Mathematical Physics](https://cchyba.scholar.princeton.edu/sites/g/files/toruqf3881/files/cchyba/files/chyba_j.math_.phys_.1982_0.pdf).

## Animación y alternativas

La geometría gravitacional permanece fija, como corresponde al modelo estático.
CSS integrado anima la opacidad de la iluminación en un ciclo de 18 segundos,
compartido entre los anillos interiores del campo y el degradado del nombre.
El degradado se desplaza suavemente dentro de un clipPath; sus tonos negro,
escarlata, naranja y amarillo mantienen el contraste del texto. Las animaciones
originales pertenecen a tres familias: terminal, intensidad compartida y
desplazamiento del degradado. La revisión con partículas añade siete
trayectorias independientes, sin cambiar esas tres familias. Se retiraron
previamente las trazas móviles del campo y la pequeña órbita.
La terminal usa recorte escalonado, cuatro intervalos de seis segundos y cursor
móvil; escribe durante 3.6 segundos y mantiene la frase unos 2.1 segundos.
El SVG tiene un estado base con identidad, primera frase y malla visibles.
Se corrigió la especificidad de `.frase.primero` para que la primera frase no
desaparezca cuando el renderizador aplica CSS pero no ejecuta animaciones.

Incluye prefers-reduced-motion. En la prueba con SVG como imagen en Edge no se
aplicó la preferencia emulada; por ello se entrega `assets/banner-static.svg`
sin animaciones como alternativa explícita. Para usarla, cambiar el src del README.
Las PNG de revisión se generan desde esta alternativa estática.

## Partículas inspiradas en neutrinos

Son una interpretación artística, no una simulación de propagación o detección.
Siete puntos de radio 1.8–2.2 px y estelas de 24 px, grosor 0.7 px. Las cuatro
trayectorias iniciales cruzan corredores sin texto; una atraviesa la malla.
Tres diagonales nuevas recorren la tarjeta completa y pasan detrás de máscaras
fijas en las zonas de contenido. No se modifica el recorrido al ocultarse bajo
nombre, terminal o fórmulas. El clip global contiene las estelas en el borde.
Se usan naranja y amarillo pálido, con opacidades de 0.54–0.64; la estela aplica
además una opacidad de 0.4.

Los cruces duran 0.85, 1.1, 1.3 y 1 segundo. Los ciclos duran 47, 61, 73 y 89
segundos, con retrasos iniciales de 3, 16, 30 y 44 segundos. Las diagonales
duran 1.15, 1.3 y 1.05 segundos, en ciclos de 107, 109 y 127 segundos y
retrasos iniciales de 8, 23 y 38 segundos. Los keyframes
interpolan posiciones en línea recta, desvanecen los extremos y mantienen
opacidad cero durante el resto del ciclo. La secuencia es determinista.

Dos trazas muy discretas quedan congeladas en el estado base y la versión
estática. Una animación mínima las oculta cuando funciona la versión animada.
Si el renderizador reconoce `prefers-reduced-motion`, se detienen las
animaciones y vuelven esas dos trazas. Se mantiene la alternativa SVG estática
para los renderizadores que no transmiten la preferencia a una imagen SVG.

## Verificación

XML validado al generar. Banner animado: 49,117 bytes, sin scripts,
foreignObject, fuentes externas ni rasterizados. Vista como img probada en
Microsoft Edge / Chromium 155.0.4283.45. Se revisan PNG a 1200, 800 y 600 px,
y capturas animadas a 2.4 y 8.1 segundos. Se comprueban las cuatro frases en sus
intervalos de lectura, una de cada vez, y la primera frase sin animaciones.
El README se revisa localmente con columnas de escritorio y móvil, en temas claro
y oscuro. Estas capturas aproximan GitHub; no prueban su tema claro real.
Las microetiquetas siguen siendo secundarias y pequeñas en móvil; nombre,
subtítulo, terminal y geometría tienen prioridad. El cirílico aparece una vez.

Las capturas se prepararon con Playwright, Marked y Edge en el entorno local.
Estas herramientas son de revisión; el banner y el generador no dependen de ellas.
La revisión de partículas usa `scripts/preview_particulas.cjs`: comprueba el
recorrido completo contra las cajas tipográficas, desaparición durante las
pausas, estados estáticos y movimiento reducido con SVG integrado. Captura cada
cruce como imagen SVG a 1200 px y uno a 800/600 px. Las diagonales se revisan
en 21 fotogramas frente a una base sin partículas para verificar que no cambian
píxeles en las zonas protegidas; `scripts/check_particle_masks.py` usa Pillow
solo para esa revisión local. El resultado se guarda en
`docs/review/particulas/validacion.json` durante la revisión local. La publicación
del banner, alternativa estática, generador y notas fue autorizada por el titular.
Las capturas y herramientas de revisión permanecen en el espacio de trabajo local.

## Corrección visual

Las ecuaciones usan texto SVG con tipografía matemática de sistema, exponentes
y subíndices con tspan, y una fracción con barra vectorial y posiciones explícitas.
Así conservan la composición matemática en un img sin depender de LaTeX o MathJax.

## Decisiones v1.2

Se comparó la versión anterior con órbita y la versión refinada sin órbita a 600 px.
Se eligió la segunda para dejar aire a las fórmulas y evitar un motivo sin relación
con el corte de Schwarzschild. Las etiquetas pasan de 10–11 a 13–14 px, la firma
de 12 a 15 px y las fórmulas principales de 21–23 a 25–26 px. El gris secundario
se aclara a #C2B6C4. Los anillos exteriores usan púrpura/escarlata; el amarillo
se concentra junto al horizonte. El líder apunta al borde exacto r=r_s.

NutrequinePro se presenta como software administrativo según su README técnico:
https://github.com/VicWaltzO/NutrequinePro/blob/main/app/README.md.
data-analysis-journey se enlaza como diario inicial de aprendizaje según README
y learning-log.md; no se presenta como un análisis científico terminado.
