from abc import ABC, abstractmethod

from src.resultado import ResultadoPrueba


class PruebaUniformidad(ABC):
    def validar_datos(self, valores: list[float]) -> None:
        if not valores:
            raise ValueError("La secuencia no puede estar vacia")

        if any(valor < 0 or valor >= 1 for valor in valores):
            raise ValueError("Todos los valores deben pertenecer a [0, 1)")

    @abstractmethod
    def evaluar(self, valores: list[float]) -> ResultadoPrueba:
        """Evalua si la secuencia es compatible con U(0, 1)."""
        raise NotImplementedError
