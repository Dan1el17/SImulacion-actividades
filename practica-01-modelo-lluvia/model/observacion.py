from dataclasses import dataclass


@dataclass(frozen=True)
class Observacion:
    hora: str
    h: float      # humedad normalizada (0..1)
    n: float      # nubosidad normalizada (0..1)
    temp: float   # °C


@dataclass(frozen=True)
class Resultado:
    observacion: Observacion
    tf: float
    indice: float
    estado: str