# Ampliación opcional S6-A2 — callbacks y estado GTK

Esta práctica se conserva para después de la clase, si dispone de un equipo preparado. No exige instalación, ejecución ni entrega durante la sesión teórica: el profesor demuestra los controles y el grupo predice oralmente las transiciones.

La carpeta incluye `odometro_gtk.c` (ventana y adquisición), `callbacks.c`
(único archivo que se modifica) y `CMakeLists.txt`. La base de sesión 6 aporta
`comun/include`, `comun/src` y `datos`; conserve su posición relativa dentro del
paquete. No necesita montar código ni copiar las soluciones del profesor.

Desde esta carpeta:

```bash
cmake -S . -B /tmp/sea-actividad-gtk
cmake --build /tmp/sea-actividad-gtk
/tmp/sea-actividad-gtk/actividad_gtk ../../datos/trayectoria_larga.csv 1000
```

La plantilla compila y abre la ventana antes de resolver los TODO. Sus controles
no adquieren ni reinician hasta completarlos: esa es la intervención del ejercicio.
Esta construcción de práctica usa CSV; la aplicación común ofrece además X11.

1. `S6-A2-01`: al pausar, elimina el temporizador, guarda cero como identificador,
   invalida la referencia y actualiza botón y estado.
2. `S6-A2-02`: al reanudar, crea un temporizador solo cuando no existe y la fuente
   no está agotada; actualiza botón y estado.
3. `S6-A2-03`: «Poner a cero» reinicia núcleo y etiquetas, incluidas coordenadas,
   sin cambiar el temporizador ni la posición del CSV.

«Repetir CSV» ya está suministrado: detiene, reabre el archivo y utiliza el callback
de reinicio para dejarlo preparado. Después se pulsa «Iniciar». La trayectoria
larga da 21 muestras y distancia 100 sin interrupciones; la corta, 3 y 10.
Comprueba pausa, reanudación, puesta a cero, fin, repetición, clics alternos y cierre.
Pulsar varias veces alterna pausa y adquisición; nunca acumula temporizadores.
Si se practica en pareja, alternad la edición y comprobación: una persona trabaja pausa/reanudación
y la otra poner a cero/repetición; después intercambiad los papeles al probar.
Cada integrante debe explicar y mostrar una transición de estado. No hay otra entrega.
Tiempo orientativo de práctica opcional: 20 minutos. Dificultad: media. Integra después la lista de casos de S6-A3.
