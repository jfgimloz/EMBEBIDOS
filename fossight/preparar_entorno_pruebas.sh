#!/usr/bin/env bash
set -euo pipefail

directorio_script=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd -- "$directorio_script"

python3 -m venv .venv-pruebas
.venv-pruebas/bin/python -m pip install 'pytest>=8,<9' 'Pillow>=10,<12'
.venv-pruebas/bin/python -m pytest -p no:cacheprovider -v
