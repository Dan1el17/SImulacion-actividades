from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def guardar_grafica_ks(valores: list[float], ruta: Path) -> None:
    ordenados = sorted(valores)
    cantidad = len(ordenados)
    acumulada_empirica = [(indice + 1) / cantidad for indice in range(cantidad)]

    figura, eje = plt.subplots()
    eje.step(
        ordenados,
        acumulada_empirica,
        where="post",
        label="Distribución acumulada empírica",
    )
    eje.plot([0, 1], [0, 1], "--", label="Distribución uniforme teórica")
    eje.set(
        title="Prueba Kolmogorov-Smirnov",
        xlabel="Valor generado",
        ylabel="Probabilidad acumulada",
        xlim=(0, 1),
        ylim=(0, 1),
    )
    eje.grid(True, alpha=0.3)
    eje.legend()
    figura.tight_layout()
    figura.savefig(ruta, dpi=150)
    plt.close(figura)
