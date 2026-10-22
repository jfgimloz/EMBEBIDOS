#!/usr/bin/env bash
set -u
set -o pipefail
export LC_NUMERIC=C

intervalo_ms=100
limite=20
salida="muestras_bash.csv"
reproducir=""

uso() {
    printf 'Uso: %s [--intervalo-ms N] [--muestras N] [--salida CSV] [--reproducir CSV]\n' "$0" >&2
}

es_entero_positivo() {
    [[ $1 =~ ^[1-9][0-9]*$ ]]
}

while (($# > 0)); do
    case $1 in
        --intervalo-ms)
            (($# >= 2)) || { uso; exit 2; }
            es_entero_positivo "$2" || { printf 'Intervalo no válido: %s\n' "$2" >&2; exit 2; }
            intervalo_ms=$2
            shift 2
            ;;
        --muestras)
            (($# >= 2)) || { uso; exit 2; }
            es_entero_positivo "$2" || { printf 'Número de muestras no válido: %s\n' "$2" >&2; exit 2; }
            limite=$2
            shift 2
            ;;
        --salida)
            (($# >= 2)) || { uso; exit 2; }
            salida=$2
            shift 2
            ;;
        --reproducir)
            (($# >= 2)) || { uso; exit 2; }
            reproducir=$2
            shift 2
            ;;
        *) uso; exit 2 ;;
    esac
done

# -ef reconoce también enlaces al mismo archivo: comprobar antes de truncar.
if [[ -n $reproducir && $reproducir -ef $salida ]]; then
    printf 'La entrada y la salida deben ser archivos distintos.\n' >&2
    exit 3
fi

command -v bc >/dev/null || { printf 'Falta bc.\n' >&2; exit 4; }
contador=0
distancia=0
referencia_valida=0

registrar() {
    local x=$1 y=$2
    # La primera muestra fija la referencia; cada siguiente añade un tramo.
    # TODO S5-A1-01: comprobar si existe una posición anterior
        tramo=$(printf 'scale=12; sqrt((%s - %s)^2 + (%s - %s)^2)\n' \
            "$x" "$anterior_x" "$y" "$anterior_y" | bc -l) || exit 5
        [[ $tramo =~ ^([0-9]+(\.[0-9]*)?|\.[0-9]+)$ ]] || { printf 'Cálculo no válido.\n' >&2; exit 5; }
        distancia=0 # TODO S5-A1-02: acumular distancia + tramo con bc
        [[ $distancia =~ ^([0-9]+(\.[0-9]*)?|\.[0-9]+)$ ]] || { printf 'Cálculo no válido.\n' >&2; exit 5; }
    fi
    # TODO S5-A1-03: guardar x como referencia
    # TODO S5-A1-03: guardar y como referencia
    # shellcheck disable=SC2034
    referencia_valida=1
    contador=$((contador + 1))
    printf '%s,%s\n' "$x" "$y" >>"$salida" || exit 3
}

# Normalizar en base diez antes del cálculo; no convertir valores fuera de rango.
normalizar_entero_csv() {
    local signo digitos maximo=2147483647
    [[ $1 =~ ^([+-]?)([0-9]+)$ ]] || return 1
    signo=${BASH_REMATCH[1]}
    digitos=${BASH_REMATCH[2]}
    while [[ $digitos == 0* && ${#digitos} -gt 1 ]]; do digitos=${digitos#0}; done
    ((${#digitos} <= 10)) || return 1
    [[ $signo == - ]] && maximo=2147483648
    ((10#$digitos <= maximo)) || return 1
    valor_csv=$digitos
    [[ $signo == - && $digitos != 0 ]] && valor_csv=-$digitos
    return 0
}

reproducir_csv() {
    local linea numero_linea=0 campo_x campo_y
    while IFS= read -r linea || [[ -n $linea ]]; do
        numero_linea=$((numero_linea + 1))
        linea=${linea%$'\r'}
        [[ $numero_linea == 1 && ( $linea == x,y || $linea == X,Y ) ]] && continue
        [[ $linea =~ ^[[:space:]]*$ || $linea =~ ^[[:space:]]*# ]] && continue
        if [[ $linea =~ ^[[:space:]]*([+-]?[0-9]+)[[:space:]]*,[[:space:]]*([+-]?[0-9]+)[[:space:]]*$ ]]; then
            campo_x=${BASH_REMATCH[1]}
            campo_y=${BASH_REMATCH[2]}
            if normalizar_entero_csv "$campo_x"; then
                x=$valor_csv
                if normalizar_entero_csv "$campo_y"; then
                    y=$valor_csv
                    registrar "$x" "$y"
                    continue
                fi
            fi
        fi
        printf 'Fila CSV no válida en la línea %s: %s\n' "$numero_linea" "$linea" >&2
        exit 5
    done <&3
}

# Abrir la entrada y comprobar dependencias antes de escribir la cabecera.
if [[ -n $reproducir ]]; then
    [[ -f $reproducir && -r $reproducir ]] || { printf 'No se puede leer %s\n' "$reproducir" >&2; exit 3; }
    exec 3<"$reproducir" || exit 3
else
    [[ ${XDG_SESSION_TYPE:-x11} == x11 && -n ${DISPLAY:-} ]] || {
        printf 'La adquisición global requiere una sesión X11. Use --reproducir CSV.\n' >&2
        exit 4
    }
    command -v xdotool >/dev/null || { printf 'Falta xdotool.\n' >&2; exit 4; }
    intervalo_seg=$(printf 'scale=3; %s / 1000\n' "$intervalo_ms" | bc) || exit 5
    [[ $intervalo_seg =~ ^([0-9]+(\.[0-9]*)?|\.[0-9]+)$ ]] || { printf 'Intervalo calculado no válido.\n' >&2; exit 5; }
fi

printf 'x,y\n' >"$salida" || exit 3

if [[ -n $reproducir ]]; then
    reproducir_csv
    exec 3<&-
else
    for ((indice = 0; indice < limite; indice++)); do
        posicion=$(xdotool getmouselocation --shell) || exit 5
        [[ $posicion =~ (^|$'\n')X=(-?[0-9]+) ]] || exit 5
        x=${BASH_REMATCH[2]}
        [[ $posicion =~ (^|$'\n')Y=(-?[0-9]+) ]] || exit 5
        y=${BASH_REMATCH[2]}
        [[ $x =~ ^-?[0-9]+$ && $y =~ ^-?[0-9]+$ ]] || {
            printf 'xdotool devolvió coordenadas no válidas.\n' >&2
            exit 5
        }
        registrar "$x" "$y"
        if ((indice + 1 < limite)); then sleep "$intervalo_seg"; fi
    done
fi

printf 'muestras=%s distancia=%.3f\n' "$contador" "$distancia"
