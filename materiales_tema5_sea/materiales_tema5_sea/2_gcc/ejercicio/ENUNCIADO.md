# Ejercicio GCC — construir y enlazar módulos reales

Tras observar la demo del cliente mínimo (`2_gcc/demo/main.c` y `sumar.c`, incluidos en este paquete), completa las dos líneas marcadas en `compilar.sh`. El script ya compila por separado el cálculo (`odometro.o`), el estado (`odometro_estado.o`), las tres fuentes de adquisición y el cliente CLI. Trabaja en `/tmp`; no modifica los fuentes.

1. **S5-A2-01:** crea la biblioteca estática del núcleo con sus dos objetos.
2. **S5-A2-02:** completa el enlace del cliente con las bibliotecas construidas y deja el ejecutable preparado para localizar la biblioteca compartida. Interpreta los diagnósticos del enlazador y decide el orden y las opciones necesarias.

### Ejemplo de referencia con nombres ficticios

Suponemos que `cliente.o`, `calculo.o` y `estado.o` ya están compilados, que `libentrada.so` está creada en el mismo directorio y que el cálculo usa `hypot`:

```bash
ar rcs libcalculo.a calculo.o estado.o
gcc cliente.o -L. -lcalculo -lentrada -lm \
    -Wl,-rpath,'$ORIGIN' -o cliente
```

La primera orden reúne los dos objetos en la biblioteca estática. La segunda enlaza el objeto cliente con la estática, la compartida de entrada y la biblioteca matemática; registra también la ruta para encontrar la compartida al arrancar. Adapta los nombres a los objetos y bibliotecas del odómetro al completar los TODO.

Consulta el mapa de dependencias de la presentación antes de completar los TODO. Para que la CLI encuentre la biblioteca compartida situada junto a ella, añade al enlace `-Wl,-rpath,'$ORIGIN'`: `-Wl,` pasa opciones al enlazador, `-rpath` registra una ruta de búsqueda al ejecutar y `$ORIGIN` representa el directorio del ejecutable. Las comillas simples impiden que Bash expanda el dólar. `-L.` solo configura la búsqueda durante el enlace.

Ejecuta `bash compilar.sh` desde esta carpeta. El resultado previsto, con el CSV conocido, es `muestras=3 distancia=10.000`. Si los objetos se generan pero no el ejecutable, usa el mensaje del enlazador para localizar el símbolo que falta; si el ejecutable se genera pero no arranca, comprueba cómo encuentra las bibliotecas compartidas.

En la puesta en común, identifica qué productos dejan `-c`, `ar rcs`, `-shared` y el último `gcc`. Para consultar las etapas también puedes ejecutar sobre `comun/src/odometro.c` las opciones `-E` (preprocesado), `-S` (ensamblador) y `-c` (objeto). No hace falta leer enteros los archivos intermedios.
