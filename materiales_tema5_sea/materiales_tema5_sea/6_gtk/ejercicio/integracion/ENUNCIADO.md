# Ampliación opcional S6-A3 — verificación de integración

En clase el profesor ejecuta los casos y el grupo anticipa oralmente los resultados y registra una matriz colectiva de evidencias. Las órdenes y contratos siguientes permiten practicar opcionalmente después, sin entrega obligatoria ni instalación exigida al alumnado.

Ejecuta y registra esperado, observado y resultado, indicando el programa y la
fuente utilizados. Los casos 1–4 y 6–7 se comprueban con la plantilla GTK de
S6-A2 y los CSV suministrados. En el caso 5, la pausa y reanudación del CSV
comprueban que no se consumen filas; para observar el salto del cursor hay que
observar la demostración del docente con la aplicación completa `odometro_gtk`,
ejecutada sin argumento CSV en una sesión X11 con `libxdo`. El ZIP incluye el
cliente común con los mismos callbacks pendientes de S6-A2; tras completarlos
puede construirse con CMake, sin recibir una solución adicional. En la práctica opcional, quien disponga de un equipo preparado
ejecuta su plantilla CSV completada y registra
por separado lo observado en la demostración X11; no necesita construir otro
programa ni instalar herramientas.

1. primera muestra distinta del origen;
2. cursor inmóvil;
3. `(100,100) → (103,104) → (100,100)`;
4. puesta a cero sin rebobinar y repetición del CSV desde el principio;
5. pausa y reanudación con CSV; además, en X11, pausa, movimiento del cursor y reanudación sin sumar el salto;
6. pulsaciones repetidas de iniciar/pausar;
7. cierre limpio.

`S6-A3-01`: formula una conclusión que distinga los casos automatizados de la interacción GTK comprobada manualmente. Identifica como pendiente el caso X11 si el docente no puede mostrarlo; no atribuyas a la plantilla CSV una adquisición del cursor. Tiempo orientativo de práctica opcional: 15 minutos. Dificultad: media.
