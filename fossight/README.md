# FOSSight · paquete de prácticas

Este paquete contiene la implementación Python de referencia de un proyecto
FOSSight ficticio que pretende proporcionar firmware FOSS para Argus II y usa rutas relativas. La responsabilidad central evaluada es
`clasificar_obstaculos(matriz, antiguedad_ms)`: recibe una matriz de 6 × 10 y
una antigüedad en milisegundos, y devuelve un `ResultadoClasificacion` inmutable
con cinco alertas independientes y `failsafe`. Blanco (valor alto) significa
cerca. Varias zonas pueden estar activas a la vez; una matriz inválida o
`antiguedad_ms >= 500` deja las cinco alertas a `False` y activa solo
`failsafe`. Un adaptador externo convertiría un timestamp de captura en
`antiguedad_ms`; esa conversión no forma parte del contrato Python. La
profundidad solo prepara proximidad relativa (blanco = más cerca), no una
medida métrica.

Una celda se considera cercana cuando su valor es `>=176`. La GUI muestra
`FAILSAFE` por separado y desactiva la emisión de sonidos mientras ese estado
está activo; no representa electrodos ni patrones de estimulación de Argus II.

Con una matriz válida y una antigüedad menor de 500 ms, las zonas se cuentan
de forma independiente y se activan cuando superan el 30 % de su máscara:
`arriba` y `abajo` ocupan 2 × 10 celdas y se activan con `>=7/20`;
`izquierda` y `derecha` ocupan 3 × 6 y se activan con `>=6/18`;
`centro` ocupa 4 × 6 y se activa con `>=8/24`.

## Preparación y pruebas

Desde esta carpeta:

```text
python3 -m venv .venv-pruebas
.venv-pruebas/bin/python -m pip install 'pytest>=8,<9' 'Pillow>=10,<12'
.venv-pruebas/bin/python -m pytest -p no:cacheprovider -v
```

La primera línea crea el entorno virtual local `.venv-pruebas`, para aislar las
pruebas y sus dependencias del Python del sistema. La segunda usa el Python de
ese entorno para instalar pytest 8.x y Pillow en una versión compatible (desde
10 hasta antes de 12). La tercera ejecuta las pruebas con ese mismo Python:
`-p no:cacheprovider` desactiva la caché de pytest y `-v` muestra cada prueba y
su resultado con detalle. Ejecutar las líneas en este orden hace que la
comprobación sea reproducible y no dependa de paquetes globales ni de restos de
ejecuciones anteriores.

También puedes ejecutar las tres líneas de una vez con
`./preparar_entorno_pruebas.sh`; el script crea `.venv-pruebas`, instala esas
dependencias y ejecuta la batería.

El lanzador de escenarios queda disponible como `tests/ejecutar_tests.sh`:

```text
./tests/ejecutar_tests.sh -t antiguedad -q
./tests/ejecutar_tests.sh -t nominal -v
```

Los
directorios `__pycache__`, los enlaces simbólicos y las entradas que no sean
archivos regulares no forman parte del paquete. No se demuestra la ejecución real
de GTK, audio, modelos, cámara, hardware ni seguridad clínica.

`SKIPPED` significa que una prueba no se ejecutó y no equivale a `PASA`.
La colección distribuida se limita a las plantillas visibles de
`tests/`; incluye también `ruido_aislado_test.py`, que permite comprobar el
caso discriminante de una variante. Las metapruebas docentes, sus soluciones y
los casos de imágenes permanecen fuera del paquete del alumnado.

## Variantes y caso discriminante

`src/variantes.py` contiene cinco implementaciones deliberadamente defectuosas
para practicar pruebas de mutación. La prueba visible
`tests/ruido_aislado_test.py` distingue la referencia de la variante que activa
una zona por una sola celda cercana:

```text
./tests/ejecutar_tests.sh -t bateria -q
./tests/ejecutar_tests.sh -t discriminante -q
FOSSIGHT_VARIANTE=ruido_aislado ./tests/ejecutar_tests.sh -t discriminante -q
```

La referencia debe pasar el caso discriminante y `ruido_aislado` debe fallarlo;
ese resultado demuestra que la prueba observa la mutación.

## Documentación incluida

`AVISO_LICENCIAS.md` documenta el alcance de las licencias del código y los
recursos. `pyproject.toml_README.md` explica la configuración TOML del proyecto,
incluidos pytest y los módulos Python directos de `src/`. Ambos archivos son
copias de la documentación mantenida en `fossight_dev/`.

## Abrir la GUI sin modelos

En Linux Mint, Ubuntu o Debian instala las dependencias del sistema:

```text
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-gstreamer-1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good python3-pil
```

Abre la interfaz desde esta carpeta:

```text
PYTHONPATH=src /usr/bin/python3 ejecutar_gui.py
```

Para probarla sin descargar ni cargar modelos, proporciona los dos PNG de un
caso autorizado disponible en tu equipo:

1. deja desmarcada «Obtener profundidad desde el PNG RAW»;
2. en «Elegir PNG RAW», selecciona el `original.png` del caso;
3. en «Elegir PNG de profundidad», selecciona su `profundidad.png`;
4. conserva una antigüedad menor de 500 ms y pulsa «Procesar imagen»;
5. cambia entre `profundidad_grises` y `raw_grises` para comparar la matriz.

La GUI es únicamente un demostrador para el aula, no el firmware ni una prueba
de compatibilidad con Argus II. No depende del nombre de la carpeta y no
presupone que ambos PNG estén en una ubicación absoluta concreta.

Los modelos son opcionales y se configuran por separado en
[`MODELOS_OPCIONALES.md`](MODELOS_OPCIONALES.md).

## Casos y límites

`casos/` no contiene imágenes de caso. Para usar la GUI debes proporcionar los
PNG de un caso por separado. Los seis casos históricos del
repositorio docente no se redistribuyen porque su licencia no está establecida.
Consulta `casos/origenes.md` para conocer el alcance de esta distribución.

No se incluyen entornos, cachés, pesos ni un solucionario docente. Consulta
`AVISO_LICENCIAS.md` para el estado de licencia del código y los recursos. Las
pruebas no abren GTK, no reproducen audio, no usan red y no ejecutan inferencia;
esas capas son adaptadores o preparación, no evidencia principal del
clasificador. Los seis booleanos no se traducen aquí a electrodos, patrones de
estimulación ni hardware Argus II.
