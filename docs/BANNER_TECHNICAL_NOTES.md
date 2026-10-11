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
se limitan a tres familias: terminal, intensidad compartida y desplazamiento del
degradado. Se retiraron las trazas móviles y la pequeña órbita.
La terminal usa recorte escalonado, cuatro intervalos de seis segundos y cursor
móvil; escribe durante 3.6 segundos y mantiene la frase unos 2.1 segundos.
El SVG tiene un estado base con identidad, primera frase y malla visibles.
Se corrigió la especificidad de `.frase.primero` para que la primera frase no
desaparezca cuando el renderizador aplica CSS pero no ejecuta animaciones.

Incluye prefers-reduced-motion. En la prueba con SVG como imagen en Edge no se
aplicó la preferencia emulada; por ello se entrega `assets/banner-static.svg`
sin animaciones como alternativa explícita. Para usarla, cambiar el src del README.
Las PNG de revisión se generan desde esta alternativa estática.

## Verificación

XML validado al generar. Banner animado: aproximadamente 43 KB, sin scripts,
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
