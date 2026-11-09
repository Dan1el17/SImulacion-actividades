from dataclasses import dataclass


@dataclass
class ResultadoPrueba:
    nombre: str
    estadistico: float
    valor_p: float

    def decision(self, significancia: float = 0.05) -> str:
        if not 0 < significancia < 1:
            raise ValueError("La significancia debe estar entre 0 y 1")

        if self.valor_p < significancia:
            return "Se rechaza H0"
        return "No se rechaza H0"