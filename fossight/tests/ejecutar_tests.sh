#!/usr/bin/env bash
set -euo pipefail

# Este lanzador permite repetir los comandos de pytest sin copiar y pegar
# rutas largas. La opción -t selecciona el escenario que se quiere ejecutar.

uso() {
    cat <<'EOF'
Uso: tests/plantillas_aula/ejecutar_tests.sh -t ESCENARIO [opciones]

Escenarios:
  antiguedad   Frontera 499/500/501 ms de clasificacion_test.py.
  nominal      Un caso nominal de clasificacion_test.py.
  bateria      Batería inicial parametrizada de bateria_inicial_test.py.
  discriminante Caso que distingue la variante ruido_aislado.
  recoger      Enumera los tests de clasificacion_test.py.
  todos        Ejecuta todas las plantillas de aula.

Opciones:
  -t ESCENARIO  Escenario que se quiere lanzar (obligatorio).
  -q            Salida compacta de pytest.
  -v            Salida detallada de pytest.
  -h            Muestra esta ayuda.

Ejemplos:
  ./tests/plantillas_aula/ejecutar_tests.sh -t antiguedad -q
  ./tests/plantillas_aula/ejecutar_tests.sh -t nominal -v
EOF
}

directorio_script=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ -f "$directorio_script/../pyproject.toml" ]]; then
    directorio_proyecto=$(CDPATH= cd -- "$directorio_script/.." && pwd)
    directorio_tests="$directorio_proyecto/tests"
else
    directorio_proyecto=$(CDPATH= cd -- "$directorio_script/../.." && pwd)
    directorio_tests="$directorio_proyecto/tests/plantillas_aula"
fi

python="$directorio_proyecto/.venv-pruebas/bin/python"
if [[ ! -x "$python" ]]; then
    printf 'No se encuentra el entorno virtual requerido:\n  %s\n' "$python" >&2
    exit 1
fi

escenario=''
opciones_pytest=('-p' 'no:cacheprovider')

while getopts ':t:qvh' opcion; do
    case "$opcion" in
        t) escenario="$OPTARG" ;;
        q) opciones_pytest+=('-q') ;;
        v) opciones_pytest+=('-v') ;;
        h)
            uso
            exit 0
            ;;
        :)
            printf 'La opción -%s necesita un argumento.\n\n' "$OPTARG" >&2
            uso >&2
            exit 2
            ;;
        \?)
            printf 'Opción no reconocida: -%s\n\n' "$OPTARG" >&2
            uso >&2
            exit 2
            ;;
    esac
done

if [[ -n "${!OPTIND-}" ]]; then
    printf 'No se esperaban argumentos posicionales: %s\n' "${!OPTIND}" >&2
    uso >&2
    exit 2
fi

case "$escenario" in
    antiguedad)
        objetivo="$directorio_tests/clasificacion_test.py"
        opciones_pytest+=('-k' 'antiguedad_failsafe_test')
        ;;
    nominal)
        objetivo="$directorio_tests/clasificacion_test.py::arriba_activa_solo_su_alerta_test"
        ;;
    bateria)
        objetivo="$directorio_tests/bateria_inicial_test.py"
        ;;
    discriminante)
        objetivo="$directorio_tests/ruido_aislado_test.py"
        ;;
    recoger)
        objetivo="$directorio_tests/clasificacion_test.py"
        opciones_pytest+=('--collect-only')
        ;;
    todos)
        objetivo="$directorio_tests"
        ;;
    '')
        printf 'Falta indicar un escenario con -t.\n\n' >&2
        uso >&2
        exit 2
        ;;
    *)
        printf 'Escenario no reconocido: %s\n\n' "$escenario" >&2
        uso >&2
        exit 2
        ;;
esac

cd -- "$directorio_proyecto"
exec "$python" -m pytest "${opciones_pytest[@]}" "$objetivo"
