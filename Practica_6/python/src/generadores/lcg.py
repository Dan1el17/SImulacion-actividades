from src.generadores.generador import Generador


class LCG(Generador):
    def __init__(
        self,
        semilla: int,
        multiplicador: int,
        incremento: int,
        modulo: int
    ):
        if modulo <= 0:
            raise ValueError("El módulo debe ser mayor que cero")

        if not 0 <= semilla < modulo:
            raise ValueError("La semilla debe estar entre 0 y módulo - 1")

        if not 0 <= multiplicador < modulo:
            raise ValueError("El multiplicador debe estar entre 0 y módulo - 1")

        if not 0 <= incremento < modulo:
            raise ValueError("El incremento debe estar entre 0 y módulo - 1")

        self._estado = semilla
        self._multiplicador = multiplicador
        self._incremento = incremento
        self._modulo = modulo

    def siguiente(self) -> float:
        self._estado = (
            self._multiplicador * self._estado + self._incremento
        ) % self._modulo

        return self._estado / self._modulo