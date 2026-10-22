# Dos alternativas para comprobar el núcleo

Demostración posterior a la actividad evaluable de GCC; no es otra entrega.
Ambas baterías comprueban el mismo código C en cinco casos: primera muestra,
posición repetida, ida y vuelta, reinicio y pausa/reanudación. Contienen catorce
comprobaciones. Ejecutar desde la raíz de `materiales_tema5_sea/`.

## Alternativa C

Requiere GCC. El programa de pruebas es un cliente del núcleo:

```bash
prueba=$(mktemp /tmp/sea-test-XXXXXX)
gcc -std=c11 -Wall -Wextra -Icomun/include pruebas/test_odometro.c \
    comun/src/odometro.c comun/src/odometro_estado.c -lm -o "$prueba"
"$prueba"
rm -f -- "$prueba"
```

Salida esperada: `5/5 casos del núcleo: OK (14 comprobaciones)`.

## Alternativa pytest

Requiere Python 3, GCC y pytest. Si pytest no está disponible, preparar un entorno:

```bash
python3 -m venv /tmp/sea-pytest-venv
/tmp/sea-pytest-venv/bin/python -m pip install pytest
/tmp/sea-pytest-venv/bin/python -m pytest -q pruebas/test_odometro.py
```

Con pytest ya disponible: `python3 -m pytest -q pruebas/test_odometro.py`.
Salida esperada: `5 passed` (el tiempo varía).

La fixture `nucleo` compila los dos fuentes reales en una biblioteca `.so`
temporal y `ctypes` permite llamar a sus funciones desde Python. La fixture
`estado` inicializa un odómetro distinto para cada caso. `assert` expresa los
resultados esperados y `pytest.approx` admite una tolerancia absoluta de 1e-9
para los números en coma flotante. Si cambia la estructura de `odometro.h`, hay
que actualizar su declaración en `ctypes`, respetando tipos y orden.

No se traduce el algoritmo a Python ni se ejecuta la batería C desde pytest:
son dos clientes de prueba alternativos del mismo núcleo. pytest se detiene
en la primera aserción fallida de cada caso; la batería C acumula fallos.

Estas pruebas no comprueban GTK/X11, la adquisición CSV ni todas las entradas
posibles. La ejecución de la CLI con `trayectoria_10.csv` es una comprobación
complementaria de integración y debe producir `muestras=3 distancia=10.000`.
