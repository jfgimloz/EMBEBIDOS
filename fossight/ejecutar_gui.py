import importlib.util
import os
import sys
from pathlib import Path

from gui import crear_aplicacion

RUTA_ENTORNO_GUI = (
    Path(__file__).resolve().parent / "fossight-gui-venv" / "bin" / "python"
)
DEPENDENCIAS_PROFUNDIDAD = ("torch", "transformers", "huggingface_hub")


def dependencias_profundidad_disponibles() -> bool:
    """Indica si el intérprete actual puede cargar modelos de profundidad."""
    return all(
        importlib.util.find_spec(modulo) is not None
        for modulo in DEPENDENCIAS_PROFUNDIDAD
    )


def interprete_alternativo(
    actual: Path, entorno_gui: Path, *, dependencias_disponibles: bool
) -> Path | None:
    """Devuelve el intérprete local de GUI si el actual no sirve para profundidad."""
    if dependencias_disponibles or not entorno_gui.is_file():
        return None
    # El binario de un venv puede ser un enlace al Python del sistema. Las
    # rutas de invocación siguen siendo distintas y determinan qué pyvenv.cfg
    # utiliza Python.
    if actual.absolute() == entorno_gui.absolute():
        return None
    return entorno_gui


def ejecutar():
    """Lanza la GUI con un intérprete que incluya las dependencias opcionales."""
    interprete = interprete_alternativo(
        Path(sys.executable),
        RUTA_ENTORNO_GUI,
        dependencias_disponibles=dependencias_profundidad_disponibles(),
    )
    if interprete is not None:
        os.execve(str(interprete), [str(interprete), *sys.argv], os.environ.copy())
    raise SystemExit(crear_aplicacion().run())


if __name__ == "__main__":
    ejecutar()
