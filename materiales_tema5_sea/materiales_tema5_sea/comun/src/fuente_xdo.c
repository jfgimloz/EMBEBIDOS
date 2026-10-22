#include "fuente_posicion.h"

#include <stdio.h>
#include <stdlib.h>

#ifdef HAVE_XDO
#include <xdo.h>

typedef struct {
    xdo_t *xdo;
} EstadoXdo;

static bool xdo_leer(FuentePosicion *fuente, int *x, int *y)
{
    EstadoXdo *estado = fuente->estado;
    int pantalla = 0;
    if (xdo_get_mouse_location(estado->xdo, x, y, &pantalla) != XDO_SUCCESS) {
        snprintf(fuente->error, sizeof fuente->error,
                 "libxdo no pudo consultar la posición");
        return false;
    }
    return true;
}

static void xdo_cerrar(FuentePosicion *fuente)
{
    EstadoXdo *estado = fuente->estado;
    if (estado != NULL) {
        xdo_free(estado->xdo);
        free(estado);
    }
}

FuentePosicion *fuente_xdo_abrir(void)
{
    FuentePosicion *fuente = calloc(1, sizeof *fuente);
    EstadoXdo *estado = calloc(1, sizeof *estado);
    if (fuente == NULL || estado == NULL) {
        free(fuente);
        free(estado);
        return NULL;
    }
    estado->xdo = xdo_new(NULL);
    if (estado->xdo == NULL) {
        free(fuente);
        free(estado);
        return NULL;
    }
    fuente->leer = xdo_leer;
    fuente->cerrar = xdo_cerrar;
    fuente->estado = estado;
    return fuente;
}
#else
FuentePosicion *fuente_xdo_abrir(void)
{
    return NULL;
}
#endif
