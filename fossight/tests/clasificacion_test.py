"""Pruebas guiadas del clasificador que se usa en la sesión 3.

Cada prueba sigue la misma secuencia: preparar una entrada, llamar a
``clasificar_obstaculos`` y comparar la salida completa con el resultado
esperado. Las funciones auxiliares de este archivo solo construyen esas
entradas y salidas; no contienen la lógica del clasificador.
"""

import pytest

from clasificacion import ResultadoClasificacion, clasificar_obstaculos


# El clasificador recibe una matriz de 6 filas por 10 columnas. Estos nombres
# hacen visibles las dimensiones y los valores que forman parte del contrato.
FILAS_MATRIZ = 6
COLUMNAS_MATRIZ = 10
VALOR_LEJANO = 0
VALOR_UMBRAL_CERCANIA = 176
VALOR_CERCANO_NOMINAL = 255
LIMITE_ANTIGUEDAD_MS = 500
FILAS_ZONA_ARRIBA = 2
PROPORCION_MINIMA = 0.30
FILAS_ZONA_ABAJO = 2

def resultado_esperado(
    arriba=False,
    abajo=False,
    izquierda=False,
    derecha=False,
    centro=False,
    failsafe=False,
):
    """Construye una salida indicando explícitamente sus seis booleanos."""
    return ResultadoClasificacion(
        arriba=arriba,
        abajo=abajo,
        izquierda=izquierda,
        derecha=derecha,
        centro=centro,
        failsafe=failsafe,
    )


@pytest.fixture
def matriz_con_siete_cercanas_arriba():
    """Crea una matriz nueva con siete cercanas en las dos filas superiores."""
    fila_con_tres_cercanas = (
        (VALOR_LEJANO,) * 3
        + (VALOR_CERCANO_NOMINAL,) * 3
        + (VALOR_LEJANO,) * (COLUMNAS_MATRIZ - 6)
    )
    fila_con_cuatro_cercanas = (
        (VALOR_LEJANO,) * 3
        + (VALOR_CERCANO_NOMINAL,) * 4
        + (VALOR_LEJANO,) * (COLUMNAS_MATRIZ - 7)
    )
    fila_sin_cercania = (VALOR_LEJANO,) * COLUMNAS_MATRIZ

    # Las dos filas de arriba tienen 3 + 4 = 7 celdas cercanas: más del 30 %
    # de las 20 celdas de la región. Las cuatro filas restantes están lejanas.
    filas_superiores = (fila_con_tres_cercanas, fila_con_cuatro_cercanas)
    filas_restantes = (fila_sin_cercania,) * (
        FILAS_MATRIZ - FILAS_ZONA_ARRIBA
    )
    return filas_superiores + filas_restantes

@pytest.fixture
def matriz_con_siete_cercanas_abajo():
    """Crea una matriz nueva con siete cercanas en las dos filas superiores."""
    fila_con_tres_cercanas = (
        (VALOR_LEJANO,) * 3
        + (VALOR_UMBRAL_CERCANIA,) * 3
        + (VALOR_LEJANO,) * (COLUMNAS_MATRIZ - 6)
    )
    fila_con_cuatro_cercanas = (
        (VALOR_LEJANO,) * 3
        + (VALOR_UMBRAL_CERCANIA,) * 4
        + (VALOR_LEJANO,) * (COLUMNAS_MATRIZ - 7)
    )
    fila_sin_cercania = (VALOR_LEJANO,) * COLUMNAS_MATRIZ

    # Las dos filas de arriba tienen 3 + 4 = 7 celdas cercanas: más del 30 %
    # de las 20 celdas de la región. Las cuatro filas restantes están lejanas.
    filas_inferiores = (fila_con_tres_cercanas, fila_con_cuatro_cercanas)
    filas_restantes = (fila_sin_cercania,) * (
        FILAS_MATRIZ - FILAS_ZONA_ABAJO
    )
    return filas_restantes + filas_inferiores


def arriba_activa_solo_su_alerta_test(matriz_con_siete_cercanas_arriba):
    matriz = matriz_con_siete_cercanas_arriba

    # La zona superior son sus dos primeras filas. Convertimos cada valor en
    # True si alcanza el umbral y contamos los True con ``sum``.
    valores_arriba = matriz[:FILAS_ZONA_ARRIBA]
    cercanas = [
        valor >= VALOR_UMBRAL_CERCANIA
        for fila in valores_arriba
        for valor in fila
    ]
    cantidad_cercanas = sum(cercanas)
    cantidad_total = len(cercanas)
    proporcion_cercana = cantidad_cercanas / cantidad_total

    # La cuenta queda visible: 7 celdas cercanas / 20 celdas = 35 %.
    celdas_cercanas_esperadas = 7
    celdas_totales_esperadas = FILAS_ZONA_ARRIBA * COLUMNAS_MATRIZ
    assert cantidad_cercanas == celdas_cercanas_esperadas
    assert cantidad_total == celdas_totales_esperadas
    assert proporcion_cercana > PROPORCION_MINIMA

    # 120 ms es menor que LIMITE_ANTIGUEDAD_MS, por lo que no hay
    # failsafe. Como solo tocamos la zona superior, solo ``arriba`` debe estar
    # activa.
    observado = clasificar_obstaculos(matriz, 120)
    esperado = resultado_esperado(arriba=True)

    assert observado == esperado


def antiguedad_failsafe_test(matriz_con_siete_cercanas_arriba):
    # Usamos siempre la misma matriz para que solo cambie la antigüedad del
    # dato. Si siguiera vigente, esta matriz activaría ``arriba``.
    matriz = matriz_con_siete_cercanas_arriba

    # Un milisegundo antes del límite, el dato todavía sirve y conserva la
    # alerta de arriba.
    assert clasificar_obstaculos(matriz, LIMITE_ANTIGUEDAD_MS - 1) == resultado_esperado(
        arriba=True
    )

    # LIMITE_ANTIGUEDAD_MS es el límite incluido: el dato caduca y queda solo
    # failsafe.
    assert clasificar_obstaculos(matriz, LIMITE_ANTIGUEDAD_MS) == resultado_esperado(
        failsafe=True
    )

    # Un milisegundo después se comprueba que el modo seguro también se
    # mantiene después del límite, no solo exactamente en la frontera.
    assert clasificar_obstaculos(matriz, LIMITE_ANTIGUEDAD_MS + 1) == resultado_esperado(
        failsafe=True
    )

def abajo_activa_solo_su_alerta_test(matriz_con_siete_cercanas_abajo):
    matriz = matriz_con_siete_cercanas_abajo

    # La zona superior son sus dos primeras filas. Convertimos cada valor en
    # True si alcanza el umbral y contamos los True con ``sum``.
    valores_abajo = matriz[FILAS_MATRIZ-2:FILAS_MATRIZ]
    cercanas = [
        valor >= VALOR_UMBRAL_CERCANIA
        for fila in valores_abajo
        for valor in fila
    ]
    cantidad_cercanas = sum(cercanas)
    cantidad_total = len(cercanas)
    proporcion_cercana = cantidad_cercanas / cantidad_total

    # La cuenta queda visible: 7 celdas cercanas / 20 celdas = 35 %.
    celdas_cercanas_esperadas = 7
    celdas_totales_esperadas = FILAS_ZONA_ABAJO * COLUMNAS_MATRIZ
    assert cantidad_cercanas == celdas_cercanas_esperadas
    assert cantidad_total == celdas_totales_esperadas
    assert proporcion_cercana > PROPORCION_MINIMA

    # 120 ms es menor que LIMITE_ANTIGUEDAD_MS, por lo que no hay
    # failsafe. Como solo tocamos la zona superior, solo ``arriba`` debe estar
    # activa.
    observado = clasificar_obstaculos(matriz, 120)
    esperado = resultado_esperado(abajo=True)

    assert observado == esperado