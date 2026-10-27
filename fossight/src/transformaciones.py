"""Transformaciones deterministas de proximidad relativa."""

from PIL import Image


def _es_gris(imagen: Image.Image) -> bool:
    return isinstance(imagen, Image.Image) and imagen.mode == "L"


def a_azul_rojo(proximidad: Image.Image) -> Image.Image | None:
    """Colorea 0 como azul lejano y 255 como rojo cercano."""
    if not _es_gris(proximidad):
        return None

    salida = Image.new("RGB", proximidad.size)
    salida.putdata([(valor, 0, 255 - valor) for valor in proximidad.getdata()])
    return salida


def a_blanco_negro(proximidad: Image.Image) -> Image.Image | None:
    """Convierte la proximidad: blanco cerca y negro lejos."""
    if not _es_gris(proximidad):
        return None

    return proximidad.copy()


def cuantizar_argus(intensidad: Image.Image) -> tuple[tuple[int, ...], ...] | None:
    """Reduce una imagen L a los 60 valores de la matriz simulada 6 x 10."""
    if not _es_gris(intensidad):
        return None

    reducida = intensidad.resize((10, 6), Image.Resampling.BOX)
    valores = tuple(int(valor) for valor in reducida.getdata())
    return tuple(valores[fila * 10 : (fila + 1) * 10] for fila in range(6))
