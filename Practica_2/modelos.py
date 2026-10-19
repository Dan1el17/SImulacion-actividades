# ============================================================
# modelos.py
# Los 4 modelos de crecimiento poblacional de la practica.
# ============================================================
#
# PATRONES DE DISEÑO USADOS (pequenos y sencillos):
#   1) CLASE BASE : ModeloPoblacion guarda los datos comunes (P0, r, tiempo).
#   2) STRATEGY   : cada modelo implementa su propio calcular()/ejecutar().
#   3) FACTORY    : la funcion crear_modelo(nombre, ...) devuelve el modelo
#                   correcto sin que el resto del programa sepa cual es.
#
# Formulas de la guia:
#   Deterministico : P(t)      = P0 * e^(r*t)
#   Discreto       : P(t+1)    = P(t) + r * P(t)
#   Estocastico    : P(t+1)    = P(t) + r * P(t) + ruido ~ N(0, sigma)
#   Continuo Euler : P(t + dt) = P(t) + dt * (r * P(t))

import math

import numpy as np


# ------------------------------------------------------------------
# PATRON 1: clase base
# ------------------------------------------------------------------
class ModeloPoblacion:
    """Clase base con los datos comunes a todos los modelos."""

    def __init__(self, P0, r, tiempo, nombre="Modelo"):
        self.P0 = P0          # poblacion inicial (primer dato)
        self.r = r            # tasa de crecimiento (positiva o negativa)
        self.tiempo = tiempo  # numero de pasos a simular
        self.nombre = nombre  # nombre para la leyenda de la grafica

    def calcular(self):
        """Cada modelo concreto debe implementar este metodo."""
        raise NotImplementedError("Cada modelo debe implementar calcular()")

    def ejecutar(self):
        """PATRON 2 (Strategy): forma comun de usar cualquier modelo."""
        return self.calcular()


# ------------------------------------------------------------------
# Los 4 modelos concretos (estrategias)
# ------------------------------------------------------------------
class ModeloDeterministico(ModeloPoblacion):
    """P(t) = P0 * e^(r*t). No tiene aleatoriedad."""

    def __init__(self, P0, r, tiempo):
        super().__init__(P0, r, tiempo, "Deterministico")
        self.num_puntos = 200  # puntos para que la curva se vea suave

    def calcular(self):
        tiempos = []
        poblaciones = []
        for i in range(self.num_puntos):
            t = self.tiempo * i / (self.num_puntos - 1)
            tiempos.append(t)
            poblaciones.append(self.P0 * math.exp(self.r * t))
        return tiempos, poblaciones


class ModeloDiscreto(ModeloPoblacion):
    """P(t+1) = P(t) + r * P(t). El tiempo son pasos enteros."""

    def __init__(self, P0, r, tiempo):
        super().__init__(P0, r, tiempo, "Discreto")

    def calcular(self):
        tiempos = [0]
        poblaciones = [self.P0]
        P = self.P0
        for paso in range(1, self.tiempo + 1):
            P = P + self.r * P
            tiempos.append(paso)
            poblaciones.append(P)
        return tiempos, poblaciones


class ModeloEstocastico(ModeloPoblacion):
    """P(t+1) = P(t) + r*P(t) + ruido, con ruido ~ N(0, sigma)."""

    def __init__(self, P0, r, tiempo, sigma, semilla=42):
        super().__init__(P0, r, tiempo, "Estocastico")
        self.sigma = sigma
        # Semilla fija (42): la misma semilla siempre da el mismo ruido,
        # asi los resultados son reproducibles y las pruebas son estables.
        self.semilla = semilla

    def calcular(self):
        generador = np.random.default_rng(self.semilla)
        tiempos = [0]
        poblaciones = [self.P0]
        P = self.P0
        for paso in range(1, self.tiempo + 1):
            ruido = generador.normal(0.0, self.sigma)
            P = P + self.r * P + ruido
            # Regla de la guia: una poblacion negativa se deja en 0
            if P < 0:
                P = 0
            tiempos.append(paso)
            poblaciones.append(P)
        return tiempos, poblaciones


class ModeloContinuoEuler(ModeloPoblacion):
    """P(t + dt) = P(t) + dt * (r * P(t)). Metodo de Euler."""

    def __init__(self, P0, r, tiempo, dt):
        super().__init__(P0, r, tiempo, "Continuo (Euler)")
        self.dt = dt
        self.num_pasos = int(round(tiempo / dt))

    def calcular(self):
        tiempos = [0.0]
        poblaciones = [self.P0]
        P = self.P0
        for paso in range(1, self.num_pasos + 1):
            P = P + self.dt * (self.r * P)
            tiempos.append(paso * self.dt)
            poblaciones.append(P)
        return tiempos, poblaciones


# ------------------------------------------------------------------
# PATRON 3: fabrica (Factory)
# ------------------------------------------------------------------
NOMBRES_MODELOS = [
    "deterministico",
    "discreto",
    "estocastico",
    "continuo_euler",
]


def crear_modelo(nombre, P0, r, tiempo, sigma=0.0, dt=0.1, semilla=42):
    """
    Devuelve el modelo que corresponde al nombre indicado.
    Asi el programa principal no necesita conocer las clases directamente.
    """
    if nombre == "deterministico":
        return ModeloDeterministico(P0, r, tiempo)
    if nombre == "discreto":
        return ModeloDiscreto(P0, r, tiempo)
    if nombre == "estocastico":
        return ModeloEstocastico(P0, r, tiempo, sigma, semilla)
    if nombre == "continuo_euler":
        return ModeloContinuoEuler(P0, r, tiempo, dt)
    raise ValueError(f"Modelo desconocido: {nombre}")


def ejecutar_todos(P0, r, tiempo, sigma, dt, semilla=42):
    """Crea y ejecuta los 4 modelos. Devuelve (nombre, tiempos, poblaciones)."""
    series = []
    for nombre in NOMBRES_MODELOS:
        modelo = crear_modelo(nombre, P0, r, tiempo, sigma, dt, semilla)
        tiempos, poblaciones = modelo.ejecutar()
        series.append((modelo.nombre, tiempos, poblaciones))
    return series
