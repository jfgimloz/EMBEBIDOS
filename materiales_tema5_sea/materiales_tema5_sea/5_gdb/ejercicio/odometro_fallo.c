#include "odometro.h"

#include <math.h>
#include <stdio.h>

void odometro_inicializar(Odometro *odometro)
{
    /* TODO S6-A1-01: diagnosticar este estado antes de corregirlo. */
    *odometro = (Odometro){.referencia_valida = true};
}

double odometro_actualizar(Odometro *odometro, int x, int y)
{
    double incremento = 0.0;

    odometro->muestras++;
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

int main(void)
{
    Odometro odometro;
    odometro_inicializar(&odometro);
    odometro_actualizar(&odometro, 100, 100);
    printf("primera muestra=(100,100) distancia=%.3f\n", odometro.distancia);
    return 0;
}
