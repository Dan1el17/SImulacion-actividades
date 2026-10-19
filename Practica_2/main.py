# ============================================================
# main.py
# Punto de entrada de la Practica 02 (Simulacion).
# ============================================================
#
# Uso:
#     python main.py
#
# Que hace:
#   1) Toma el arreglo de datos de la guia.
#   2) Calcula r y sigma a partir de esos datos.
#   3) Ejecuta los 4 modelos y muestra una grafica comparativa.
#   4) Muestra el crecimiento con r positivo (e decrecimiento con r negativo).
#   5) Muestra la influencia de r.

from grafica import graficar_comparativa, graficar_influencia_r
from modelos import ejecutar_todos
from parametros import calcular_r, calcular_sigma

# Datos que indica la guia
DATOS = [1000, 1100, 1250, 1400, 1600, 1850, 2100]

P0 = DATOS[0]
TIEMPO = len(DATOS) - 1
DT = 0.1
SEMILLA = 42


def main():
    r = calcular_r(DATOS)
    sigma = calcular_sigma(DATOS, r)

    print("Datos de entrada :", DATOS)
    print(f"P0 (poblacion inicial) : {P0}")
    print(f"r  (tasa de crecimiento) : {r:.6f}")
    print(f"sigma (nivel de ruido)   : {sigma:.6f}")
    print(f"dt (paso de Euler)       : {DT}")

    # Escenario 1: crecimiento (con la r calculada de los datos)
    series_crecimiento = ejecutar_todos(P0, r, TIEMPO, sigma, DT, SEMILLA)
    graficar_comparativa(
        series_crecimiento,
        "Comparacion de modelos - Crecimiento (r > 0)",
    )

    # Escenario 2: decrecimiento (con r negativa)
    r_negativa = -abs(r)
    series_decrecimiento = ejecutar_todos(P0, r_negativa, TIEMPO, sigma, DT, SEMILLA)
    graficar_comparativa(
        series_decrecimiento,
        "Comparacion de modelos - Decrecimiento (r < 0)",
    )

    # Escenario 3: influencia de r
    graficar_influencia_r(P0, r, TIEMPO)


if __name__ == "__main__":
    main()
