"""Normalización de mapas de profundidad relativa."""

from PIL import Image


def normalizar_proximidad(origen: Image.Image) -> Image.Image | None:
    """Escala una imagen L: 0 representa lejos y 255 representa cerca."""
    if not isinstance(origen, Image.Image) or origen.mode != "L":
        return None

    minimo, maximo = origen.getextrema()
    if minimo == maximo:
        return Image.new("L", origen.size, 0)

    escala = 255 / (maximo - minimo)
    return origen.point(lambda valor: round((valor - minimo) * escala))
