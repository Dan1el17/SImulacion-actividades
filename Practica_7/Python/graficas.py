from Python.configuracion import (
    PI_REFERENCIA,
    REPETICIONES,
    TAMANO_MUESTRA,
    VALOR_CRITICO_CHI_CUADRADO,
)
from Python.comparacion import RUTA_RESULTADOS


def crear_graficas(resultados_python, resultados_java):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise RuntimeError(
            "Falta Matplotlib. Instala las dependencias con: python3 -m pip install -r requirements.txt"
        ) from error

    RUTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    muestras = list(TAMANO_MUESTRA)

    def guardar(nombre):
        plt.tight_layout()
        plt.savefig(RUTA_RESULTADOS / nombre, dpi=160)
        plt.close()

    for lenguaje, resultados, estilo in (
        ("Python", resultados_python, "o-"),
        ("Java", resultados_java, "s--"),
    ):
        plt.plot(
            muestras,
            [float(resultados[n]["pi_estimado"]) for n in muestras],
            estilo,
            label=lenguaje,
        )
    plt.axhline(PI_REFERENCIA, color="black", linestyle=":", label="Valor de referencia")
    plt.xscale("log")
    plt.xticks(muestras, [f"{n:,}".replace(",", " ") for n in muestras])
    plt.xlabel("Numero de puntos (N)")
    plt.ylabel("Estimacion de pi")
    plt.title("Estimacion de pi por Monte Carlo")
    plt.grid(True, alpha=0.3)
    plt.legend()
    guardar("estimacion_pi.png")

    for lenguaje, resultados, estilo in (
        ("Python", resultados_python, "o-"),
        ("Java", resultados_java, "s--"),
    ):
        plt.plot(
            muestras,
            [float(resultados[n]["error_absoluto"]) for n in muestras],
            estilo,
            label=lenguaje,
        )
    plt.xscale("log")
    plt.yscale("log")
    plt.xticks(muestras, [f"{n:,}".replace(",", " ") for n in muestras])
    plt.xlabel("Numero de puntos (N)")
    plt.ylabel("Error absoluto")
    plt.title("Error absoluto segun el tamano de muestra")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    guardar("error_absoluto.png")

    for lenguaje, resultados, estilo in (
        ("Python", resultados_python, "o-"),
        ("Java", resultados_java, "s--"),
    ):
        plt.plot(
            muestras,
            [float(resultados[n]["tiempo_ms"]) for n in muestras],
            estilo,
            label=lenguaje,
        )
    plt.xscale("log")
    plt.yscale("log")
    plt.xticks(muestras, [f"{n:,}".replace(",", " ") for n in muestras])
    plt.xlabel("Numero de puntos (N)")
    plt.ylabel("Tiempo mediano (ms)")
    plt.title(f"Tiempo de ejecucion (mediana de {REPETICIONES} ejecuciones)")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    guardar("tiempo_ejecucion.png")

    for lenguaje, resultados, estilo in (
        ("Python", resultados_python, "o-"),
        ("Java", resultados_java, "s--"),
    ):
        plt.plot(
            muestras,
            [float(resultados[n]["chi_cuadrado"]) for n in muestras],
            estilo,
            label=lenguaje,
        )
    plt.axhline(
        VALOR_CRITICO_CHI_CUADRADO,
        color="black",
        linestyle=":",
        label=f"Valor critico (gl=15, alfa=0.05): {VALOR_CRITICO_CHI_CUADRADO:.3f}",
    )
    plt.xscale("log")
    plt.xticks(muestras, [f"{n:,}".replace(",", " ") for n in muestras])
    plt.xlabel("Numero de puntos (N)")
    plt.ylabel("Estadistico chi-cuadrado")
    plt.title("Prueba de uniformidad en una cuadricula de 4 x 4")
    plt.grid(True, alpha=0.3)
    plt.legend()
    guardar("chi_cuadrado.png")
