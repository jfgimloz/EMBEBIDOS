#define _POSIX_C_SOURCE 200809L

#include "fuente_posicion.h"
#include "odometro.h"

#include <errno.h>
#include <getopt.h>
#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/stat.h>

typedef struct {
    const char *csv;
    const char *salida;
    unsigned long limite;
    long intervalo_ms;
    bool usar_x11;
    bool silencioso;
} Opciones;

static void uso(const char *programa)
{
    fprintf(stderr,
            "Uso: %s (--csv RUTA | --x11) [--intervalo-ms N] "
            "[--muestras N] [--salida RUTA] [--silencioso]\n",
            programa);
}

static bool entero_largo(const char *texto, long minimo, long *resultado)
{
    char *fin = NULL;
    long valor;
    errno = 0;
    valor = strtol(texto, &fin, 10);
    if (errno != 0 || fin == texto || *fin != '\0' || valor < minimo) {
        return false;
    }
    *resultado = valor;
    return true;
}

static bool leer_opciones(int argc, char **argv, Opciones *opciones)
{
    static const struct option largas[] = {
        {"csv", required_argument, NULL, 'c'},
        {"x11", no_argument, NULL, 'x'},
        {"intervalo-ms", required_argument, NULL, 'i'},
        {"muestras", required_argument, NULL, 'n'},
        {"salida", required_argument, NULL, 'o'},
        {"silencioso", no_argument, NULL, 'q'},
        {NULL, 0, NULL, 0}
    };
    int opcion;
    while ((opcion = getopt_long(argc, argv, "c:xi:n:o:q", largas, NULL)) != -1) {
        long valor;
        switch (opcion) {
        case 'c': opciones->csv = optarg; break;
        case 'x': opciones->usar_x11 = true; break;
        case 'i':
            if (!entero_largo(optarg, 0, &valor)) return false;
            opciones->intervalo_ms = valor;
            break;
        case 'n':
            if (!entero_largo(optarg, 1, &valor)) return false;
            opciones->limite = (unsigned long)valor;
            break;
        case 'o': opciones->salida = optarg; break;
        case 'q': opciones->silencioso = true; break;
        default: return false;
        }
    }
    return optind == argc && ((opciones->csv != NULL) != opciones->usar_x11);
}

static void esperar(long milisegundos)
{
    struct timespec pausa = {
        .tv_sec = milisegundos / 1000,
        .tv_nsec = (milisegundos % 1000) * 1000000L
    };
    while (nanosleep(&pausa, &pausa) == -1 && errno == EINTR) {
    }
}

int main(int argc, char **argv)
{
    Opciones opciones = {.intervalo_ms = 100};
    FuentePosicion *fuente;
    Odometro odometro;
    FILE *salida = NULL;
    bool error_salida = false;
    int resultado = 0;
    int x;
    int y;

    if (!leer_opciones(argc, argv, &opciones)) {
        uso(argv[0]);
        return 2;
    }
    fuente = opciones.csv != NULL ? fuente_csv_abrir(opciones.csv) : fuente_xdo_abrir();
    if (fuente == NULL) {
        fprintf(stderr, "No se pudo abrir la fuente de posiciones. "
                        "Compruebe la ruta, X11 y libxdo.\n");
        return 3;
    }
    if (opciones.csv != NULL && opciones.salida != NULL) {
        struct stat entrada, destino;
        if (stat(opciones.csv, &entrada) == 0 && stat(opciones.salida, &destino) == 0 &&
            entrada.st_dev == destino.st_dev && entrada.st_ino == destino.st_ino) {
            fprintf(stderr, "La entrada y la salida deben ser archivos distintos.\n");
            fuente_posicion_cerrar(fuente);
            return 4;
        }
    }
    if (opciones.salida != NULL) {
        salida = fopen(opciones.salida, "w");
        if (salida == NULL) {
            perror(opciones.salida);
            fuente_posicion_cerrar(fuente);
            return 4;
        }
        error_salida = fputs("indice,x,y,incremento,distancia\n", salida) == EOF;
    }

    odometro_inicializar(&odometro);
    while (!error_salida &&
           (opciones.limite == 0 || odometro.muestras < opciones.limite) &&
           fuente_posicion_leer(fuente, &x, &y)) {
        double incremento = odometro_actualizar(&odometro, x, y);
        if (!opciones.silencioso) {
            printf("x=%d y=%d muestras=%lu distancia=%.3f\n",
                   x, y, odometro.muestras, odometro.distancia);
        }
        if (salida != NULL) {
            error_salida = fprintf(salida, "%lu,%d,%d,%.6f,%.6f\n",
                                   odometro.muestras, x, y, incremento,
                                   odometro.distancia) < 0;
        }
        if (!error_salida && opciones.intervalo_ms > 0 &&
            (opciones.limite == 0 || odometro.muestras < opciones.limite)) {
            esperar(opciones.intervalo_ms);
        }
    }

    if (fuente_posicion_error(fuente)[0] != '\0') {
        fprintf(stderr, "%s\n", fuente_posicion_error(fuente));
        resultado = 5;
    }
    if (salida != NULL && fclose(salida) == EOF) error_salida = true;
    if (error_salida) {
        perror(opciones.salida);
        resultado = 4;
    }
    if (resultado == 0) {
        printf("muestras=%lu distancia=%.3f\n", odometro.muestras, odometro.distancia);
    }
    fuente_posicion_cerrar(fuente);
    return resultado;
}
