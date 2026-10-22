#ifndef FUENTE_POSICION_H
#define FUENTE_POSICION_H

#include <stdbool.h>
#include <stddef.h>

typedef struct FuentePosicion FuentePosicion;

FuentePosicion *fuente_csv_abrir(const char *ruta);
FuentePosicion *fuente_xdo_abrir(void);
bool fuente_posicion_leer(FuentePosicion *fuente, int *x, int *y);
const char *fuente_posicion_error(const FuentePosicion *fuente);
void fuente_posicion_cerrar(FuentePosicion *fuente);

struct FuentePosicion {
    bool (*leer)(FuentePosicion *fuente, int *x, int *y);
    void (*cerrar)(FuentePosicion *fuente);
    void *estado;
    char error[192];
};

#endif
