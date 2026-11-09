import unittest

from src.generadores.lcg import LCG


class PruebasLCG(unittest.TestCase):
    def test_genera_secuencia_conocida(self):
        generador = LCG(semilla=7, multiplicador=5, incremento=3, modulo=16)

        self.assertEqual(generador.generar(4), [0.375, 0.0625, 0.5, 0.6875])

    def test_generar_cantidad_negativa_falla(self):
        generador = LCG(semilla=7, multiplicador=5, incremento=3, modulo=16)

        with self.assertRaises(ValueError):
            generador.generar(-1)

    def test_parametros_invalidos_fallan(self):
        with self.assertRaises(ValueError):
            LCG(semilla=16, multiplicador=5, incremento=3, modulo=16)


if __name__ == "__main__":
    unittest.main()
