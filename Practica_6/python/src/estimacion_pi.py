import hashlib
import struct
import time
from dataclasses import dataclass

from src.generadores.lcg import LCG


@dataclass(frozen=True)
class ResultadoPi:
    cantidad_puntos: int
    puntos_dentro: int
    pi_estimado: float
    sha256_secuencia: str
    tiempo_segundos: float


def estimar_pi(generador: LCG, cantidad_puntos: int) -> ResultadoPi:
    if cantidad_puntos <= 0:
        raise ValueError("La cantidad de puntos debe ser mayor que cero")

    inicio = time.perf_counter()
    puntos_dentro = 0
    resumen = hashlib.sha256()

    for _ in range(cantidad_puntos):
        x_entero = generador.siguiente_entero()
        y_entero = generador.siguiente_entero()
        resumen.update(struct.pack(">QQ", x_entero, y_entero))

        x = x_entero / generador.modulo
        y = y_entero / generador.modulo
        if x * x + y * y <= 1:
            puntos_dentro += 1

    tiempo = time.perf_counter() - inicio
    return ResultadoPi(
        cantidad_puntos=cantidad_puntos,
        puntos_dentro=puntos_dentro,
        pi_estimado=4 * puntos_dentro / cantidad_puntos,
        sha256_secuencia=resumen.hexdigest(),
        tiempo_segundos=tiempo,
    )
