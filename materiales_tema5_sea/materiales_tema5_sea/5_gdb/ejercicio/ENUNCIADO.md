# Actividad 1 — investigar antes de corregir

Síntoma: la primera posición `(100,100)` produce una distancia distinta de cero.

1. Formula dos hipótesis próximas.
2. Compila y abre el programa con:

   ```bash
   gcc -std=c11 -Wall -Wextra -O0 -g3 -I../../comun/include odometro_fallo.c -lm -o /tmp/odometro_fallo
   gdb /tmp/odometro_fallo
   ```

3. Decide qué valor observar antes y después de la actualización para distinguir tus hipótesis. Como apoyo, puedes usar `break odometro_actualizar`, `run`, `info args`, `print *odometro`, `next` y `backtrace`.
4. `S6-A1-01`: registra los valores observados y explica qué decisión causa el primer tramo inesperado. Si te atascas, compara el estado antes y después de `odometro_actualizar`; después comprueba qué valor indica si ya existe una posición anterior.
5. Tras justificar la causa con GDB, corrige solo el punto responsable y verifica que la primera distancia es cero. Añade una segunda llamada con `(103,104)` y repite esa misma posición en el programa corregido: los acumulados esperados son `0.000`, `5.000` y `5.000`. Así descartas un arreglo que simplemente deje de sumar.

Tiempo: 20 minutos. Dificultad: media.
