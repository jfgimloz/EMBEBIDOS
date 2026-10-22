#include "fuente_posicion.h"

#include <stdlib.h>

bool fuente_posicion_leer(FuentePosicion *fuente, int *x, int *y)
{
    if (fuente == NULL || fuente->leer == NULL) {
        return false;
    }
    fuente->error[0] = '\0';
    return fuente->leer(fuente, x, y);
}

const char *fuente_posicion_error(const FuentePosicion *fuente)
{
    return fuente == NULL ? "fuente no inicializada" : fuente->error;
}

void fuente_posicion_cerrar(FuentePosicion *fuente)
{
    if (fuente == NULL) {
        return;
    }
    if (fuente->cerrar != NULL) {
        fuente->cerrar(fuente);
    }
    free(fuente);
}
