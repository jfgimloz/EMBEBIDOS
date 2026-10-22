#!/usr/bin/env bash
set -euo pipefail
# Tres posiciones, dos distintas: cada proceso tiene una entrada y una salida.
sort 1_bash/demo/posiciones.txt | uniq | wc -l
