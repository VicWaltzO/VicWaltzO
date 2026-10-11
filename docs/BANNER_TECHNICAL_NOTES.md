# Banner INFERNO Scientific Identity

Banner de Owen A. Hurtado para `VicWaltzO/VicWaltzO`: 1200 × 576 px,
un 60% más alto que la revisión de 360 px. Conserva tipografía, paleta,
terminal, ecuaciones y siete trayectorias. Se retiraron las dos partículas
fijas que parecían detenidas a mitad del recorrido.

## Regeneración

Ejecutar `python scripts/generate_banner.py`. Solo requiere Python 3.
`ALTO_BANNER`, `DURACION_ROTACION`, `ESTADOS_ROTACION` y
`PASOS_MERIDIANO` controlan altura y rotación. La lista `particulas`
contiene posiciones, duración, retraso, color, opacidad y radio.
El generador produce `assets/banner.svg` y `assets/banner-static.svg`.

## Geometría y rotación

Se representa la hoja exterior del paraboloide de Flamm:
z² = 4r_s(r−r_s), con r_s=1 y 1 ≤ r/r_s ≤ 4.8.
El horizonte cumple r_s = 2GM/c². Es una representación del corte
ecuatorial espacial de Schwarzschild, no de una sombra ni de un disco de acreción.

Python calcula puntos `(r cos θ, r sin θ, 2√(r−1))`, aplica una matriz
de rotación alrededor del eje z y los proyecta con una cámara ortográfica
inclinada. Los 24 meridianos se muestrean con 33 puntos y 120 estados por vuelta.
Una trayectoria CSS compartida anima sus coordenadas `d`, con desfases distintos.
No se utiliza una rotación plana del grupo SVG.

Cada meridiano completa 360° en **30 segundos**, con velocidad angular uniforme
y repetición infinita. Los extremos del ciclo reutilizan exactamente el mismo
estado. Un meridiano naranja destacado permite seguir una vuelta completa.
La opacidad se calcula mediante la normal de la superficie y una luz direccional.
Los nueve anillos, el horizonte y las ecuaciones permanecen fijos. La silueta
conserva su forma porque la superficie es axialmente simétrica.

La rotación pertenece a la visualización; el modelo sigue siendo un agujero negro
de Schwarzschild sin rotación física. Entre estados, la interpolación lineal
aproxima los arcos con un error proyectado máximo de 0.067 px. La discretización
radial aporta menos de 0.038 px, además del redondeo de coordenadas a 0.1 px.

Referencias: [Schwarzschild, JILA](https://jila.colorado.edu/~ajsh/bh/schwp.html),
[paraboloide de Flamm, Princeton](https://cchyba.scholar.princeton.edu/sites/g/files/toruqf3881/files/cchyba/files/chyba_j.math_.phys_.1982_0.pdf).

## Animación y respaldo

El SVG es autónomo: sin JavaScript, dependencias externas, fuentes remotas,
foreignObject ni imágenes rasterizadas. Mide **94,391 bytes**.
Se conservan el degradado y la iluminación ambiental de 18 segundos,
así como las cuatro frases de la terminal en un ciclo de 24 segundos.

La animación CSS de `d` tiene compatibilidad limitada entre navegadores.
Se comprobó en Edge/Chromium 155 como SVG directo y como imagen `img`.
Los atributos `d` contienen una malla estática legible cuando no se admiten
las animaciones. No se afirma compatibilidad universal.
[Documentación de la propiedad d, MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/d).

`prefers-reduced-motion` detiene las animaciones cuando el renderizador transmite
la preferencia al SVG. En algunos contextos de imagen no se propaga; por eso
se incluye `assets/banner-static.svg`, sin animaciones. Para usarlo en el README,
cambiar el recurso de la imagen a esa alternativa.

## Partículas

Interpretación artística de neutrinos, no una simulación física. Siete puntos
de radio 3.6–3.8 px, estelas de 36 px y grosor 1.5 px; colores naranja y amarillo
pálido, opacidades 0.84–0.86. Tres diagonales atraviesan toda la tarjeta y pasan
detrás de máscaras que protegen el nombre, la terminal y las ecuaciones.

Los cruces duran 1.15–1.5 segundos. El ciclo determinista de 28 segundos inicia
cruces en 0.6, 4.6, 9.1, 12.6, 17.6, 20.6 y 25.1 segundos. Hay intervalos de
3–5 segundos entre inicios y como máximo una partícula móvil simultánea.
Fuera del cruce permanecen ocultas. El respaldo estático mantiene la identidad
sin puntos detenidos en las trayectorias.

## Verificación

Se validan XML, conservación de r y z bajo rotación, ecuación de Flamm,
duración de 30 segundos, cierre idéntico y cuatro orientaciones distintas.
Las pruebas del navegador comprueban ecuaciones inmóviles, ausencia de
transformaciones planas y un desplazamiento inferior a 0.03 px al atravesar
el reinicio del ciclo. La comparación como `img` muestra movimiento de la malla
sin cambios en el panel izquierdo ni en las ecuaciones.

Se verifican las siete partículas, las cuatro frases, movimiento reducido
y primer cruce visible antes de dos segundos, tanto directo como imagen.
En 21 fotogramas diagonales no hay cambios de píxeles en las zonas protegidas;
11 muestran la partícula en espacios libres. Las capturas y herramientas de
revisión permanecen locales en `docs/review/rotacion`.

El README conserva su contenido y fija el recurso animado al commit de su
publicación para evitar reutilizar una imagen anterior en caché. Cada actualización
del banner debe actualizar esa referencia.

Publicación autorizada: recurso fijado al commit
`cd20449152c6e00ac94ff16da23da7be83bc8083`; README actualizado en
`6f72099a97500d3c6784420c8911034c1d2686b5`. Se verificó el perfil real
con una imagen natural de 1200 × 576 px, mostrada a 831 px. Cien capturas
durante 31.5 segundos muestran el meridiano destacado en distintas orientaciones.
Cuatro capturas consecutivas muestran una partícula que avanza de x=451 a x=718
en la captura, con desaparición fuera del cruce. El SVG abierto directamente
también cambia su trayectoria y luz, declara 30 s y mantiene transform:none.
Los archivos publicados coinciden exactamente con los artefactos comprobados.
La imagen del perfil usa el nuevo commit, sin reutilizar el recurso anterior.
La verificación se realizó en el navegador Chromium disponible; otros motores
pueden utilizar el respaldo estático si no admiten CSS d.

Las ecuaciones usan texto y trazos SVG nativos, con exponentes, subíndices
y fracción vectorial; no dependen de LaTeX ni de MathJax.
