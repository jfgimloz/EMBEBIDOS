import os

import pytest

from variantes import VARIANTES
from clasificacion import clasificar_obstaculos


@pytest.fixture
def clasificador():
    nombre = os.environ.get("FOSSIGHT_VARIANTE")
    return VARIANTES.get(nombre, clasificar_obstaculos)
