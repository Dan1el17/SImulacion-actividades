import matplotlib.pyplot as plt

UMBRALES = {
    "Baja posibilidad (0.40)": 0.40,
    "Lluvia probable (0.60)": 0.60,
    "Lluvia (0.75)": 0.75,
}


class GraficaView:
    def mostrar_indice(self, resultados, titulo, guardar=None):
        horas = [r.observacion.hora for r in resultados]
        indices = [r.indice for r in resultados]

        plt.figure(figsize=(10, 5))
        plt.plot(horas, indices, marker="o", label="Índice I")
        for etiqueta, valor in UMBRALES.items():
            plt.axhline(y=valor, linestyle="--", alpha=0.7, label=etiqueta)
        plt.xlabel("Hora")
        plt.ylabel("Índice de lluvia")
        plt.title(titulo)
        plt.ylim(0, 1)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        if guardar:
            plt.savefig(guardar, dpi=150)
        plt.show()