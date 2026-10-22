#!/usr/bin/env bash
set -euo pipefail

raiz=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
trabajo=$(mktemp -d /tmp/sea-gcc-XXXXXX)
trap 'rm -rf -- "$trabajo"' EXIT
cd "$trabajo"

for modulo in odometro odometro_estado; do
    gcc -std=c11 -Wall -Wextra -O0 -g3 -I"$raiz/comun/include" \
        -c "$raiz/comun/src/$modulo.c" -o "$modulo.o"
done
# TODO S5-A2-01: crear libodometro_core.a con los dos objetos

for modulo in fuente_posicion fuente_csv fuente_xdo; do
    gcc -std=c11 -Wall -Wextra -O0 -g3 -fPIC -I"$raiz/comun/include" \
        -c "$raiz/comun/src/$modulo.c" -o "$modulo.o"
done
gcc -shared fuente_posicion.o fuente_csv.o fuente_xdo.o -o libfuente_posicion.so
gcc -std=c11 -Wall -Wextra -O0 -g3 -I"$raiz/comun/include" \
    -c "$raiz/comun/src/odometro_cli.c" -o odometro_cli.o
# TODO S5-A2-02: enlazar el cliente con ambas bibliotecas, libm y ruta de carga

./odometro_cli --csv "$raiz/datos/trayectoria_10.csv" --intervalo-ms 0 --silencioso
