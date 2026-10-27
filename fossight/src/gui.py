"""Interfaz GTK para explorar una cadena visual de FOSSight."""

from io import BytesIO
from pathlib import Path

from PIL import Image

from audio import reproducir
from avisos import perfil_sonoro
from clasificacion import (
    FALLO_SEGURO,
    ResultadoClasificacion,
    clasificar_obstaculos,
)
from modelo_opcional import (
    MODELO_DPT,
    NOMBRES_MODELO,
    ModeloNoInstalado,
    cargar_modelo,
    comandos_instalacion,
    estimar_proximidad,
)
from transformaciones import a_azul_rojo, a_blanco_negro, cuantizar_argus

TITULO_APLICACION = "Demostrador del concepto de FOSSight"
CREDITO_AUTOR = "Javier Monreal Trigo, 2026 CC BY-NC-SA 4.0"
NOMBRE_ICONO = "fossight-eye-icon"
RUTA_ICONO = Path(__file__).resolve().parents[1] / "assets" / f"{NOMBRE_ICONO}.png"

NOMBRES_LED = {
    "arriba": "Arriba",
    "abajo": "Abajo",
    "izquierda": "Izquierda",
    "derecha": "Derecha",
    "centro": "Centro",
}
ZONAS_SONORAS = tuple(NOMBRES_LED)

POSICIONES_LED = {
    "arriba": (1, 0),
    "abajo": (1, 2),
    "centro": (1, 1),
    "izquierda": (0, 1),
    "derecha": (2, 1),
}

ORIGEN_MATRIZ_RAW_GRISES = "raw_grises"
ORIGEN_MATRIZ_PROFUNDIDAD_GRISES = "profundidad_grises"
NOMBRES_PNG_MATRIZ = {
    ORIGEN_MATRIZ_RAW_GRISES: "matriz_directa.png",
    ORIGEN_MATRIZ_PROFUNDIDAD_GRISES: "matriz_profundidad.png",
}
TAMANO_VISTA_IMAGEN = (300, 200)
ETAPAS_LAYOUT = (
    ("raw", "azul_rojo", "profundidad_grises"),
    ("raw_grises", "matriz", "leds"),
    (None, "opciones_matriz", None),
)


def profundidad_seleccionable(obtener_desde_raw: bool) -> bool:
    """Indica si debe poder elegirse un PNG de profundidad externo."""
    return not obtener_desde_raw


def carpeta_inicial_dialogo(
    ultimo_archivo: str | Path | None,
    carpeta_ejecucion: str | Path | None = None,
) -> Path:
    """Elige la carpeta inicial: último archivo válido o carpeta de ejecución."""
    if ultimo_archivo is not None:
        ruta = Path(ultimo_archivo).expanduser()
        carpeta = ruta if ruta.is_dir() else ruta.parent
        if carpeta.is_dir():
            return carpeta
    return (
        Path(carpeta_ejecucion).expanduser()
        if carpeta_ejecucion is not None
        else Path.cwd()
    )


def ruta_matriz_png(ruta_raw: str | Path, origen_matriz: str) -> Path:
    """Devuelve el PNG de matriz asociado al RAW y al origen elegido."""
    try:
        nombre = NOMBRES_PNG_MATRIZ[origen_matriz]
    except KeyError as error:
        raise ValueError(f"Origen de matriz desconocido: {origen_matriz}") from error
    return Path(ruta_raw).expanduser().parent / nombre


def cargar_matriz_png(
    ruta_raw: str | Path, origen_matriz: str
) -> Image.Image | None:
    """Carga la matriz precomputada del caso, si existe."""
    try:
        with Image.open(ruta_matriz_png(ruta_raw, origen_matriz)) as imagen:
            return imagen.convert("L")
    except (OSError, ValueError):
        return None


def texto_instrucciones_instalacion(mensaje: str, modelo: str = MODELO_DPT) -> str:
    """Compone el texto completo que se ofrece para copiar en el popup."""
    return (
        f"{mensaje}\n\nEn Linux Mint, ejecuta estos comandos desde la "
        f"carpeta del ejercicio:\n\n{comandos_instalacion(modelo)}"
    )


def procesar_etapas(
    proximidad: Image.Image,
    raw: Image.Image | None = None,
    origen_matriz: str = ORIGEN_MATRIZ_PROFUNDIDAD_GRISES,
) -> dict[str, object]:
    """Devuelve las salidas visibles y cuantiza el origen seleccionado."""
    if raw is None:
        raw = proximidad
    raw_grises = raw.convert("L")
    azul_rojo = a_azul_rojo(proximidad)
    blanco_negro = a_blanco_negro(proximidad)
    if origen_matriz == ORIGEN_MATRIZ_RAW_GRISES:
        origen = raw_grises
    elif origen_matriz == ORIGEN_MATRIZ_PROFUNDIDAD_GRISES:
        origen = blanco_negro
    else:
        raise ValueError(f"Origen de matriz desconocido: {origen_matriz}")
    return {
        "raw": raw.convert("RGB"),
        "proximidad": proximidad,
        "azul_rojo": azul_rojo,
        "blanco_negro": blanco_negro,
        "raw_grises": raw_grises,
        "matriz": cuantizar_argus(origen),
    }


def _a_textura(imagen: Image.Image):
    from gi.repository import GLib, Gdk

    datos = BytesIO()
    imagen.save(datos, format="PNG")
    contenido = GLib.Bytes.new(datos.getvalue())
    return Gdk.Texture.new_from_bytes(contenido)


def _matriz_a_imagen(matriz: tuple[tuple[int, ...], ...]) -> Image.Image:
    imagen = Image.new("L", (10, 6))
    imagen.putdata([valor for fila in matriz for valor in fila])
    return imagen.resize((500, 300), Image.Resampling.NEAREST)


def ajustar_matriz_a_vista(imagen: Image.Image) -> Image.Image:
    """Ajusta el PNG 6 × 10 a la misma caja visual que las demás imágenes."""
    return imagen.resize(TAMANO_VISTA_IMAGEN, Image.Resampling.NEAREST)


def matrices_desde_capas(capas: dict[str, object]) -> dict[str, Image.Image]:
    """Calcula las matrices únicamente desde las dos fuentes visibles."""
    matrices = {}
    for origen, nombre_capa in (
        (ORIGEN_MATRIZ_RAW_GRISES, "raw_grises"),
        (ORIGEN_MATRIZ_PROFUNDIDAD_GRISES, "blanco_negro"),
    ):
        matriz = cuantizar_argus(capas[nombre_capa])
        if matriz is None:
            raise ValueError(f"La capa {nombre_capa} no es una imagen L válida")
        matrices[origen] = _matriz_a_imagen(matriz)
    return matrices


def resultado_desde_imagen(
    imagen: Image.Image, antiguedad_ms: int
) -> ResultadoClasificacion | None:
    """Clasifica una imagen de matriz para mantener sincronizados LED y sonido."""
    matriz = cuantizar_argus(imagen)
    if matriz is None:
        return None
    return clasificar_obstaculos(matriz, antiguedad_ms)


def resultado_desde_matriz_visible(
    imagen: Image.Image, antiguedad_ms: int
) -> ResultadoClasificacion | None:
    """Clasifica exactamente la representación que se presenta en pantalla."""
    return resultado_desde_imagen(ajustar_matriz_a_vista(imagen), antiguedad_ms)


def texto_resultado(resultado: ResultadoClasificacion) -> str:
    """Resume varias alertas sin confundirlas con el estado ``failsafe``."""
    if resultado.failsafe:
        return "FAILSAFE"
    activas = [nombre for zona, nombre in NOMBRES_LED.items() if getattr(resultado, zona)]
    return f"OBSTÁCULOS: {', '.join(activas)}" if activas else "SIN AVISO"


def zonas_sonoras_seleccionadas(seleccionadas: dict[str, bool]) -> tuple[str, ...]:
    """Devuelve las zonas marcadas, conservando el orden de la interfaz."""
    return tuple(zona for zona in ZONAS_SONORAS if seleccionadas.get(zona, False))


def crear_aplicacion():
    """Crea la ventana GTK sin descargar modelos automáticamente."""
    import gi

    gi.require_version("Gtk", "4.0")
    from gi.repository import Gio, Gtk

    aplicacion = Gtk.Application(application_id="org.sea.fossight")

    def activar(app):
        app.hold()
        ventana = Gtk.ApplicationWindow(application=app, title=TITULO_APLICACION)
        tema_iconos = Gtk.IconTheme.get_for_display(ventana.get_display())
        tema_iconos.add_search_path(str(RUTA_ICONO.parent))
        ventana.set_icon_name(NOMBRE_ICONO)
        ventana.set_default_size(1280, 820)

        raiz = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        raiz.set_margin_top(18)
        raiz.set_margin_bottom(18)
        raiz.set_margin_start(18)
        raiz.set_margin_end(18)
        ventana.set_child(raiz)

        configuracion = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        configuracion.set_size_request(300, -1)
        raiz.append(configuracion)

        configuracion.append(Gtk.Label(label="Entrada y configuración", xalign=0))
        configuracion.append(Gtk.Label(label="PNG RAW", xalign=0))
        ruta_raw = Gtk.Entry(placeholder_text="Selecciona el PNG RAW")
        configuracion.append(ruta_raw)
        ultima_carpeta = {"ruta": None}
        boton_raw = Gtk.Button(label="Elegir PNG RAW")
        configuracion.append(boton_raw)
        usar_modelo = Gtk.CheckButton()
        etiqueta_modelo = Gtk.Label(
            label="Obtener profundidad desde el PNG RAW (requiere modelo instalado)",
            wrap=True,
            xalign=0,
        )
        usar_modelo.set_child(etiqueta_modelo)
        configuracion.append(usar_modelo)
        configuracion.append(Gtk.Label(label="Modelo de profundidad", xalign=0))
        modelos_disponibles = tuple(NOMBRES_MODELO)
        modelo_profundidad = Gtk.DropDown.new_from_strings(
            [NOMBRES_MODELO[modelo] for modelo in modelos_disponibles]
        )
        modelo_profundidad.set_sensitive(False)
        configuracion.append(modelo_profundidad)
        entrada_profundidad = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        entrada_profundidad.append(Gtk.Label(label="PNG de profundidad", xalign=0))
        ruta_profundidad = Gtk.Entry(placeholder_text="Selecciona el PNG de profundidad")
        entrada_profundidad.append(ruta_profundidad)
        boton_profundidad = Gtk.Button(label="Elegir PNG de profundidad")
        entrada_profundidad.append(boton_profundidad)
        configuracion.append(entrada_profundidad)
        antiguedad = Gtk.SpinButton.new_with_range(0, 5_000, 1)
        antiguedad.set_value(120)
        configuracion.append(Gtk.Label(label="Antigüedad de la imagen (ms)", xalign=0))
        configuracion.append(antiguedad)
        algoritmo = Gtk.DropDown.new_from_strings(["por_zonas_v1"])
        configuracion.append(Gtk.Label(label="Algoritmo", xalign=0))
        configuracion.append(algoritmo)
        boton_procesar = Gtk.Button(label="Procesar imagen")
        configuracion.append(boton_procesar)
        estado = Gtk.Label(
            label="Elige un PNG RAW y un PNG de profundidad para comenzar.",
            wrap=True,
            xalign=0,
        )
        configuracion.append(estado)

        etapas = Gtk.Grid(
            column_spacing=12,
            row_spacing=12,
            column_homogeneous=True,
            row_homogeneous=True,
            hexpand=True,
            vexpand=True,
        )
        columna_principal = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
            hexpand=True,
            vexpand=True,
        )
        raiz.append(columna_principal)
        columna_principal.append(etapas)
        vistas = {}

        def crear_vista(clave, titulo, columna, fila):
            caja = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                spacing=6,
                hexpand=True,
                vexpand=True,
            )
            caja.append(Gtk.Label(label=titulo, xalign=0, wrap=True))
            imagen = Gtk.Picture(
                hexpand=True,
                vexpand=True,
                content_fit=Gtk.ContentFit.CONTAIN,
            )
            imagen.set_size_request(*TAMANO_VISTA_IMAGEN)
            caja.append(imagen)
            etapas.attach(caja, columna, fila, 1, 1)
            vistas[clave] = imagen

        crear_vista("raw", "RAW", 0, 0)
        crear_vista(
            "azul_rojo", "Profundidad (azul lejano ↔ rojo cercano)", 1, 0
        )
        crear_vista(
            "blanco_negro", "Profundidad (blanco cerca ↔ negro lejos)",
            2,
            0,
        )
        crear_vista("raw_grises", "RAW convertido a escala de grises", 0, 1)
        crear_vista("matriz", "6 × 10 en escala de grises", 1, 1)
        imagen_matriz = vistas["matriz"]
        radio_profundidad = Gtk.CheckButton(label="Origen: profundidad_grises")
        radio_raw = Gtk.CheckButton(label="Origen: raw_grises")
        radio_raw.set_group(radio_profundidad)
        radio_profundidad.set_active(True)
        caja_radios = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        caja_radios.append(radio_profundidad)
        caja_radios.append(radio_raw)
        etapas.attach(caja_radios, 1, 2, 1, 1)
        matrices_calculadas = {}

        leds = Gtk.Grid(column_spacing=10, row_spacing=10, hexpand=True, vexpand=True)
        leds.set_column_homogeneous(True)
        leds.set_row_homogeneous(True)
        etiquetas_led = {}
        for zona, nombre in NOMBRES_LED.items():
            etiqueta = Gtk.Label(label=f"○ {nombre}")
            etiqueta.set_halign(Gtk.Align.CENTER)
            etiqueta.set_valign(Gtk.Align.CENTER)
            columna, fila = POSICIONES_LED[zona]
            leds.attach(etiqueta, columna, fila, 1, 1)
            etiquetas_led[zona] = etiqueta
        etapas.attach(leds, 2, 1, 1, 1)
        etiqueta_failsafe = Gtk.Label(label="● FAILSAFE")
        etapas.attach(etiqueta_failsafe, 2, 2, 1, 1)
        clasificacion_actual = {"valor": FALLO_SEGURO}

        fila_sonidos = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
            hexpand=True,
        )
        checkboxes_sonido = {}
        for zona in ZONAS_SONORAS:
            checkbox = Gtk.CheckButton(label=NOMBRES_LED[zona])
            checkboxes_sonido[zona] = checkbox
            fila_sonidos.append(checkbox)
        boton_emitir_sonidos = Gtk.Button(label="Emitir sonidos seleccionados")
        fila_sonidos.append(boton_emitir_sonidos)
        columna_principal.append(fila_sonidos)
        credito_autor = Gtk.Label(label=CREDITO_AUTOR, xalign=1, hexpand=True)
        credito_autor.set_halign(Gtk.Align.FILL)
        columna_principal.append(credito_autor)

        def actualizar_boton_sonidos(_=None):
            boton_emitir_sonidos.set_sensitive(
                not clasificacion_actual["valor"].failsafe
                and bool(
                    zonas_sonoras_seleccionadas(
                        {
                            zona: checkbox.get_active()
                            for zona, checkbox in checkboxes_sonido.items()
                        }
                    )
                )
            )

        for checkbox in checkboxes_sonido.values():
            checkbox.connect("toggled", actualizar_boton_sonidos)
        actualizar_boton_sonidos()

        def actualizar_leds(resultado):
            for zona, etiqueta in etiquetas_led.items():
                etiqueta.set_label(
                    f"{'●' if getattr(resultado, zona) else '○'} {NOMBRES_LED[zona]}"
                )
            etiqueta_failsafe.set_label(
                "● FAILSAFE" if resultado.failsafe else "○ FAILSAFE"
            )
            for checkbox in checkboxes_sonido.values():
                checkbox.set_sensitive(not resultado.failsafe)
            actualizar_boton_sonidos()

        actualizar_leds(FALLO_SEGURO)

        def origen_matriz_activo():
            return (
                ORIGEN_MATRIZ_RAW_GRISES
                if radio_raw.get_active()
                else ORIGEN_MATRIZ_PROFUNDIDAD_GRISES
            )

        def actualizar_vista_matriz(_=None):
            origen = origen_matriz_activo()
            imagen = matrices_calculadas.get(origen)
            if imagen is None:
                return

            imagen_matriz.set_paintable(_a_textura(ajustar_matriz_a_vista(imagen)))
            resultado = resultado_desde_matriz_visible(
                imagen, antiguedad.get_value_as_int()
            )
            if resultado is None:
                return
            clasificacion_actual["valor"] = resultado
            actualizar_leds(resultado)
            estado.set_label(texto_resultado(resultado))

        radio_profundidad.connect("toggled", actualizar_vista_matriz)
        radio_raw.connect("toggled", actualizar_vista_matriz)

        def cargar_archivo(entrada, titulo):
            dialogo = Gtk.FileDialog(title=titulo)
            carpeta = carpeta_inicial_dialogo(
                ultima_carpeta["ruta"], carpeta_ejecucion=Path.cwd()
            )
            dialogo.set_initial_folder(Gio.File.new_for_path(str(carpeta)))

            def elegido(dialogo_archivo, respuesta):
                try:
                    archivo = dialogo_archivo.open_finish(respuesta)
                    ruta = archivo.get_path()
                    if ruta is None:
                        return
                    entrada.set_text(ruta)
                    ultima_carpeta["ruta"] = Path(ruta).parent
                except Exception:
                    return

            dialogo.open(ventana, None, elegido)

        def actualizar_entrada_profundidad(_):
            activo = usar_modelo.get_active()
            entrada_profundidad.set_sensitive(
                profundidad_seleccionable(activo)
            )
            modelo_profundidad.set_sensitive(activo)

        def mostrar_instrucciones_instalacion(mensaje, modelo=MODELO_DPT):
            dialogo = Gtk.Dialog(
                transient_for=ventana,
                modal=True,
                title="Instala el modelo de profundidad antes de usar esta opción",
            )
            contenido = dialogo.get_content_area()
            contenido.set_spacing(10)
            texto = Gtk.TextView(
                editable=False,
                cursor_visible=True,
                monospace=True,
                wrap_mode=Gtk.WrapMode.WORD_CHAR,
                hexpand=True,
                vexpand=True,
            )
            texto.set_buffer(Gtk.TextBuffer())
            texto.get_buffer().set_text(
                texto_instrucciones_instalacion(mensaje, modelo=modelo)
            )
            texto.set_size_request(760, 300)
            contenido.append(texto)
            dialogo.add_button("Cerrar", Gtk.ResponseType.CLOSE)
            dialogo.connect("response", lambda dialogo, _: dialogo.destroy())
            dialogo.present()

        def mostrar_error(mensaje):
            estado.set_label(mensaje)
            clasificacion_actual["valor"] = FALLO_SEGURO
            actualizar_leds(FALLO_SEGURO)

        def procesar(_):
            try:
                original = Image.open(Path(ruta_raw.get_text())).convert("RGB")
            except (OSError, ValueError):
                mostrar_error("No se ha podido abrir un PNG RAW válido.")
                return

            try:
                if usar_modelo.get_active():
                    indice_modelo = modelo_profundidad.get_selected()
                    modelo = modelos_disponibles[indice_modelo]
                    proximidad = estimar_proximidad(
                        original, lambda: cargar_modelo(modelo)
                    )
                else:
                    modelo = MODELO_DPT
                    proximidad = Image.open(Path(ruta_profundidad.get_text())).convert("L")
                if proximidad is None:
                    mostrar_error("No se pudo obtener profundidad relativa.")
                    return
                origen_matriz = (
                    ORIGEN_MATRIZ_RAW_GRISES
                    if radio_raw.get_active()
                    else ORIGEN_MATRIZ_PROFUNDIDAD_GRISES
                )
                capas = procesar_etapas(proximidad, original, origen_matriz)
                matrices_calculadas.clear()
                matrices_calculadas.update(matrices_desde_capas(capas))
                for nombre, imagen in (
                    ("raw", capas["raw"]),
                    ("azul_rojo", capas["azul_rojo"]),
                    ("blanco_negro", capas["blanco_negro"]),
                    ("raw_grises", capas["raw_grises"]),
                ):
                    vistas[nombre].set_paintable(_a_textura(imagen))
                actualizar_vista_matriz()
            except ModeloNoInstalado as error:
                mostrar_error("El modelo de profundidad no está instalado.")
                mostrar_instrucciones_instalacion(str(error), modelo=modelo)
            except (OSError, ValueError):
                mostrar_error("No se ha podido abrir un PNG de profundidad válido.")
            except Exception as error:
                mostrar_error(f"No se pudo procesar la imagen: {error}")

        boton_raw.connect("clicked", lambda _: cargar_archivo(ruta_raw, "Selecciona un PNG RAW"))
        boton_profundidad.connect(
            "clicked",
            lambda _: cargar_archivo(ruta_profundidad, "Selecciona un PNG de profundidad"),
        )
        usar_modelo.connect("toggled", actualizar_entrada_profundidad)
        boton_procesar.connect("clicked", procesar)

        def emitir_sonidos_seleccionados(_):
            seleccionadas = {
                zona: checkbox.get_active()
                for zona, checkbox in checkboxes_sonido.items()
            }
            for zona in zonas_sonoras_seleccionadas(seleccionadas):
                reproducir(perfil_sonoro(zona))

        boton_emitir_sonidos.connect("clicked", emitir_sonidos_seleccionados)
        ventana.connect("close-request", lambda _: (app.release(), False)[1])
        ventana.present()

    aplicacion.connect("activate", activar)
    return aplicacion
