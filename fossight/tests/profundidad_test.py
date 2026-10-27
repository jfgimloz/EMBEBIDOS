from PIL import Image

from profundidad import normalizar_proximidad


def normalizar_proximidad_convierte_el_mas_cercano_en_255_test():
    origen = Image.frombytes("L", (2, 1), bytes([10, 30]))

    resultado = normalizar_proximidad(origen)

    assert list(resultado.getdata()) == [0, 255]


def normalizar_proximidad_rechaza_una_imagen_que_no_es_gris_test():
    origen = Image.new("RGB", (1, 1), (0, 0, 0))

    assert normalizar_proximidad(origen) is None
