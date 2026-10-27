"""Adaptadores optativos para profundidad monocular local."""

from collections.abc import Callable, Mapping
from math import isfinite
from numbers import Real

from PIL import Image

NOMBRE_MODELO = "Intel/dpt-hybrid-midas"
MODELO_DPT = "dpt_hybrid_midas"
MODELO_DEPTH_ANYTHING = "depth_anything_v2_small"
NOMBRES_MODELO = {
    MODELO_DPT: "DPT / MiDaS Hybrid (490 MB)",
    MODELO_DEPTH_ANYTHING: "Depth Anything V2 Small (99 MB)",
}
REPOSITORIOS_MODELO = {
    MODELO_DPT: NOMBRE_MODELO,
    MODELO_DEPTH_ANYTHING: "depth-anything/Depth-Anything-V2-Small-hf",
}
COMANDOS_BASE_LINUX_MINT = """sudo apt install python3-venv python3-gi gir1.2-gtk-4.0 gir1.2-gstreamer-1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good
/usr/bin/python3 -m venv --system-site-packages fossight-gui-venv
fossight-gui-venv/bin/python -m pip install 'Pillow>=10,<12' 'torch>=2.5,<3' 'transformers>=4.45,<6'"""


def comandos_instalacion(modelo: str = MODELO_DPT) -> str:
    """Devuelve comandos Linux Mint para instalar y descargar un modelo."""
    try:
        repositorio = REPOSITORIOS_MODELO[modelo]
    except KeyError as error:
        raise ValueError(f"Modelo desconocido: {modelo}") from error
    return (
        f"{COMANDOS_BASE_LINUX_MINT}\n"
        "fossight-gui-venv/bin/python -c "
        f"'from transformers import pipeline; pipeline(\"depth-estimation\", "
        f"model=\"{repositorio}\")'"
    )


COMANDOS_INSTALACION_LINUX_MINT = comandos_instalacion()


class ModeloNoInstalado(RuntimeError):
    """El modelo o sus dependencias no están disponibles en el equipo."""


def estimar_proximidad(
    origen: Image.Image,
    cargar_modelo: Callable[[], Callable[[Image.Image], object]],
) -> Image.Image | None:
    """Normaliza una vez la salida numérica de un modelo ya instalado."""
    if not isinstance(origen, Image.Image):
        return None

    estimador = cargar_modelo()
    prediccion = estimador(origen.convert("RGB"))
    if not isinstance(prediccion, Mapping) or "predicted_depth" not in prediccion:
        return None

    return _normalizar_predicted_depth(prediccion["predicted_depth"])


def _normalizar_predicted_depth(predicted_depth: object) -> Image.Image | None:
    """Convierte por protocolo una matriz numérica en proximidad ``L``."""
    valores = predicted_depth
    for metodo in ("detach", "cpu"):
        operacion = getattr(valores, metodo, None)
        if callable(operacion):
            valores = operacion()
    a_lista = getattr(valores, "tolist", None)
    if callable(a_lista):
        valores = a_lista()

    while (
        isinstance(valores, (list, tuple))
        and len(valores) == 1
        and isinstance(valores[0], (list, tuple))
        and valores[0]
        and isinstance(valores[0][0], (list, tuple))
    ):
        valores = valores[0]

    if not isinstance(valores, (list, tuple)) or not valores:
        return None
    if not all(isinstance(fila, (list, tuple)) and fila for fila in valores):
        return None
    anchura = len(valores[0])
    if not all(len(fila) == anchura for fila in valores):
        return None

    planos = [valor for fila in valores for valor in fila]
    if not all(
        isinstance(valor, Real)
        and not isinstance(valor, bool)
        and isfinite(float(valor))
        for valor in planos
    ):
        return None

    minimo = min(float(valor) for valor in planos)
    maximo = max(float(valor) for valor in planos)
    if minimo == maximo:
        pixeles = [0] * len(planos)
    else:
        escala = 255 / (maximo - minimo)
        pixeles = [round((float(valor) - minimo) * escala) for valor in planos]

    salida = Image.new("L", (anchura, len(valores)))
    salida.putdata(pixeles)
    return salida


def cargar_modelo(modelo: str = MODELO_DPT) -> Callable[[Image.Image], object]:
    """Carga el modelo seleccionado desde la caché local, sin descargarlo."""
    try:
        repositorio = REPOSITORIOS_MODELO[modelo]
    except KeyError as error:
        raise ValueError(f"Modelo desconocido: {modelo}") from error
    try:
        from huggingface_hub import snapshot_download
        from transformers import pipeline
    except ImportError as error:
        raise ModeloNoInstalado("Faltan torch o transformers.") from error

    try:
        directorio_modelo = snapshot_download(
            repo_id=repositorio,
            local_files_only=True,
        )
    except Exception as error:
        raise ModeloNoInstalado(
            f"El modelo {repositorio} no está descargado localmente."
        ) from error

    estimador = pipeline("depth-estimation", model=directorio_modelo)
    return lambda imagen: estimador(imagen)


def cargar_dpt() -> Callable[[Image.Image], object]:
    """Compatibilidad con el cargador DPT/MiDaS original."""
    return cargar_modelo(MODELO_DPT)
