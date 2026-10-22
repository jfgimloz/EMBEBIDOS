#!/usr/bin/env bash
sea_demo=local
export sea_demo
bash 1_bash/demo/cambiar.sh
printf 'Después de bash: %s\n' "$sea_demo"
# shellcheck disable=SC1091
source 1_bash/demo/cambiar.sh
printf 'Después de source: %s\n' "$sea_demo"
