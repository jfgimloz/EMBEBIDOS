from clasificacion import ResultadoClasificacion


def caso_discriminante_ruido_aislado_test(clasificador):
    matriz = [[0] * 10 for _ in range(6)]
    matriz[2][3] = 176
    matriz = tuple(tuple(fila) for fila in matriz)

    esperado = ResultadoClasificacion(False, False, False, False, False, False)
    assert clasificador(matriz, 120) == esperado
