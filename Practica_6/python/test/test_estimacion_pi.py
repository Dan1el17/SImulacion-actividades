import unittest

from src.estimacion_pi import estimar_pi
from src.generadores.lcg import LCG


class PruebasEstimacionPi(unittest.TestCase):
    def test_estimacion_usa_dos_valores_por_punto(self):
        generador = LCG(semilla=7, multiplicador=5, incremento=3, modulo=16)

        resultado = estimar_pi(generador, 2)

        self.assertEqual(resultado.puntos_dentro, 2)
        self.assertEqual(resultado.pi_estimado, 4)
        self.assertEqual(
            resultado.sha256_secuencia,
            "a9eef3ce335c54728a008489041f04c1a5d909b9ff2c048e520bd4bd52d87176",
        )

    def test_cantidad_no_positiva_falla(self):
        with self.assertRaises(ValueError):
            estimar_pi(LCG(1, 5, 3, 16), 0)


if __name__ == "__main__":
    unittest.main()
