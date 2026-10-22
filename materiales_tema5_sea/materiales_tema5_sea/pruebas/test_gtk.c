/* Ejercita los callbacks reales sobre widgets GTK; no captura el cursor. */
#define main aplicacion_principal
#include "../comun/src/odometro_gtk.c"
#undef main

static gboolean terminar(gpointer datos)
{
    Aplicacion *app = datos;
    cerrar(NULL, app);
    return G_SOURCE_REMOVE;
}

int main(int argc, char **argv)
{
    if (!gtk_init_check(&argc, &argv)) {
        g_print("OMITIDA: callbacks GTK requieren pantalla disponible.\n");
        return 77;
    }
    g_assert_cmpint(argc, ==, 2);
    Aplicacion app = {.intervalo_ms = 10, .ruta_csv = argv[1]};
    app.fuente = fuente_csv_abrir(app.ruta_csv);
    g_assert_nonnull(app.fuente);
    GtkWidget *ventana = gtk_offscreen_window_new();
    GtkWidget *caja = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_container_add(GTK_CONTAINER(ventana), caja);
    app.coordenadas = gtk_label_new("");
    app.muestras = gtk_label_new("");
    app.distancia = gtk_label_new("");
    app.estado = gtk_label_new("");
    app.boton_inicio = gtk_button_new_with_label("Iniciar");
    GtkWidget *widgets[] = {app.coordenadas, app.muestras, app.distancia,
                            app.estado, app.boton_inicio};
    for (unsigned i = 0; i < G_N_ELEMENTS(widgets); i++)
        gtk_container_add(GTK_CONTAINER(caja), widgets[i]);
    g_signal_connect(app.boton_inicio, "clicked", G_CALLBACK(iniciar_pausar), &app);

    /* Pausar elimina realmente la fuente; reanudar descarta el salto. */
    gtk_button_clicked(GTK_BUTTON(app.boton_inicio));
    guint fuente = app.temporizador;
    g_assert_cmpuint(fuente, !=, 0);
    adquirir_una_muestra(&app);
    gtk_button_clicked(GTK_BUTTON(app.boton_inicio));
    g_assert_cmpuint(app.temporizador, ==, 0);
    g_assert_null(g_main_context_find_source_by_id(NULL, fuente));
    gtk_button_clicked(GTK_BUTTON(app.boton_inicio));
    adquirir_una_muestra(&app);
    g_assert_cmpfloat(app.odometro.distancia, ==, 0.0);
    adquirir_una_muestra(&app);
    g_assert_cmpfloat(app.odometro.distancia, ==, 5.0);
    gtk_button_clicked(GTK_BUTTON(app.boton_inicio));

    /* Repetir deja preparado el mismo caso, desde su primera posición. */
    repetir_csv(NULL, &app);
    g_assert_cmpuint(app.odometro.muestras, ==, 0);
    g_assert_cmpuint(app.temporizador, ==, 0);
    g_assert_cmpstr(gtk_button_get_label(GTK_BUTTON(app.boton_inicio)), ==, "Iniciar");
    gtk_button_clicked(GTK_BUTTON(app.boton_inicio));
    fuente = app.temporizador;
    adquirir_una_muestra(&app);
    reiniciar(NULL, &app);
    g_assert_cmpuint(app.temporizador, ==, fuente);
    g_assert_cmpuint(app.odometro.muestras, ==, 0);
    g_assert_cmpstr(gtk_label_get_text(GTK_LABEL(app.coordenadas)), ==, "Coordenadas: —");
    repetir_csv(NULL, &app);
    g_assert_null(g_main_context_find_source_by_id(NULL, fuente));

    /* Clics alternos no acumulan temporizadores. */
    for (int i = 0; i < 10; i++) {
        gtk_button_clicked(GTK_BUTTON(app.boton_inicio));
        fuente = app.temporizador;
        gtk_button_clicked(GTK_BUTTON(app.boton_inicio));
        g_assert_null(g_main_context_find_source_by_id(NULL, fuente));
    }
    gtk_button_clicked(GTK_BUTTON(app.boton_inicio));
    fuente = app.temporizador;
    /* Ahora sí: consumir el CSV con el bucle real y su temporizador. */
    gint64 limite = g_get_monotonic_time() + G_TIME_SPAN_SECOND;
    while (app.temporizador != 0 && g_get_monotonic_time() < limite) {
        g_main_context_iteration(NULL, FALSE);
        g_usleep(1000);
    }
    g_assert_cmpuint(app.temporizador, ==, 0);
    g_assert_null(g_main_context_find_source_by_id(NULL, fuente));
    g_assert_true(app.agotada);
    g_assert_false(gtk_widget_get_sensitive(app.boton_inicio));
    g_assert_cmpfloat(app.odometro.distancia, ==, 10.0);
    reiniciar(NULL, &app);
    g_assert_true(app.agotada);
    repetir_csv(NULL, &app);
    g_assert_false(app.agotada);
    g_assert_true(gtk_widget_get_sensitive(app.boton_inicio));
    gtk_button_clicked(GTK_BUTTON(app.boton_inicio));
    fuente = app.temporizador;
    g_idle_add(terminar, &app);
    gtk_main();
    g_assert_null(g_main_context_find_source_by_id(NULL, fuente));
    gtk_widget_destroy(ventana);
    g_print("GTK: pausa, reinicio, repetición, fin, clics y cierre: OK\n");
    return 0;
}
