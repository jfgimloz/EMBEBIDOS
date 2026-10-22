#include <gtk/gtk.h>

int main(int argc, char **argv)
{
    gtk_init(&argc, &argv);
    GtkWidget *ventana = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(ventana), "2. Botón sin acción");
    gtk_container_set_border_width(GTK_CONTAINER(ventana), 20);
    g_signal_connect(ventana, "destroy", G_CALLBACK(gtk_main_quit), NULL);
    GtkWidget *boton = gtk_button_new_with_label("Pulsar");
    gtk_container_add(GTK_CONTAINER(ventana), boton);
    gtk_widget_show_all(ventana);
    gtk_main();
    return 0;
}
