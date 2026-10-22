#include "odometro.h"

#include <math.h>

double odometro_actualizar(Odometro *odometro, int x, int y)
{
    double incremento = 0.0;

    odometro->muestras++;
    /* La primera muestra (también tras una pausa) no tiene tramo previo. */
    if (odometro->referencia_valida) {
        incremento = hypot((double)x - odometro->x_anterior,
                           (double)y - odometro->y_anterior);
        odometro->distancia += incremento;
    }

    odometro->x_anterior = x;
    odometro->y_anterior = y;
    odometro->referencia_valida = true;
    return incremento;
}
