#define _POSIX_C_SOURCE 200809L

#include "fuente_posicion.h"

#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    FILE *archivo;
    unsigned long linea;
    char *texto;
    size_t capacidad;
} EstadoCsv;

static void saltar_espacios(const char **texto)
{
    while (isspace((unsigned char)**texto)) {
        (*texto)++;
    }
}

static bool entero_csv(const char **texto, int *resultado)
{
    const char *digito;
    char *fin;
    long valor;

    saltar_espacios(texto);
    digito = *texto;
    if (*digito == '+' || *digito == '-') digito++;
    if (*digito < '0' || *digito > '9') return false;
    errno = 0;
    valor = strtol(*texto, &fin, 10);
    if (errno != 0 || valor < INT_MIN || valor > INT_MAX) return false;
    *resultado = (int)valor;
    *texto = fin;
    saltar_espacios(texto);
    return true;
}

static bool fila_csv(const char *texto, int *x, int *y)
{
    if (!entero_csv(&texto, x) || *texto++ != ',') return false;
    return entero_csv(&texto, y) && *texto == '\0';
}

static bool csv_leer(FuentePosicion *fuente, int *x, int *y)
{
    EstadoCsv *estado = fuente->estado;
    ssize_t longitud;

    while ((longitud = getline(&estado->texto, &estado->capacidad, estado->archivo)) != -1) {
        const char *contenido;
        estado->linea++;
        if (longitud > 0 && estado->texto[longitud - 1] == '\n') {
            estado->texto[--longitud] = '\0';
        }
        if (longitud > 0 && estado->texto[longitud - 1] == '\r') {
            estado->texto[--longitud] = '\0';
        }
        contenido = estado->texto;
        saltar_espacios(&contenido);
        if (*contenido == '\0' || *contenido == '#') {
            continue;
        }
        if (estado->linea == 1 &&
            (strcmp(estado->texto, "x,y") == 0 || strcmp(estado->texto, "X,Y") == 0)) {
            continue;
        }
        if (fila_csv(contenido, x, y)) {
            return true;
        }
        snprintf(fuente->error, sizeof fuente->error,
                 "CSV inválido en la línea %lu", estado->linea);
        return false;
    }

    if (ferror(estado->archivo)) {
        snprintf(fuente->error, sizeof fuente->error, "error de lectura del CSV");
    }
    return false;
}

static void csv_cerrar(FuentePosicion *fuente)
{
    EstadoCsv *estado = fuente->estado;
    if (estado != NULL) {
        if (estado->archivo != NULL) {
            fclose(estado->archivo);
        }
        free(estado->texto);
        free(estado);
    }
}

FuentePosicion *fuente_csv_abrir(const char *ruta)
{
    FuentePosicion *fuente = calloc(1, sizeof *fuente);
    EstadoCsv *estado = calloc(1, sizeof *estado);

    if (fuente == NULL || estado == NULL) {
        free(fuente);
        free(estado);
        return NULL;
    }
    estado->archivo = fopen(ruta, "r");
    if (estado->archivo == NULL) {
        free(fuente);
        free(estado);
        return NULL;
    }
    fuente->leer = csv_leer;
    fuente->cerrar = csv_cerrar;
    fuente->estado = estado;
    return fuente;
}
