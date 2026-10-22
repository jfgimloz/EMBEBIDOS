#include <gtk/gtk.h>
typedef struct {
    int cuenta;
    GtkWidget *etiqueta;
} Contexto;

static void contar(GtkButton *boton, gpointer datos)
{
    Contexto *contexto = datos;
    char texto[64];
    (void)boton;
    g_snprintf(texto, sizeof texto, "Pulsaciones: %d", ++contexto->cuenta);
    gtk_label_set_text(GTK_LABEL(contexto->etiqueta), texto);
}
int main(int argc, char **argv)
{
    gtk_init(&argc, &argv);
    GtkWidget *ventana = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(ventana), "4. Contexto explícito");
    gtk_container_set_border_width(GTK_CONTAINER(ventana), 20);
    g_signal_connect(ventana, "destroy", G_CALLBACK(gtk_main_quit), NULL);
    /* Vive hasta que termina gtk_main: el callback no recibe un puntero caducado. */
    Contexto contexto = {0};
    GtkWidget *caja = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    GtkWidget *boton = gtk_button_new_with_label("Pulsar");
    contexto.etiqueta = gtk_label_new("Pulsaciones: 0");
    gtk_container_add(GTK_CONTAINER(ventana), caja);
    gtk_container_add(GTK_CONTAINER(caja), contexto.etiqueta);
    gtk_container_add(GTK_CONTAINER(caja), boton);
    g_signal_connect(boton, "clicked", G_CALLBACK(contar), &contexto);
    gtk_widget_show_all(ventana);
    gtk_main();
    return 0;
}
