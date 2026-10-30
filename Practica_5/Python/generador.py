class GeneradorCongruencial:
    def __init__(self, semilla=12345):
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32
        self.semilla = semilla
        self.estado = semilla

    def siguiente(self):
        self.estado = (self.a * self.estado + self.c) % self.m
        return self.estado

    def generar(self, cantidad):
        return [self.siguiente() for _ in range(cantidad)]

    def normalizar(self, valor):
        return valor / self.m
