from scipy.stats import kstest

from src.pruebas.prueba_uniformidad import PruebaUniformidad
from src.resultado import ResultadoPrueba


class KolmogorovSmirnov(PruebaUniformidad):
    def evaluar(self, valores: list[float]) -> ResultadoPrueba:
        self.validar_datos(valores)
        resultado = kstest(valores, "uniform")

        return ResultadoPrueba(
            "Kolmogorov-Smirnov",
            float(resultado.statistic),
            float(resultado.pvalue),
        )
