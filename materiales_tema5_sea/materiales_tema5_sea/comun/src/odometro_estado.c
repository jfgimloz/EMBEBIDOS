#include "odometro.h"

void odometro_inicializar(Odometro *odometro)
{
    *odometro = (Odometro){0};
}

void odometro_pausar(Odometro *odometro)
{
    odometro->referencia_valida = false;
}

void odometro_reiniciar(Odometro *odometro)
{
    odometro_inicializar(odometro);
}
