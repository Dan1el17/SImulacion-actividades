import unittest

from src.pruebas.chi_cuadrado import ChiCuadrado
from src.pruebas.kolmogorov_smirnov import KolmogorovSmirnov


class PruebasUniformidadTest(unittest.TestCase):
    def setUp(self):
        self.valores = [(indice + 0.5) / 100 for indice in range(100)]

    def test_chi_cuadrado_con_frecuencias_iguales(self):
        resultado = ChiCuadrado().evaluar(self.valores)

        self.assertEqual(resultado.estadistico, 0)
        self.assertAlmostEqual(resultado.valor_p, 1)

    def test_kolmogorov_smirnov_devuelve_resultado_valido(self):
        resultado = KolmogorovSmirnov().evaluar(self.valores)

        self.assertGreaterEqual(resultado.estadistico, 0)
        self.assertGreaterEqual(resultado.valor_p, 0)
        self.assertLessEqual(resultado.valor_p, 1)

    def test_rechaza_datos_fuera_del_intervalo(self):
        with self.assertRaises(ValueError):
            KolmogorovSmirnov().evaluar([0.2, 1.0])


if __name__ == "__main__":
    unittest.main()
