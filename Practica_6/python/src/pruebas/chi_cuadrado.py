from scipy.stats import chisquare

from src.pruebas.prueba_uniformidad import PruebaUniformidad
from src.resultado import ResultadoPrueba


class ChiCuadrado(PruebaUniformidad):
    def __init__(self, intervalos: int = 10):
        if intervalos <= 0:
            raise ValueError("La cantidad de intervalos debe ser mayor que cero")

        self.intervalos = intervalos

    def evaluar(self, valores: list[float]) -> ResultadoPrueba:
        frecuencias = self.frecuencias_observadas(valores)
        frecuencia_esperada = len(valores) / self.intervalos

        if frecuencia_esperada < 5:
            raise ValueError(
                "Chi-cuadrado requiere una frecuencia esperada de al menos 5"
            )

        esperadas = [frecuencia_esperada] * self.intervalos
        estadistico, valor_p = chisquare(f_obs=frecuencias, f_exp=esperadas)

        return ResultadoPrueba("Chi-cuadrado", float(estadistico), float(valor_p))

    def frecuencias_observadas(self, valores: list[float]) -> list[int]:
        self.validar_datos(valores)
        frecuencias = [0] * self.intervalos
        for valor in valores:
            frecuencias[int(valor * self.intervalos)] += 1
        return frecuencias
