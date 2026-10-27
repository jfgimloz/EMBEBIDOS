# Modelos opcionales de profundidad

La GUI funciona sin modelos con un PNG RAW y otro PNG de profundidad, como se
explica en `README.md`. Esta configuración es independiente y opcional.

## Modelos reales disponibles

- DPT / MiDaS Hybrid: `Intel/dpt-hybrid-midas`.
- Depth Anything V2 Small: `depth-anything/Depth-Anything-V2-Small-hf`.

El adaptador necesita `torch`, `transformers`, `huggingface_hub` y Pillow. En
Linux Mint, Ubuntu o Debian se puede crear un entorno con acceso a GTK así:

```text
sudo apt install python3-venv python3-gi gir1.2-gtk-4.0 gir1.2-gstreamer-1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good
/usr/bin/python3 -m venv --system-site-packages fossight-gui-venv
fossight-gui-venv/bin/python -m pip install 'Pillow>=10,<12' 'torch>=2.5,<3' 'transformers>=4.45,<6' 'huggingface_hub>=0.25,<1'
```

La caché predeterminada de Hugging Face está en `~/.cache/huggingface/hub`.
Puedes cambiarla con `HF_HUB_CACHE` o, de forma más general, con `HF_HOME`.

## Descarga manual

La aplicación no descarga pesos automáticamente al ejecutarse. `cargar_modelo` llama a
`snapshot_download(..., local_files_only=True)`: solo usa la caché local. La
descarga manual explícita de cada modelo se realiza una vez con uno de estos
comandos:

```text
fossight-gui-venv/bin/python -c 'from transformers import pipeline; pipeline("depth-estimation", model="Intel/dpt-hybrid-midas")'
fossight-gui-venv/bin/python -c 'from transformers import pipeline; pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf")'
```

## Comprobación sin red

Después de la descarga manual, comprueba la caché sin permitir acceso de red:

```text
HF_HUB_OFFLINE=1 PYTHONPATH=src fossight-gui-venv/bin/python -c 'from modelo_opcional import cargar_modelo, MODELO_DPT; cargar_modelo(MODELO_DPT); print("DPT disponible en caché")'
HF_HUB_OFFLINE=1 PYTHONPATH=src fossight-gui-venv/bin/python -c 'from modelo_opcional import cargar_modelo, MODELO_DEPTH_ANYTHING; cargar_modelo(MODELO_DEPTH_ANYTHING); print("Depth Anything disponible en caché")'
```

Los mapas obtenidos por estos modelos son de profundidad relativa, no métrica:
no deben interpretarse como distancias en metros sin una calibración independiente.

Solo entonces marca «Obtener profundidad desde el PNG RAW» y elige el modelo
en la lista de la GUI. Si no está en caché, la interfaz informa del problema;
no inicia una descarga automática.
