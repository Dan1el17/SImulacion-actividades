# ============================================================
# parametros.py
# Calculo de los parametros r y sigma a partir de los datos.
# ============================================================
#
# La guia no dice como obtener r, asi que lo calculamos desde el
# arreglo de datos con una regresion lineal.
#
# COMO SE CALCULA r:
#   El modelo deterministico supone crecimiento exponencial:
#       P(t) = P0 * e^(r*t)
#   Tomando logaritmo natural en los dos lados:
#       ln(P(t)) = ln(P0) + r * t
#   Esto es una RECTA (y = a + m*t) donde la PENDIENTE es r.
#   Por eso ajustamos una recta a ln(P) contra t y usamos su pendiente.
#   Datos crecientes -> r > 0 ; datos que bajan -> r < 0.

import numpy as np
from scipy import stats


def calcular_r(datos):
    """Calcula la tasa de crecimiento r a partir del arreglo de datos."""
    datos = np.asarray(datos, dtype=float)

    if np.any(datos <= 0):
        raise ValueError("Todos los datos deben ser mayores que cero.")
    if datos.size < 2:
        raise ValueError("Se necesitan al menos 2 datos para calcular r.")

    # El tiempo de los datos es discreto: 0, 1, 2, ..., n-1
    tiempo = np.arange(datos.size, dtype=float)

    # Regresion lineal de ln(P) contra t; la pendiente es r
    regresion = stats.linregress(tiempo, np.log(datos))
    return float(regresion.slope)


def calcular_sigma(datos, r):
    """
    Estima sigma (variabilidad del ruido) a partir de los datos.

    Se calculan los residuos: cuanto se desvian los datos de la recta
    ln(P) = a + r*t. sigma es la desviacion estandar de esos residuos.
    """
    datos = np.asarray(datos, dtype=float)
    tiempo = np.arange(datos.size, dtype=float)
    ln_poblacion = np.log(datos)

    intercepto = float(np.mean(ln_poblacion - r * tiempo))
    residuos = ln_poblacion - (intercepto + r * tiempo)

    sigma = float(np.std(residuos))

    # Si los datos son casi perfectos, damos un minimo para que el
    # modelo estocastico igual tenga algo de ruido.
    if sigma < 1e-6:
        sigma = 0.01
    return sigma
