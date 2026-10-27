"""Clasificación determinista de una matriz simulada de 6 x 10."""

from typing import NamedTuple


class ResultadoClasificacion(NamedTuple):
    """Alertas independientes y estado seguro del núcleo de clasificación."""

    arriba: bool
    abajo: bool
    izquierda: bool
    derecha: bool
    centro: bool
    failsafe: bool


ZONAS = (
    ("arriba", range(0, 2), range(0, 10)),
    ("abajo", range(4, 6), range(0, 10)),
    ("izquierda", range(0, 6), range(0, 3)),
    ("derecha", range(0, 6), range(7, 10)),
    ("centro", range(0, 6), range(3, 7)),
)
UMBRAL_CERCANIA = 176
MINIMOS_ACTIVACION = {
    "arriba": 7,
    "abajo": 7,
    "izquierda": 6,
    "derecha": 6,
    "centro": 8,
}
SIN_ALERTAS = ResultadoClasificacion(False, False, False, False, False, False)
FALLO_SEGURO = ResultadoClasificacion(False, False, False, False, False, True)


def _matriz_valida(matriz: object) -> bool:
    return (
        isinstance(matriz, tuple)
        and len(matriz) == 6
        and all(isinstance(fila, tuple) and len(fila) == 10 for fila in matriz)
        and all(
            isinstance(valor, int)
            and not isinstance(valor, bool)
            and 0 <= valor <= 255
            for fila in matriz
            for valor in fila
        )
    )


def clasificar_obstaculos(
    matriz: object, antiguedad_ms: object
) -> ResultadoClasificacion:
    """Activa todas las zonas que alcanzan el umbral o solo ``failsafe``.

    Las celdas iguales o mayores que 176 se consideran cercanas. Cada zona se
    evalúa por separado y se activa cuando alcanza su mínimo entero de celdas
    cercanas.
    """
    if (
        not _matriz_valida(matriz)
        or not isinstance(antiguedad_ms, int)
        or isinstance(antiguedad_ms, bool)
        or antiguedad_ms < 0
        or antiguedad_ms >= 500
    ):
        return FALLO_SEGURO

    activas = {}
    for nombre, filas, columnas in ZONAS:
        valores = [matriz[fila][columna] for fila in filas for columna in columnas]
        activas[nombre] = (
            sum(valor >= UMBRAL_CERCANIA for valor in valores)
            >= MINIMOS_ACTIVACION[nombre]
        )

    return ResultadoClasificacion(
        activas["arriba"],
        activas["abajo"],
        activas["izquierda"],
        activas["derecha"],
        activas["centro"],
        False,
    )


clasificar_obstaculo = clasificar_obstaculos
