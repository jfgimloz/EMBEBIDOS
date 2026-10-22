# Materiales del tema 5 de SEA — demos y actividades

Esta carpeta reúne los materiales para seguir las demostraciones y las actividades en clase. No se pide instalar herramientas ni realizar tareas obligatorias fuera del aula. GTK se estudia observando el equipo del docente y respondiendo oralmente; S6-A2 y S6-A3 se conservan como práctica opcional posterior en un equipo preparado. Las demostraciones las ejecuta el docente en el equipo preparado. El estudiantado formula predicciones y trabaja las actividades sobre papel o en un equipo preparado, según el enunciado, con ayuda del docente. Las órdenes de las actividades sirven para ejecutar y comprobar las plantillas en clase; si se trabaja sobre papel, el docente realiza el contraste. La copia de trabajo permite modificar fuentes o marcas de tiempo sin alterar el material original. El recorrido calculado usa coordenadas de pantalla, no distancia física del ratón.

## Qué se entrega completo y qué debes resolver

El paquete incluye las demos introductorias y todos los componentes de apoyo del odómetro: cálculo y estado, adquisición CSV/X11, CLI, ventana GTK, configuración CMake, cabeceras, datos y pruebas. Los ejemplos de `demo/` están completos y pueden ejecutarse sin resolver las actividades. Los archivos de trabajo se entregan con sus TODO o con el fallo que hay que investigar; no se incluyen las soluciones del profesorado.

| Parte | Demo incluida y completa | Actividad |
|---|---|---|
| Bash | `1_bash/demo/tuberia.sh` y `posiciones.txt`; `entorno.sh` y `cambiar.sh` como apoyo del tema 6 | S5-A1: `1_bash/ejercicio/ENUNCIADO.md`. |
| GCC | `2_gcc/demo/main.c`, `sumar.c` y `sumar.h` | S5-A2: `2_gcc/ejercicio/ENUNCIADO.md`. |
| Make | `3_make/demo/minimo/`: Makefile, cliente, implementación y cabecera | S5-A3: `3_make/ejercicio/ENUNCIADO.md`. |
| CMake | `4_cmake/demo/minimo/` y `4_cmake/demo/odometro/` | Demostraciones resueltas; no hay ejercicio CMake. |
| GDB | `5_gdb/demo/sumar.c` | S6-A1: `5_gdb/ejercicio/ENUNCIADO.md`. |
| GTK | `6_gtk/demo/minimos/01_ventana.c` a `04_contexto.c` | Ampliación opcional S6-A2 y S6-A3: `6_gtk/ejercicio/ENUNCIADO.md` e `integracion/ENUNCIADO.md`. |

**Estos son los únicos archivos que debes completar o corregir:**

| Archivo | Trabajo pendiente | Estado antes de resolver |
|---|---|---|
| `1_bash/ejercicio/odometro.sh` | S5-A1: condición de referencia, suma decimal y actualización de coordenadas. | El `if` está pendiente: la plantilla tiene sintaxis incompleta y no se ejecuta todavía. |
| `2_gcc/ejercicio/compilar.sh` | S5-A2: biblioteca estática y enlace del cliente. | No termina la construcción del ejecutable. |
| `3_make/ejercicio/Makefile` | S5-A3: dependencia del objeto de estado y enlaces normal y compartido. | No construye la CLI hasta completar las recetas. |
| `5_gdb/ejercicio/odometro_fallo.c` | S6-A1: diagnosticar y corregir la inicialización responsable del primer tramo falso. | Compila, pero conserva deliberadamente el fallo; no se entrega corregido. |
| `6_gtk/ejercicio/callbacks.c` | S6-A2: pausa, reanudación y puesta a cero. | La ventana compila y abre; los controles están incompletos. |

En S6-A3 se registra esperado, observado y conclusión según el enunciado; no hay otro archivo de código que completar. Los enunciados y las instrucciones se entregan completos.

`comun/src/odometro.c`, `odometro_estado.c`, `fuente_*.c` y `odometro_cli.c`, sus cabeceras, `comun/CMakeLists.txt`, `comun/cmake/config.h.in`, `datos/` y las pruebas son apoyos completos. El núcleo está resuelto porque GCC y Make trabajan su construcción, no su implementación. **No añadas TODO a estos apoyos ni los sustituyas para resolver las actividades.**

Hay dos conexiones para conservar una sola plantilla por actividad: `comun/Makefile` remite a `3_make/ejercicio/Makefile`, y `comun/src/odometro_gtk.c` incluye `6_gtk/ejercicio/callbacks.c`. Por tanto, el cliente GTK común también mantiene esos callbacks pendientes y ambos clientes usan lo que completes allí. La ventana y la adquisición están suministradas. No hay una segunda versión resuelta de esos archivos en el paquete.

Las pruebas `pruebas/test_odometro.c` y `test_archivos.py` comprueban el núcleo y la CLI completos. `test_bash_odometro.py` comprueba tu Bash después de completar S5-A1; no contiene un solucionador. `test_gtk.c` comprueba los callbacks después de completar S6-A2. Estas dos últimas pruebas no se consideran aprobadas antes de resolver las plantillas.

El equipo de demostración necesita Bash, `bc`, GCC y Make para la sesión 5. `bc` es la calculadora externa que usa el script Bash para raíz cuadrada y aritmética decimal; Python no es necesario para ejecutar el odómetro. Las pruebas suministradas usan Python 3, que prepara el docente. En la sesión 6 se usan CMake y GDB; la parte GTK necesita también sus cabeceras de desarrollo. La adquisición del cursor en vivo requiere X11 y `xdotool`; el ejercicio Bash puede hacerse con el CSV suministrado.

## Contrato de los CSV

Los CSV de posiciones admiten una cabecera opcional exacta `x,y` o `X,Y` solo en la primera línea. Cada posición tiene dos enteros decimales en el rango de 32 bits con signo (−2147483648 a 2147483647); se admiten espacios alrededor de los campos, finales de línea LF o CRLF, líneas en blanco y comentarios que comienzan con `#`. No se admite una tercera columna ni el formato CSV general (campos entrecomillados, separadores alternativos, etc.).

## Seguir la secuencia de clase

Las demos permiten seguir los conceptos antes de cada actividad; las plantillas conservan el trabajo pendiente. La secuencia de clase es **S5-A1, S5-A2, S5-A3; CMake, S6-A1 y demostraciones GTK**. En GTK se predicen eventos, estados y resultados, se consultan firmas y señales en la documentación oficial y se contrasta lo previsto con la ejecución del docente. Las instrucciones siguientes sirven para observar las demostraciones y ejecutar o contrastar las decisiones en el aula. Los ejemplos de entorno son un apoyo del tema 6, sin añadir otra actividad a estas sesiones.

En un equipo preparado para la actividad, abra una terminal Bash con ayuda del docente dentro de la carpeta descomprimida `materiales_tema5_sea` (la que contiene este README, `comun` y `datos`). El destino `/tmp/sea-estudiantes` debe ser una carpeta nueva. Si ya está trabajando en esa copia, continúe con `cd /tmp/sea-estudiantes`; para crearla, compruebe su ubicación y copie el paquete:

```bash
pwd
ls README.md comun datos
cp -a . /tmp/sea-estudiantes
cd /tmp/sea-estudiantes
```

Edite los ejercicios de esa carpeta, conservando la entrega original. Puede cerrar y volver a abrir la terminal: cada apartado empieza con la orden para volver a la copia.

La preparación del equipo docente se realiza antes de clase: Bash, `bc`, GCC, Make, CMake y GDB; GTK añade `pkg-config` y sus cabeceras de desarrollo. El estudiantado no tiene que instalar estas herramientas. En Linux Mint, Ubuntu o Debian, el docente puede preparar el equipo con:

```bash
sudo apt install build-essential bc cmake gdb pkg-config libgtk-3-dev
```

Las ejecuciones siguientes usan CSV reproducible. No requieren capturar el cursor ni una sesión X11; la ventana GTK sí necesita una sesión gráfica. `1000` es un intervalo técnico en milisegundos, independiente de la duración de la actividad.

### Demo Bash — tubería y entorno

Desde la raíz de la copia, observa qué proceso produce, transforma y cuenta los datos:

```bash
cd /tmp/sea-estudiantes
bash 1_bash/demo/tuberia.sh
```

El resultado es `2` posiciones distintas. `sort` ordena las tres posiciones, `uniq` elimina repeticiones consecutivas y `wc -l` cuenta las líneas. Este ejemplo no calcula el recorrido ni completa el estado de S5-A1.

Como apoyo del tema 6, `bash 1_bash/demo/entorno.sh` muestra que `export` transmite la variable al proceso hijo, mientras que `source` ejecuta `cambiar.sh` en el shell actual. El valor sigue siendo `local` después de `bash` y pasa a `modificada` después de `source`.

### S5-A1 — completar y ejecutar Bash

Lea `1_bash/ejercicio/ENUNCIADO.md` y complete los tres TODO de `1_bash/ejercicio/odometro.sh` en la copia. Antes de completarlos, la plantilla no calcula el recorrido esperado. Ejecute:

```bash
cd /tmp/sea-estudiantes
bash 1_bash/ejercicio/odometro.sh \
  --reproducir datos/trayectoria_10.csv --salida /tmp/sea-estudiantes/bash.csv
cat /tmp/sea-estudiantes/bash.csv
```

Resultado tras resolver en la terminal: `muestras=3 distancia=10.000`. El CSV de salida contiene la cabecera `x,y` y las tres posiciones; el resumen de muestras y distancia no se escribe en ese archivo. La primera muestra suma cero. Entrada y salida deben ser archivos distintos. Explique las tres decisiones de estado que completó.

### Demo GCC — cliente, implementación y cabecera

El ejemplo mínimo está completo. Observa los productos de cada etapa y el diagnóstico al enlazar sin la implementación:

```bash
cd /tmp/sea-estudiantes
mkdir -p "/tmp/sea-estudiantes/gcc-minimo"
gcc -E 2_gcc/demo/main.c -o "/tmp/sea-estudiantes/gcc-minimo/main.i"
gcc -S 2_gcc/demo/main.c -o "/tmp/sea-estudiantes/gcc-minimo/main.s"
gcc -Wall -Wextra -c 2_gcc/demo/main.c -o "/tmp/sea-estudiantes/gcc-minimo/main.o"
gcc -Wall -Wextra -c 2_gcc/demo/sumar.c -o "/tmp/sea-estudiantes/gcc-minimo/sumar.o"
# Esta orden debe fallar: falta la definición de sumar.
gcc "/tmp/sea-estudiantes/gcc-minimo/main.o" -o "/tmp/sea-estudiantes/gcc-minimo/incompleto"
gcc "/tmp/sea-estudiantes/gcc-minimo/main.o" "/tmp/sea-estudiantes/gcc-minimo/sumar.o" \
  -o "/tmp/sea-estudiantes/gcc-minimo/sumar"
"/tmp/sea-estudiantes/gcc-minimo/sumar"
```

El ejecutable completo imprime `resultado=5`. La cabecera declara la función y permite compilar al cliente; la implementación aporta la definición necesaria para enlazar. Después se aplica esa distinción a los módulos y bibliotecas del odómetro.

### S5-A2 — completar construcción y enlace con GCC

Lea `2_gcc/ejercicio/ENUNCIADO.md` y complete los dos TODO de `2_gcc/ejercicio/compilar.sh`. Después:

```bash
cd /tmp/sea-estudiantes
bash 2_gcc/ejercicio/compilar.sh
```

El script construye una biblioteca estática del núcleo, una compartida de adquisición y la CLI; reproduce `datos/trayectoria_10.csv` y debe terminar con `muestras=3 distancia=10.000`. Usa y elimina su propio directorio temporal; no busque el ejecutable en la entrega. Sin completar los TODO falla la construcción. Distinga compilación de objetos, creación de bibliotecas y enlace del cliente.

### Demo Make — reglas y reconstrucción del mínimo

El Makefile del mínimo está completo. Trabaja en la copia para cambiar sus marcas de tiempo:

```bash
cd /tmp/sea-estudiantes
make -C 3_make/demo/minimo
./3_make/demo/minimo/sumar
make -C 3_make/demo/minimo
touch 3_make/demo/minimo/sumar.c
make -C 3_make/demo/minimo
touch 3_make/demo/minimo/sumar.h
make -C 3_make/demo/minimo
```

El programa imprime `resultado=5`. La segunda construcción no repite recetas; modificar el fuente reconstruye su objeto y enlaza, y modificar la cabecera reconstruye ambos objetos. Localiza objetivos, prerrequisitos, tabuladores y las variables `$@`, `$<` y `$^`. El ejercicio posterior conserva pendientes las reglas y enlaces del odómetro.

### S5-A3 — completar Make y observar reconstrucciones

Lea `3_make/ejercicio/ENUNCIADO.md` y complete los tres TODO del Makefile. Todo lo siguiente ocurre en la copia, pues `touch` cambia marcas de tiempo:

```bash
cd /tmp/sea-estudiantes
make -C 3_make/ejercicio test
make -C 3_make/ejercicio
touch comun/src/odometro_estado.c
make -C 3_make/ejercicio
touch comun/src/fuente_csv.c
make -C 3_make/ejercicio
touch comun/include/odometro.h
make -C 3_make/ejercicio
make -C 3_make/ejercicio dinamico
ldd 3_make/ejercicio/build/odometro_cli_dinamico
```

`make test` debe terminar con `muestras=3 distancia=10.000`; sin cambios, `make` no repite recetas. Antes de cada cambio, anote qué espera que haga Make. Observe las recetas que ejecuta y los productos que cambian; compare la salida con su predicción y justifique cada diferencia a partir de las dependencias declaradas. La consulta de `ldd` permite identificar bibliotecas compartidas.

### Sesión 6 — ejecutar los dos ejemplos CMake resueltos

El docente ejecuta ambos ejemplos al comienzo de la sesión 6. No dependen de completar los ejercicios anteriores. La clase identifica configurar, construir, probar y ejecutar; no hay tarea CMake para resolver:

```bash
cd /tmp/sea-estudiantes
cmake -S 4_cmake/demo/minimo -B /tmp/sea-estudiantes/cmake-minimo
cmake --build /tmp/sea-estudiantes/cmake-minimo
/tmp/sea-estudiantes/cmake-minimo/sumar
cmake -S 4_cmake/demo/odometro -B /tmp/sea-estudiantes/cmake-odometro
cmake --build /tmp/sea-estudiantes/cmake-odometro
ctest --test-dir /tmp/sea-estudiantes/cmake-odometro --output-on-failure
/tmp/sea-estudiantes/cmake-odometro/componentes/odometro_cli \
  --csv datos/trayectoria_10.csv --intervalo-ms 0 --silencioso
```

El mínimo imprime `resultado=5`. El odómetro construye los módulos comunes completos, CTest verifica el núcleo, la trayectoria y el manejo de archivos de la CLI, y la CLI imprime `muestras=3 distancia=10.000`. Identifique qué hace cada paso: configurar, construir, probar y ejecutar. Si GTK está disponible, también construye el cliente común con los callbacks todavía pendientes de S6-A2. Las pruebas GTK están desactivadas por defecto hasta completar esa actividad; las pruebas del núcleo y la CLI no dependen de ella.

### Demo GDB — familiarización con el depurador

El programa `sumar.c` está completo y no contiene el fallo de la actividad:

```bash
cd /tmp/sea-estudiantes
gcc -Wall -Wextra -O0 -g3 5_gdb/demo/sumar.c -o "/tmp/sea-estudiantes/gdb-sumar"
gdb "/tmp/sea-estudiantes/gdb-sumar"
```

En `(gdb)`:

```gdb
break sumar
run
info args
next
print resultado
backtrace
finish
continue
quit
```

Observa `a=2` y `b=3`; después de ejecutar la asignación, `resultado=5`. `next` avanza una línea y `backtrace` muestra las llamadas. Esta familiarización precede al diagnóstico del odómetro; no incluye su versión corregida.

### S6-A1 — reproducir e investigar el fallo con GDB

Lea `5_gdb/ejercicio/ENUNCIADO.md`, formule dos hipótesis y compile el caso todavía defectuoso desde la raíz de la copia:

```bash
cd /tmp/sea-estudiantes
gcc -std=c11 -Wall -Wextra -O0 -g3 -Icomun/include \
  5_gdb/ejercicio/odometro_fallo.c -lm -o /tmp/sea-estudiantes/gdb-fallo
/tmp/sea-estudiantes/gdb-fallo
gdb /tmp/sea-estudiantes/gdb-fallo
```

La primera posición `(100,100)` da la distancia falsa `141.421`. En el indicador `(gdb)`, use estas órdenes para contrastar sus hipótesis:

```gdb
break odometro_actualizar
run
info args
print *odometro
next
backtrace
continue
quit
```

Registre el estado observado antes de actualizar y explique qué decisión causa el tramo falso. Después corrija solo el punto responsable en el fuente de la copia y repita la compilación y ejecución: la misma primera posición debe dar `0.000`. Añada después `(103,104)` y repita esa posición; los acumulados esperados son `0.000`, `5.000`, `5.000`. Esta regresión comprueba que el arreglo no se limita a dejar de sumar.

### Demos GTK del profesor — ventana, botón, señal y contexto

Los cuatro mínimos están completos. El docente los construye y muestra en la sesión gráfica preparada:

```bash
cd /tmp/sea-estudiantes
make -C 6_gtk/demo/minimos
"/tmp/sea-demo-gtk/01_ventana"
"/tmp/sea-demo-gtk/02_boton"
"/tmp/sea-demo-gtk/03_senal"
"/tmp/sea-demo-gtk/04_contexto"
```

El Makefile suministrado consulta `pkg-config --cflags gtk+-3.0` para compilar y `pkg-config --libs gtk+-3.0` para enlazar. Los ejecutables quedan en `/tmp/sea-demo-gtk`. Cierra cada ventana para pasar a la siguiente. La primera presenta ventana y bucle; la segunda añade un botón sin acción; la tercera conecta su señal a un contador; la cuarta comparte estado mediante un contexto explícito. Identifica `g_signal_connect`, el callback y `gpointer`. Estos ejemplos no implementan el temporizador ni los controles pendientes del odómetro.

### Ampliación opcional posterior S6-A2 y S6-A3 — construir la plantilla GTK y comprobar controles

Estas órdenes son una referencia para practicar después, si dispone de un equipo preparado; no se ejecutan obligatoriamente durante la clase. La plantilla GTK ya compila: pruebe primero la construcción y apertura, y complete después los tres TODO de `6_gtk/ejercicio/callbacks.c` siguiendo el enunciado. Desde la raíz de la copia:

```bash
cd /tmp/sea-estudiantes
cmake -S 6_gtk/ejercicio -B /tmp/sea-estudiantes/gtk
cmake --build /tmp/sea-estudiantes/gtk
/tmp/sea-estudiantes/gtk/actividad_gtk datos/trayectoria_larga.csv 1000
```

Antes de completar los callbacks, la ventana abre pero los controles no adquieren ni reinician correctamente. Tras cada edición, cierre la aplicación, repita `cmake --build /tmp/sea-estudiantes/gtk` y vuelva a ejecutarla. Pulse «Iniciar»: sin pausas ni reinicios, la trayectoria larga debe producir 21 muestras y distancia 100. Para el caso corto, cierre la ventana y ejecute:

```bash
cd /tmp/sea-estudiantes
/tmp/sea-estudiantes/gtk/actividad_gtk datos/trayectoria_10.csv 1000
```

Debe obtener 3 muestras y distancia 10. Si ejecuta desde `6_gtk/ejercicio`, las rutas CSV son `../../datos/trayectoria_larga.csv` y `../../datos/trayectoria_10.csv`.

Compruebe manualmente pausa, reanudación, «Poner a cero», fin de datos, «Repetir CSV», clics alternos y cierre; siga `6_gtk/ejercicio/integracion/ENUNCIADO.md` para **S6-A3**. «Poner a cero» no vuelve al principio del archivo; «Repetir CSV» lo reabre y deja la aplicación preparada para pulsar «Iniciar». La construcción no prueba esa interacción. El CSV se detiene durante la pausa y no simula movimiento físico del cursor: observe ese caso en la demostración docente con X11 y registre el programa utilizado. El cliente común `odometro_gtk` usa los mismos callbacks que acabas de completar y conserva la adquisición X11. Solo prueba ese modo en el equipo preparado por el docente; si no hay X11 y libxdo, identifique la comprobación como pendiente.

### Pruebas suministradas después de completar las actividades

Para comprobar tu Bash completado, desde la raíz de la copia:

```bash
python3 -m unittest discover -s pruebas -p 'test_bash_odometro.py'
```

Para comprobar los callbacks completados, reutiliza la construcción común de la demo CMake y activa su prueba:

```bash
cmake -S 4_cmake/demo/odometro -B "/tmp/sea-estudiantes/cmake-odometro" -DPROBAR_GTK=ON
cmake --build "/tmp/sea-estudiantes/cmake-odometro"
ctest --test-dir "/tmp/sea-estudiantes/cmake-odometro" --output-on-failure
```

`callbacks_gtk` comprueba estados y temporizadores con widgets GTK y el CSV conocido; requiere GTK instalado y una pantalla disponible. Si no hay pantalla, se marca como omitida. No sustituye la comprobación manual de la ventana ni prueba la captura X11. Para construir el cliente común con tus callbacks y ejecutar ese modo en el equipo preparado, usa `"/tmp/sea-estudiantes/cmake-odometro/componentes/odometro_gtk"` sin argumento CSV. No constituye otra actividad ni otra entrega.
