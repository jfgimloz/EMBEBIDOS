/* Ventana y adquisición suministradas en odometro_gtk.c. Completar solo aquí. */
static void iniciar_pausar(GtkButton *boton, gpointer datos)
{
    Aplicacion *app = datos;
    (void)boton;
    if (app->temporizador != 0) {
        /* TODO S6-A2-01: retirar temporizador, invalidar referencia y actualizar UI. */
        return;
    }
    if (app->agotada) return;
    (void)adquirir_una_muestra; /* Callback suministrado para el temporizador. */
    /* TODO S6-A2-02: registrar un único temporizador y actualizar UI. */
}

static void reiniciar(GtkButton *boton, gpointer datos)
{
    Aplicacion *app = datos;
    (void)boton;
    (void)app;
    /* TODO S6-A2-03: poner núcleo y etiquetas a cero, conservando el temporizador. */
}
