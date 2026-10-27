import pytest


LEJOS = tuple(tuple(0 for _ in range(10)) for _ in range(6))


def _cercania(celdas, valor=255):
    matriz = [list(fila) for fila in LEJOS]
    for fila, columna in celdas:
        matriz[fila][columna] = valor
    return tuple(tuple(fila) for fila in matriz)


MATRIZ_CENTRO = _cercania(
    [(fila, columna) for fila in (1, 2, 3) for columna in (3, 4, 5, 6)]
)


@pytest.mark.parametrize(
    ("matriz", "zona"),
    [
        pytest.param(LEJOS, None, id="sin-alertas"),
        pytest.param(MATRIZ_CENTRO, "centro", id="centro-nominal"),
    ],
)
def bateria_inicial_test(clasificador, matriz, zona):
    resultado = clasificador(matriz, 120)
    assert resultado.failsafe is False
    assert all(
        getattr(resultado, nombre) is (nombre == zona)
        for nombre in ("arriba", "abajo", "izquierda", "derecha", "centro")
    )
