#include <gtk/gtk.h>

int main(int argc, char **argv)
{
    gtk_init(&argc, &argv);
    GtkWidget *ventana = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(ventana), "1. Ventana y bucle");
    gtk_container_set_border_width(GTK_CONTAINER(ventana), 20);
    g_signal_connect(ventana, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    gtk_widget_show_all(ventana);
    gtk_main();
    return 0;
}
