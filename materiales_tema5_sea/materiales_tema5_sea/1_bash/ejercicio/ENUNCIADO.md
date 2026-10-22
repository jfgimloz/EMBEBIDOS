# Actividad S5-A1 — completar el cálculo del odómetro Bash

Trabajad en pareja durante diez minutos. Se puede resolver sobre papel o en una terminal con el CSV suministrado, sin X11. La demostración anterior muestra la lectura del CSV, la expresión de `bc` y el resultado esperado. La plantilla ya incluye opciones, validación, adquisición, lectura de filas, bucles, escritura del CSV y cálculo de cada tramo. Solo faltan tres decisiones del estado.

1. `S5-A1-01`: completa la condición que determina si la muestra actual ya tiene una posición anterior. Explica por qué la primera muestra no suma recorrido.
2. `S5-A1-02`: sustituye `distancia=0` dentro de esa condición por `distancia=$(printf '%s + %s\n' "$distancia" "$tramo" | bc -l) || exit 5`. La expresión suma el tramo decimal al acumulado.
3. `S5-A1-03`: completa la actualización de las coordenadas anteriores con la muestra actual. Explica por qué se actualiza la referencia después de calcular el tramo.

La expresión ya proporcionada `sqrt((x-anterior_x)^2 + (y-anterior_y)^2)` representa la distancia euclídea. `bc` es una calculadora externa invocada por el script; Bash organiza la lectura, el bucle, el estado y la salida.

Desde la raíz del paquete distribuido `materiales_tema5_sea`, comprobad:

```bash
bash 1_bash/ejercicio/odometro.sh \
  --reproducir datos/trayectoria_10.csv --salida /tmp/aula.csv
```

El resumen esperado es `muestras=3 distancia=10.000`. La primera muestra fija referencia; las dos siguientes suman 5 cada una. El CSV de salida conserva una sola cabecera. No hace falta diseñar otra validación ni completar la adquisición X11.
