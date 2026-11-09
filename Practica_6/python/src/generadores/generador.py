from abc import ABC, abstractmethod


class Generador(ABC):
    @abstractmethod
    def siguiente(self) -> float:
        """Devuelve el siguiente numero generado."""
        raise NotImplementedError

    def generar(self, cantidad: int) -> list[float]:
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

        return [self.siguiente() for _ in range(cantidad)]
