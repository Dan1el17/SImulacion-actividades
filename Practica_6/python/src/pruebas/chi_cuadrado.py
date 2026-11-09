from scipy.stats import chisquare

from src.pruebas.prueba_uniformidad import PruebaUniformidad
from src.resultado import ResultadoPrueba


class ChiCuadrado(PruebaUniformidad):
    def __init__(self, intervalos: int = 10):
        if intervalos <= 0:
            raise ValueError("La cantidad de intervalos debe ser mayor que cero")

        self.intervalos = intervalos

    def evaluar(self, valores: list[float]) -> ResultadoPrueba:
        self.validar_datos(valores)
        frecuencia_esperada = len(valores) / self.intervalos

        if frecuencia_esperada < 5:
            raise ValueError(
                "Chi-cuadrado requiere una frecuencia esperada de al menos 5"
            )

        frecuencias = [0] * self.intervalos
        for valor in valores:
            indice = int(valor * self.intervalos)
            frecuencias[indice] += 1

        esperadas = [frecuencia_esperada] * self.intervalos
        estadistico, valor_p = chisquare(f_obs=frecuencias, f_exp=esperadas)

        return ResultadoPrueba("Chi-cuadrado", float(estadistico), float(valor_p))
