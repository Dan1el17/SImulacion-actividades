MODULO = 2_147_483_647
MULTIPLICADOR = 16_807
INCREMENTO = 0


class GeneradorCongruencialLineal:
    def __init__(self, semilla):
        if not 1 <= semilla < MODULO:
            raise ValueError(f"La semilla debe estar entre 1 y {MODULO - 1}.")
        self.estado = semilla

    def siguiente_entero(self):
        self.estado = (MULTIPLICADOR * self.estado + INCREMENTO) % MODULO
        return self.estado

    def siguiente_real(self):
        return self.siguiente_entero() / MODULO


def crear_generador(semilla):
    return GeneradorCongruencialLineal(semilla)
