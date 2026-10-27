# Nota sobre `pyproject.toml`

`pyproject.toml` es un archivo de configuración escrito en TOML. TOML aporta
la sintaxis —tablas, claves, cadenas, listas, números y valores booleanos—,
pero el significado de cada clave lo define la herramienta que lee esa
sección. Por eso no basta con consultar la referencia general de TOML: también
hay que consultar la documentación de pytest, setuptools o del sistema de
empaquetado de Python, según la sección que se quiera modificar.

## Cómo se organiza este archivo

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "fossight"
version = "0.1.0"

[project.optional-dependencies]
dev = ["pytest>=8,<9"]

[tool.setuptools]
py-modules = [
    "audio",
    "avisos",
    "clasificacion",
    "gui",
    "modelo_opcional",
    "profundidad",
    "transformaciones",
    "variantes",
]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
python_files = ["*_test.py"]
python_functions = ["*_test"]
```

- `[build-system]` indica cómo se construye el paquete.
- `[project]` contiene los metadatos y dependencias principales del proyecto.
- `[project.optional-dependencies]` define grupos opcionales, como `dev`.
- `[tool.setuptools]` declara los módulos Python independientes que setuptools
  debe incluir desde `src`.
- `[tool.pytest.ini_options]` configura pytest. `testpaths` indica dónde buscar
  pruebas y `python_files` y `python_functions` determinan sus nombres.

La notación entre corchetes introduce una tabla. Los valores entre corchetes
son listas; las comillas delimitan cadenas; `true` y `false` son valores
booleanos; y `#` inicia un comentario fuera de una cadena.

## Relación con los comandos de pytest

Las barras invertidas de un comando como este pertenecen a Bash, no a TOML:

```bash
python3 -m pytest \
  tests/plantillas_aula/clasificacion_test.py \
  -k antiguedad_failsafe_test -v
```

Cada barra invertida debe ser el último carácter de su línea. Si el comando se
escribe en una sola línea, deben eliminarse:

```bash
python3 -m pytest tests/plantillas_aula/clasificacion_test.py -k antiguedad_failsafe_test -v
```

## Referencias que deben consultarse

1. [Especificación oficial de TOML](https://toml.io/en/v1.0.0): sintaxis y
   tipos de datos.
2. [Especificación de `pyproject.toml`](https://packaging.python.org/en/latest/specifications/pyproject-toml/):
   estructura estándar de proyectos Python, `build-system` y `project`.
3. [Configuración de pytest](https://docs.pytest.org/en/stable/reference/customize.html):
   claves válidas dentro de `[tool.pytest.ini_options]`.
4. [Configuración de módulos y paquetes en setuptools](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html):
   configuración de `[tool.setuptools]`.

Con la restricción actual `pytest>=8,<9`, la configuración de pytest debe
mantenerse en `[tool.pytest.ini_options]`. No se debe inventar una clave TOML
ni trasladarla desde otra herramienta sin comprobar antes su documentación.
