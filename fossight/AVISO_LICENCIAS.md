# Aviso de licencias

No se ha localizado una licencia global verificable en el repositorio fuente.
Por tanto, este desarrollo no presupone ni concede una licencia adicional
sobre su código: conserva los derechos de sus titulares. Solicita al
responsable del material las condiciones de reutilización antes de
redistribuirlo.

## Algoritmos opcionales de profundidad

La GUI puede usar, de forma opcional, modelos externos para obtener un mapa de
profundidad monocular a partir del PNG RAW. El desarrollo no incluye sus pesos
ni los descarga automáticamente; solo conserva los identificadores y el
adaptador de carga. 

| Modelo usado por FOSSight                                           | Licencia del checkpoint/modelo | Fuente oficial                                                                                                      |
| ------------------------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| `Intel/dpt-hybrid-midas` (DPT-Hybrid, también denominado MiDaS 3.0) | Apache License 2.0             | [model card de Intel en Hugging Face](https://huggingface.co/Intel/dpt-hybrid-midas)                                |
| `depth-anything/Depth-Anything-V2-Small-hf`                         | Apache License 2.0             | [model card de Depth Anything V2 en Hugging Face](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf) |

La licencia MIT del [repositorio fuente histórico de DPT](https://github.com/isl-org/DPT)
se refiere a su código y no sustituye la licencia Apache-2.0 declarada para el
checkpoint `Intel/dpt-hybrid-midas`. Análogamente, el repositorio de
[Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2) declara
Apache-2.0 para la variante Small; sus variantes Base, Large y Giant declaran
CC-BY-NC-4.0 y no son las usadas por este desarrollo. Depth Anything V2 usa una
arquitectura DPT con backbone DINOv2; el repositorio de [DINOv2](https://github.com/facebookresearch/dinov2)
declara Apache License 2.0 para su código y sus pesos.

`src/modelo_opcional.py` solo adapta la salida numérica
`predicted_depth` del modelo instalado y `src/profundidad.py` realiza
la normalización local del mapa. Esas piezas no incluyen los modelos ni
conceden una licencia sobre ellos. `torch`, `transformers`,
`huggingface_hub` y Pillow son dependencias de ejecución independientes y
conservan sus propias licencias.
