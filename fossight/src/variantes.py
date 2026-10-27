"""Variantes deliberadamente defectuosas para practicar pruebas de mutación."""

from collections.abc import Callable

from clasificacion import (
    FALLO_SEGURO,
    MINIMOS_ACTIVACION,
    SIN_ALERTAS,
    ZONAS,
    ResultadoClasificacion,
    _matriz_valida,
    clasificar_obstaculos,
)


Clasificador = Callable[[object, object], ResultadoClasificacion]


def _clasificar_con_limites(
    matriz: object,
    antiguedad_ms: object,
    *,
    cerca: Callable[[int], bool],
    caducada: Callable[[int], bool],
) -> ResultadoClasificacion:
    if (
        not _matriz_valida(matriz)
        or not isinstance(antiguedad_ms, int)
        or isinstance(antiguedad_ms, bool)
        or antiguedad_ms < 0
        or caducada(antiguedad_ms)
    ):
        return FALLO_SEGURO

    activas = {}
    for nombre, filas, columnas in ZONAS:
        valores = [matriz[fila][columna] for fila in filas for columna in columnas]
        activas[nombre] = (
            sum(cerca(valor) for valor in valores) >= MINIMOS_ACTIVACION[nombre]
        )
    return ResultadoClasificacion(
        activas["arriba"],
        activas["abajo"],
        activas["izquierda"],
        activas["derecha"],
        activas["centro"],
        False,
    )


def clasificar_umbral_estricto(
    matriz: object, antiguedad_ms: object
) -> ResultadoClasificacion:
    """Variante 1: considera cerca solo valores mayores que 176."""
    return _clasificar_con_limites(
        matriz,
        antiguedad_ms,
        cerca=lambda valor: valor > 176,
        caducada=lambda antiguedad_ms: antiguedad_ms >= 500,
    )


def clasificar_antiguedad_estricta(
    matriz: object, antiguedad_ms: object
) -> ResultadoClasificacion:
    """Variante 2: deja pasar incorrectamente una imagen de 500 ms."""
    return _clasificar_con_limites(
        matriz,
        antiguedad_ms,
        cerca=lambda valor: valor >= 176,
        caducada=lambda antiguedad_ms: antiguedad_ms > 500,
    )


def clasificar_exclusiva(
    matriz: object, antiguedad_ms: object
) -> ResultadoClasificacion:
    """Variante 3: conserva únicamente la primera alerta activa."""
    resultado = clasificar_obstaculos(matriz, antiguedad_ms)
    if resultado.failsafe:
        return resultado
    activas = list(resultado[:5])
    if True not in activas:
        return resultado
    primera = activas.index(True)
    return ResultadoClasificacion(
        *(indice == primera for indice in range(5)),
        False,
    )


def clasificar_sin_failsafe(
    matriz: object, antiguedad_ms: object
) -> ResultadoClasificacion:
    """Variante 4: confunde cualquier fallo seguro con ausencia de alertas."""
    resultado = clasificar_obstaculos(matriz, antiguedad_ms)
    return SIN_ALERTAS if resultado.failsafe else resultado


def clasificar_ruido_aislado(
    matriz: object, antiguedad_ms: object
) -> ResultadoClasificacion:
    """Variante 5: activa una zona por cualquier celda cercana."""
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
        activas[nombre] = any(valor >= 176 for valor in valores)
    return ResultadoClasificacion(
        activas["arriba"],
        activas["abajo"],
        activas["izquierda"],
        activas["derecha"],
        activas["centro"],
        False,
    )


VARIANTES: dict[str, Clasificador] = {
    "umbral_estricto": clasificar_umbral_estricto,
    "antiguedad_estricta": clasificar_antiguedad_estricta,
    "salida_exclusiva": clasificar_exclusiva,
    "sin_failsafe": clasificar_sin_failsafe,
    "ruido_aislado": clasificar_ruido_aislado,
}
