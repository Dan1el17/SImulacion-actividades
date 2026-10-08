from abc import ABC, abstractmethod


class FactorTemperatura(ABC):
    @abstractmethod
    def calcular(self, temp: float) -> float:
        ...


class FactorLineal(FactorTemperatura):
    """1.00 hasta 10 °C, baja 0.05 por grado, mínimo 0.10 desde 28 °C."""

    def calcular(self, temp: float) -> float:
        return min(1.0, max(0.1, 1 - 0.05 * (temp - 10)))