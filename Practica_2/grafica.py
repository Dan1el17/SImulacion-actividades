# ============================================================
# grafica.py
# Graficas de la practica con matplotlib.
# ============================================================

import math

import matplotlib.pyplot as plt


def graficar_comparativa(series, titulo):
    """
    Grafica comparativa de los 4 modelos.

    Entrada:
        series: lista de tuplas (nombre, tiempos, poblaciones)
        titulo: texto de arriba de la grafica

    La grafica lleva titulo, eje X "Tiempo", eje Y "Poblacion",
    leyenda y cuadricula.
    """
    plt.figure(figsize=(10, 6))

    for nombre, tiempos, poblaciones in series:
        plt.plot(tiempos, poblaciones, label=nombre, linewidth=2)

    plt.title(titulo, fontsize=14, fontweight="bold")
    plt.xlabel("Tiempo")
    plt.ylabel("Poblacion")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


def graficar_influencia_r(P0, r, tiempo):
    """
    Muestra la influencia de r: compara el modelo deterministico
    con r*0.5, r (la calculada) y r*1.5.
    """
    plt.figure(figsize=(10, 6))

    dt = 0.1
    num_pasos = int(tiempo / dt)
    valores = [r * 0.5, r, r * 1.5]
    etiquetas = ["r * 0.5", "r (calculada)", "r * 1.5"]

    for valor_r, etiqueta in zip(valores, etiquetas):
        tiempos = []
        poblaciones = []
        for paso in range(num_pasos + 1):
            t = paso * dt
            tiempos.append(t)
            poblaciones.append(P0 * math.exp(valor_r * t))
        plt.plot(tiempos, poblaciones,
                 label=f"{etiqueta} = {valor_r:.4f}", linewidth=2)

    plt.title("Influencia de la tasa r (modelo deterministico)",
              fontsize=14, fontweight="bold")
    plt.xlabel("Tiempo")
    plt.ylabel("Poblacion")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()
