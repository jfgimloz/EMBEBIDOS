#include "odometro.h"

#include <math.h>
#include <stdio.h>

static int comprobaciones = 0;
static int fallos = 0;

static void comprobar(int condicion, const char *mensaje)
{
    comprobaciones++;
    if (!condicion) {
        fprintf(stderr, "FALLO: %s\n", mensaje);
        fallos++;
    }
}

static int casi_igual(double a, double b)
{
    return fabs(a - b) < 1e-9;
}

static void primera_muestra_no_suma(void)
{
    Odometro o;
    odometro_inicializar(&o);
    comprobar(casi_igual(odometro_actualizar(&o, 100, 100), 0.0),
              "la primera muestra debe devolver incremento cero");
    comprobar(casi_igual(o.distancia, 0.0),
              "la primera muestra distinta del origen no debe sumar");
    comprobar(o.muestras == 1, "la primera muestra debe contarse");
}

static void posicion_repetida_no_suma(void)
{
    Odometro o;
    odometro_inicializar(&o);
    odometro_actualizar(&o, 40, 20);
    odometro_actualizar(&o, 40, 20);
    comprobar(casi_igual(o.distancia, 0.0),
              "una posición repetida no debe incrementar la distancia");
    comprobar(o.muestras == 2, "las posiciones repetidas siguen siendo muestras válidas");
}

static void ida_y_vuelta_suma_diez(void)
{
    Odometro o;
    odometro_inicializar(&o);
    odometro_actualizar(&o, 100, 100);
    odometro_actualizar(&o, 103, 104);
    odometro_actualizar(&o, 100, 100);
    comprobar(casi_igual(o.distancia, 10.0),
              "la trayectoria 3-4-5 de ida y vuelta debe sumar 10");
    comprobar(o.muestras == 3, "la trayectoria debe contener tres muestras");
}

static void reiniciar_borra_estado_y_referencia(void)
{
    Odometro o;
    odometro_inicializar(&o);
    odometro_actualizar(&o, 1, 1);
    odometro_actualizar(&o, 4, 5);
    odometro_reiniciar(&o);
    comprobar(casi_igual(o.distancia, 0.0), "reiniciar debe borrar la distancia");
    comprobar(o.muestras == 0, "reiniciar debe borrar el contador");
    comprobar(!o.referencia_valida, "reiniciar debe invalidar la referencia");
    odometro_actualizar(&o, 50, 60);
    comprobar(casi_igual(o.distancia, 0.0),
              "la primera muestra tras reiniciar no debe sumar");
}

static void reanudar_no_suma_movimiento_en_pausa(void)
{
    Odometro o;
    odometro_inicializar(&o);
    odometro_actualizar(&o, 10, 10);
    odometro_actualizar(&o, 13, 14);
    odometro_pausar(&o);
    comprobar(!o.referencia_valida, "pausar debe invalidar la referencia");
    comprobar(casi_igual(odometro_actualizar(&o, 100, 100), 0.0),
              "reanudar debe establecer una referencia sin sumar");
    comprobar(casi_igual(o.distancia, 5.0),
              "el movimiento durante la pausa no debe añadirse");
}

int main(void)
{
    primera_muestra_no_suma();
    posicion_repetida_no_suma();
    ida_y_vuelta_suma_diez();
    reiniciar_borra_estado_y_referencia();
    reanudar_no_suma_movimiento_en_pausa();

    if (fallos != 0) {
        fprintf(stderr, "%d/%d comprobaciones fallaron\n", fallos, comprobaciones);
        return 1;
    }
    printf("5/5 casos del núcleo: OK (%d comprobaciones)\n", comprobaciones);
    return 0;
}
