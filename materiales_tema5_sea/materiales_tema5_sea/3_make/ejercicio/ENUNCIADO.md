# Ejercicio Make — reconstrucción selectiva del odómetro

Tras ver el grafo y una segunda ejecución sin cambios, completa los tres TODO del `Makefile`. Se construyen los módulos reales de `comun/src/`: `odometro.c` y `odometro_estado.c` forman `libodometro_core.a`; los tres archivos `fuente_*.c` forman `libfuente_posicion.a` o `.so`; `odometro_cli.c` produce el ejecutable. `test_odometro.c` no forma parte de esta variante didáctica.

1. **S5-A3-01:** completa la regla del objeto de estado a partir de los archivos y las dependencias que necesita su compilación.
2. **S5-A3-02:** completa la receta de enlace para producir el ejecutable declarado por la regla. Usa la salida del enlazador para diagnosticar errores.
3. **S5-A3-03:** completa la receta de la variante compartida y comprueba qué bibliotecas carga el ejecutable.

Trabaja en una **copia de todo `materiales_tema5_sea`** para alterar marcas de tiempo sin tocar la entrega original. Desde la raíz de la copia, entra en `3_make/ejercicio` y ejecuta:

```bash
make test                 # construcción inicial y trayectoria conocida
make                      # sin cambios: observa qué hace Make
# Antes de cada cambio, anota qué esperas que se actualice.
touch ../../comun/src/odometro_estado.c
make
make                      # otra vez, sin cambios
touch ../../comun/src/fuente_csv.c
make
touch ../../comun/include/odometro.h
make
make dinamico             # construye la variante con biblioteca compartida
```

Registra la salida y las recetas que se ejecutan en cada caso. Compara las observaciones con las predicciones que escribiste antes de cambiar las marcas de tiempo. `make test` debe terminar con `muestras=3 distancia=10.000`. Con `make dinamico`, consulta también `ldd build/odometro_cli_dinamico` y explica qué muestra.
