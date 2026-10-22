#include "fuente_posicion.h"
#include "odometro.h"

#include <gtk/gtk.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>

typedef struct {
    Odometro odometro;
    FuentePosicion *fuente;
    GtkWidget *coordenadas;
    GtkWidget *muestras;
    GtkWidget *distancia;
    GtkWidget *estado;
    GtkWidget *boton_inicio;
    guint temporizador;
    guint intervalo_ms;
    const char *ruta_csv;
    bool agotada;
} Aplicacion;

static void actualizar_indicadores(Aplicacion *app, int x, int y)
{
    char texto[96];
    g_snprintf(texto, sizeof texto, "Coordenadas: (%d, %d)", x, y);
    gtk_label_set_text(GTK_LABEL(app->coordenadas), texto);
    g_snprintf(texto, sizeof texto, "Muestras válidas: %lu", app->odometro.muestras);
    gtk_label_set_text(GTK_LABEL(app->muestras), texto);
    g_snprintf(texto, sizeof texto, "Recorrido estimado: %.2f unidades",
               app->odometro.distancia);
    gtk_label_set_text(GTK_LABEL(app->distancia), texto);
}

static gboolean adquirir_una_muestra(gpointer datos)
{
    Aplicacion *app = datos;
    int x;
    int y;

    if (!fuente_posicion_leer(app->fuente, &x, &y)) {
        const char *error = fuente_posicion_error(app->fuente);
        gtk_label_set_text(GTK_LABEL(app->estado),
                           error[0] == '\0' ? "Fin de los datos" : error);
        app->temporizador = 0;
        app->agotada = true;
        gtk_widget_set_sensitive(app->boton_inicio, FALSE);
        gtk_button_set_label(GTK_BUTTON(app->boton_inicio), "Iniciar");
        odometro_pausar(&app->odometro);
        return G_SOURCE_REMOVE;
    }
    odometro_actualizar(&app->odometro, x, y);
    printf("x=%d y=%d muestras=%lu distancia=%.3f\n",
           x, y, app->odometro.muestras, app->odometro.distancia);
    fflush(stdout);
    actualizar_indicadores(app, x, y);
    gtk_label_set_text(GTK_LABEL(app->estado), "Adquiriendo");
    return G_SOURCE_CONTINUE;
}

#include "callbacks.c"

/* Repetir vuelve a abrir el CSV; poner a cero conserva la posición de lectura. */
static void repetir_csv(GtkButton *boton, gpointer datos)
{
    Aplicacion *app = datos;
    FuentePosicion *nueva = fuente_csv_abrir(app->ruta_csv);
    if (nueva == NULL) {
        gtk_label_set_text(GTK_LABEL(app->estado), "No se pudo volver a abrir el CSV");
        return;
    }
    if (app->temporizador != 0) {
        g_source_remove(app->temporizador);
        app->temporizador = 0;
    }
    fuente_posicion_cerrar(app->fuente);
    app->fuente = nueva;
    app->agotada = false;
    reiniciar(boton, app);
    gtk_widget_set_sensitive(app->boton_inicio, TRUE);
    gtk_button_set_label(GTK_BUTTON(app->boton_inicio), "Iniciar");
}

static void cerrar(GtkWidget *ventana, gpointer datos)
{
    Aplicacion *app = datos;
    (void)ventana;
    if (app->temporizador != 0) {
        g_source_remove(app->temporizador);
    }
    fuente_posicion_cerrar(app->fuente);
    gtk_main_quit();
}

int main(int argc, char **argv)
{
    Aplicacion app = {.intervalo_ms = 100};
    GtkWidget *ventana;
    GtkWidget *caja;
    GtkWidget *controles;
    GtkWidget *reinicio;

    /* Sintaxis pequeña para el aula: [CSV [intervalo_ms]]. */
    gtk_init(&argc, &argv);
    if (argc > 3) {
        g_printerr("Uso: %s [CSV [intervalo_ms]]\n", argv[0]);
        return 2;
    }
    if (argc == 3) {
        char *fin;
        errno = 0;
        unsigned long valor = strtoul(argv[2], &fin, 10);
        if (errno != 0 || fin == argv[2] || *fin != '\0' ||
            argv[2][0] == '-' || valor == 0 || valor > G_MAXUINT) {
            g_printerr("El intervalo debe ser un entero positivo en milisegundos.\n");
            return 2;
        }
        app.intervalo_ms = (guint)valor;
    }
    app.ruta_csv = argc >= 2 ? argv[1] : NULL;
    app.fuente = app.ruta_csv != NULL ? fuente_csv_abrir(app.ruta_csv) : fuente_xdo_abrir();
    if (app.fuente == NULL) {
        g_printerr("No se pudo abrir la fuente. Pase un CSV o instale libxdo y use X11.\n");
        return 2;
    }
    odometro_inicializar(&app.odometro);

    ventana = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(ventana), "Odómetro del cursor");
    gtk_window_set_default_size(GTK_WINDOW(ventana), 420, 240);
    gtk_container_set_border_width(GTK_CONTAINER(ventana), 18);

    caja = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_container_add(GTK_CONTAINER(ventana), caja);
    app.coordenadas = gtk_label_new("Coordenadas: —");
    app.muestras = gtk_label_new("Muestras válidas: 0");
    app.distancia = gtk_label_new("Recorrido estimado: 0.00 unidades");
    app.estado = gtk_label_new("Preparado");
    gtk_box_pack_start(GTK_BOX(caja), app.coordenadas, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(caja), app.muestras, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(caja), app.distancia, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(caja), app.estado, FALSE, FALSE, 0);

    controles = gtk_button_box_new(GTK_ORIENTATION_HORIZONTAL);
    app.boton_inicio = gtk_button_new_with_label("Iniciar");
    reinicio = gtk_button_new_with_label("Poner a cero");
    gtk_container_add(GTK_CONTAINER(controles), app.boton_inicio);
    gtk_container_add(GTK_CONTAINER(controles), reinicio);
    if (app.ruta_csv != NULL) {
        GtkWidget *repetir = gtk_button_new_with_label("Repetir CSV");
        gtk_container_add(GTK_CONTAINER(controles), repetir);
        g_signal_connect(repetir, "clicked", G_CALLBACK(repetir_csv), &app);
    }
    gtk_box_pack_end(GTK_BOX(caja), controles, FALSE, FALSE, 0);

    g_signal_connect(app.boton_inicio, "clicked", G_CALLBACK(iniciar_pausar), &app);
    g_signal_connect(reinicio, "clicked", G_CALLBACK(reiniciar), &app);
    g_signal_connect(ventana, "destroy", G_CALLBACK(cerrar), &app);
    gtk_widget_show_all(ventana);
    gtk_main();
    return 0;
}
