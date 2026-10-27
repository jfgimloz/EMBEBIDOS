"""Síntesis local de los perfiles de aviso."""

import math
import struct
import wave
from io import BytesIO

from avisos import PerfilSonoro

_CANALES_ACTIVOS = []


def generar_wav(
    perfil: PerfilSonoro | None, frecuencia_muestreo: int = 44_100
) -> bytes | None:
    """Genera un WAV mono de 16 bits sin depender del dispositivo de audio."""
    if perfil is None:
        return None

    datos = BytesIO()
    with wave.open(datos, "wb") as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(frecuencia_muestreo)
        for pulso in range(perfil.pulsos):
            numero_muestras = round(
                frecuencia_muestreo * perfil.duracion_ms / 1000
            )
            muestras = (
                struct.pack(
                    "<h",
                    round(
                        12_000
                        * math.sin(
                            2
                            * math.pi
                            * perfil.frecuencia_hz
                            * muestra
                            / frecuencia_muestreo
                        )
                    ),
                )
                for muestra in range(numero_muestras)
            )
            archivo.writeframes(b"".join(muestras))
            if pulso + 1 < perfil.pulsos:
                silencio = round(frecuencia_muestreo * perfil.pausa_ms / 1000)
                archivo.writeframes(b"\x00\x00" * silencio)
    return datos.getvalue()


def reproducir(perfil: PerfilSonoro | None) -> bool:
    """Reproduce el perfil mediante GStreamer y devuelve si inició el audio."""
    contenido = generar_wav(perfil)
    if contenido is None:
        return False

    import gi

    gi.require_version("Gst", "1.0")
    from gi.repository import Gst

    Gst.init(None)
    canal = Gst.parse_launch(
        "appsrc name=fuente format=time ! wavparse ! audioconvert ! "
        "audioresample ! autoaudiosink"
    )
    fuente = canal.get_by_name("fuente")
    fuente.set_property("caps", Gst.Caps.from_string("audio/x-wav"))
    fuente.emit("push-buffer", Gst.Buffer.new_wrapped(contenido))
    fuente.emit("end-of-stream")
    canal.set_state(Gst.State.PLAYING)
    _CANALES_ACTIVOS.append(canal)
    return True
