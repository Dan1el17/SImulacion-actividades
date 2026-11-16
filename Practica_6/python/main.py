import csv
import time
from pathlib import Path

from src.generadores.lcg import LCG
from src.estimacion_pi import estimar_pi
from src.pruebas.chi_cuadrado import ChiCuadrado
from src.pruebas.grafica_ks import guardar_grafica_ks
from src.pruebas.kolmogorov_smirnov import KolmogorovSmirnov


SEMILLA = 123
MULTIPLICADOR = 1103515245
INCREMENTO = 12345
MODULO = 2**31
TAMANOS_MUESTRA = (1_000, 10_000, 100_000, 1_000_000)
SIGNIFICANCIA = 0.05


def main() -> None:
    prueba_chi = ChiCuadrado(intervalos=10)
    pruebas = [prueba_chi, KolmogorovSmirnov()]
    ruta_resultados = (
        Path(__file__).resolve().parent.parent
        / "resultados"
        / "resultados_python.csv"
    )
    ruta_resultados.parent.mkdir(parents=True, exist_ok=True)
    ruta_pi = ruta_resultados.parent / "resultados_pi_python.csv"
    valores_grafica = []

    with ruta_resultados.open("w", newline="", encoding="utf-8") as archivo:
        columnas = [
            "cantidad",
            "frecuencias_observadas",
            "frecuencia_esperada",
            "chi_cuadrado",
            "p_chi_cuadrado",
            "decision_chi_cuadrado",
            "estadistico_ks",
            "p_ks",
            "decision_ks",
            "tiempo_total_segundos",
        ]
        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas,
            lineterminator="\n",
        )
        escritor.writeheader()

        for indice, cantidad in enumerate(TAMANOS_MUESTRA):
            inicio = time.perf_counter()
            generador = LCG(SEMILLA, MULTIPLICADOR, INCREMENTO, MODULO)
            valores = generador.generar(cantidad)
            if indice == len(TAMANOS_MUESTRA) - 1:
                valores_grafica = valores

            print(f"\nCantidad de numeros: {cantidad:,}")
            resultados = [prueba.evaluar(valores) for prueba in pruebas]
            frecuencias = prueba_chi.frecuencias_observadas(valores)
            frecuencia_esperada = cantidad / prueba_chi.intervalos
            print(f"Frecuencias observadas: {frecuencias}")
            print(
                "Frecuencias esperadas: "
                f"{[frecuencia_esperada] * prueba_chi.intervalos}"
            )
            for resultado in resultados:
                print(
                    f"{resultado.nombre}: "
                    f"estadistico={resultado.estadistico:.6f}, "
                    f"p={resultado.valor_p:.6f}, "
                    f"{resultado.decision(SIGNIFICANCIA)}"
                )

            tiempo_total = time.perf_counter() - inicio
            print(f"Tiempo total: {tiempo_total:.6f} segundos")
            escritor.writerow(
                {
                    "cantidad": cantidad,
                    "frecuencias_observadas": ";".join(map(str, frecuencias)),
                    "frecuencia_esperada": frecuencia_esperada,
                    "chi_cuadrado": resultados[0].estadistico,
                    "p_chi_cuadrado": resultados[0].valor_p,
                    "decision_chi_cuadrado": resultados[0].decision(
                        SIGNIFICANCIA
                    ),
                    "estadistico_ks": resultados[1].estadistico,
                    "p_ks": resultados[1].valor_p,
                    "decision_ks": resultados[1].decision(SIGNIFICANCIA),
                    "tiempo_total_segundos": tiempo_total,
                }
            )

    with ruta_pi.open("w", newline="", encoding="utf-8") as archivo:
        columnas_pi = [
            "cantidad_puntos",
            "puntos_dentro",
            "pi_estimado",
            "error_absoluto",
            "tiempo_segundos",
            "sha256_secuencia",
        ]
        escritor_pi = csv.DictWriter(
            archivo,
            fieldnames=columnas_pi,
            lineterminator="\n",
        )
        escritor_pi.writeheader()

        for cantidad in TAMANOS_MUESTRA:
            resultado = estimar_pi(
                LCG(SEMILLA, MULTIPLICADOR, INCREMENTO, MODULO),
                cantidad,
            )
            error = abs(3.141592653589793 - resultado.pi_estimado)
            escritor_pi.writerow(
                {
                    "cantidad_puntos": cantidad,
                    "puntos_dentro": resultado.puntos_dentro,
                    "pi_estimado": resultado.pi_estimado,
                    "error_absoluto": error,
                    "tiempo_segundos": resultado.tiempo_segundos,
                    "sha256_secuencia": resultado.sha256_secuencia,
                }
            )
            print(
                f"\nEstimacion de pi ({cantidad:,} puntos): "
                f"{resultado.pi_estimado:.8f}; error={error:.8f}; "
                f"tiempo={resultado.tiempo_segundos:.6f} s"
            )

    ruta_grafica = ruta_resultados.parent / "ecdf_ks_python.png"
    guardar_grafica_ks(valores_grafica, ruta_grafica)
    print(f"\nResultados guardados en: {ruta_resultados}")
    print(f"Resultados de pi guardados en: {ruta_pi}")
    print(f"Grafica KS guardada en: {ruta_grafica}")


if __name__ == "__main__":
    main()