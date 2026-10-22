#ifndef ODOMETRO_H
#define ODOMETRO_H

#include <stdbool.h>

typedef struct {
    double distancia;
    unsigned long muestras;
    int x_anterior;
    int y_anterior;
    bool referencia_valida;
} Odometro;

void odometro_inicializar(Odometro *odometro);
double odometro_actualizar(Odometro *odometro, int x, int y);
void odometro_pausar(Odometro *odometro);
void odometro_reiniciar(Odometro *odometro);

#endif
