"""Perfiles reproducibles de avisos sonoros."""

from dataclasses import dataclass

from clasificacion import ResultadoClasificacion


@dataclass(frozen=True)
class PerfilSonoro:
    frecuencia_hz: int
    pulsos: int
    duracion_ms: int
    pausa_ms: int


PERFILES = {
    "arriba": PerfilSonoro(1200, 1, 180, 0),
    "abajo": PerfilSonoro(300, 1, 180, 0),
    "izquierda": PerfilSonoro(550, 1, 180, 0),
    "derecha": PerfilSonoro(950, 1, 180, 0),
    "centro": PerfilSonoro(750, 3, 100, 80),
}


def perfil_sonoro(zona: str) -> PerfilSonoro | None:
    """Devuelve el perfil del obstáculo o ``None`` si no debe sonar."""
    return PERFILES.get(zona)


def perfiles_sonoros(
    clasificacion: ResultadoClasificacion,
) -> tuple[PerfilSonoro, ...]:
    """Devuelve todos los perfiles activos; ``failsafe`` siempre es silencioso."""
    if clasificacion.failsafe:
        return ()
    return tuple(
        PERFILES[zona]
        for zona in PERFILES
        if getattr(clasificacion, zona)
    )
