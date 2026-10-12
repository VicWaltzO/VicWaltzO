# Banner INFERNO Scientific Identity

Banner de Owen A. Hurtado para `VicWaltzO/VicWaltzO`: 1200 × 576 px,
un 60% más alto que la revisión de 360 px. Conserva la identidad CERN,
paleta Inferno, terminal animada, ecuaciones y composición general.

## Regeneración

Ejecutar `python scripts/generate_banner.py`. Solo requiere Python 3.
El generador produce `assets/banner.svg` y `assets/banner-static.svg`.
`ALTO_BANNER`, `DURACION_ROTACION`, `ESTADOS_ROTACION` y
`PASOS_MERIDIANO` controlan altura y rotación. La lista `particulas`
contiene posición inicial y final, duración, retraso, color, opacidad,
radio, longitud y grosor de estela. Los nombres y funciones están en español.

## Geometría y rotación

Se representa la hoja exterior del paraboloide de Flamm:
z² = 4r_s(r−r_s), con r_s=1 y 1 ≤ r/r_s ≤ 4.8.
El horizonte cumple r_s = 2GM/c². Es el corte ecuatorial espacial
de Schwarzschild.

Python calcula puntos `(r cos θ, r sin θ, 2√(r−1))`, aplica una matriz
de rotación alrededor del eje z y los proyecta con una cámara ortográfica
inclinada. Los 24 meridianos se muestrean con 33 puntos y 120 estados por vuelta.
Una animación CSS compartida modifica sus coordenadas `d`, con desfases distintos.

Cada meridiano completa 360° en **30 segundos**, con velocidad angular uniforme
y repetición infinita. Los extremos del ciclo reutilizan exactamente el mismo
estado. Un meridiano naranja destacado permite seguir la vuelta.
La opacidad se calcula mediante la normal de la superficie y una luz direccional.
Los nueve anillos, el horizonte y las ecuaciones permanecen fijos. La silueta
conserva su forma porque la superficie es axialmente simétrica.

La rotación pertenece a la visualización; el modelo sigue siendo Schwarzschild
sin rotación física. La interpolación entre estados aproxima los arcos con un
error proyectado máximo de 0.067 px. La discretización radial aporta menos
de 0.038 px, además del redondeo de coordenadas a 0.1 px.

Referencias: [Schwarzschild, JILA](https://jila.colorado.edu/~ajsh/bh/schwp.html),
[paraboloide de Flamm, Princeton](https://cchyba.scholar.princeton.edu/sites/g/files/toruqf3881/files/cchyba/files/chyba_j.math_.phys_.1982_0.pdf).

## Trayectorias de neutrinos

Once puntos de radio 3.6–3.8 px, con cinco tonos suaves: ámbar, melocotón,
rosa, malva y crema. Sus estelas tienen longitudes de 36–70 px y grosores
de 1.4–1.6 px. La opacidad máxima de la cabeza es 0.84; la estela es más tenue.

**Cuatro rutas cruzan entre esquinas opuestas**, en ambas diagonales y sentidos.
Las otras **siete atraviesan de borde a borde con pendientes moderadas distintas**.
Seis de ellas se desvían suavemente al pasar cerca del centro del horizonte
proyectado (915,358.4); la más alejada permanece recta. Los cuatro cruces
entre esquinas conservan su trayectoria recta.

`crear_recorrido` integra 64 pasos de longitud uniforme. La dirección gira
hacia el centro con una transición cúbica de derivada nula en sus extremos.
El desvío máximo observado es 4.154°, con un límite configurado de 5°.
La dirección de salida conserva el giro. Cada estela se orienta según la
tangente de la partícula, mediante una rotación local en su propio grupo.

El efecto es una interpretación artística de la desviación gravitacional,
no una integración de geodésicas ni un cálculo de masas o energías de neutrinos.
Referencia del fenómeno:
[Gravitational lensing of transient neutrino sources by black holes](https://www.sciencedirect.com/science/article/pii/S0370269308004589).

La duración se divide por 1.3 para aumentar la rapidez de paso un **30%**.
Cada cruce dura 0.885–1.154 s. La secuencia determinista se repite cada 28 s
con inicios en 0.6, 2.6, 4.6, 6.8, 9.1, 12.6, 15.1, 17.6, 20.6, 22.9 y 25.1 s.
Los intervalos entre inicios son 2–3.5 s, con como máximo una partícula móvil
simultánea. Fuera del cruce permanece oculta. Una máscara común protege
el nombre, la terminal y las ecuaciones tanto de las cabezas como de las estelas.

## Animación y respaldo

SVG autónomo de **131,994 bytes**, sin JavaScript, dependencias externas,
fuentes remotas, foreignObject ni imágenes rasterizadas. Se conservan
el degradado y la iluminación ambiental de 18 s, y las cuatro frases
de la terminal en un ciclo de 24 s.

Se comprobó CSS en Edge/Chromium 155 como SVG directo y como imagen `img`.
La propiedad CSS `d` tiene compatibilidad limitada entre navegadores.
Los atributos `d` mantienen una malla legible cuando no se admiten las animaciones.
[Documentación de la propiedad d, MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/d).

`prefers-reduced-motion` detiene las animaciones cuando el renderizador transmite
la preferencia al SVG. También se incluye `assets/banner-static.svg`, sin
animaciones ni partículas que parezcan detenidas en el recorrido.
Las ecuaciones usan texto y trazos SVG nativos, con exponentes,
subíndices y fracción vectorial; no dependen de LaTeX ni de MathJax.

## Verificación y publicación

`check_rotacion.py` valida la ecuación de Flamm, conservación de r y z,
rotación 3D de 30 s y cierre idéntico. `check_desviacion.py` valida
cuatro cruces exactos entre esquinas, siete ángulos distintos, orientación
hacia el centro y pasos de velocidad uniforme.

La revisión local comprobó las once rutas y 18 zonas de texto protegidas.
En 77 fotogramas no hubo cambios de píxeles en esas zonas; 48 mostraron
partículas en espacios libres. Diecisiete capturas densas junto a la malla
mostraron un giro visible de aproximadamente 3.13°. El primer cruce fue visible
a 1.323 s como SVG directo y 1.299 s como imagen. También se verificaron
movimiento reducido y respaldo estático, sin puntos fijos.

Publicación autorizada del 12 de octubre de 2026:
banner `64234d1a2ce741566a97700461c6fd27cf2b3fbf`;
README `14c393aa9298fd1f824d3cbc3f21daf49e4b9efc`.
El README conserva su contenido y solo cambia el recurso de la imagen y
su texto alternativo. La referencia al commit nuevo evita reutilizar el
banner anterior en caché. La lectura posterior de GitHub confirmó que
el generador, ambos SVG y README coinciden exactamente con los archivos comprobados.

El perfil real carga el recurso nuevo con tamaño natural 1200 × 576 px,
mostrado a 831 px de ancho. El SVG publicado abierto directamente conserva
once rutas, rotación de 30 s, malla sin transformación plana y ecuaciones
inmóviles. Las capturas de verificación y herramientas permanecen locales
en `docs/review/desviacion`.

La revisión del README real confirmó movimiento y estela: en tres capturas
consecutivas la cabeza avanzó aproximadamente 231 px en coordenadas del SVG
durante 218 ms. Las ecuaciones y el nombre conservaron su posición; el meridiano
naranja también se desplazó. Las muestras remotas bastan para comprobar el
movimiento, pero no para medir con precisión el ángulo de desviación, validado
localmente. Evidencia en `perfil/evidencia.json` dentro de la revisión local.
Esta comprobación corresponde al navegador Chromium disponible.
