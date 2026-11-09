import csv
import time
from pathlib import Path

from src.generadores.lcg import LCG
from src.pruebas.chi_cuadrado import ChiCuadrado
from src.pruebas.kolmogorov_smirnov import KolmogorovSmirnov


SEMILLA = 123
MULTIPLICADOR = 1103515245
INCREMENTO = 12345
MODULO = 2**31
TAMANOS_MUESTRA = (1_000, 10_000, 100_000, 1_000_000)
SIGNIFICANCIA = 0.05


def main() -> None:
    pruebas = [ChiCuadrado(intervalos=10), KolmogorovSmirnov()]
    ruta_resultados = (
        Path(__file__).resolve().parent.parent
        / "resultados"
        / "resultados_python.csv"
    )
    ruta_resultados.parent.mkdir(parents=True, exist_ok=True)

    with ruta_resultados.open("w", newline="", encoding="utf-8") as archivo:
        columnas = [
            "cantidad",
            "chi_cuadrado",
            "p_chi_cuadrado",
            "decision_chi_cuadrado",
            "estadistico_ks",
            "p_ks",
            "decision_ks",
            "tiempo_total_segundos",
        ]
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()

        for cantidad in TAMANOS_MUESTRA:
            inicio = time.perf_counter()
            generador = LCG(SEMILLA, MULTIPLICADOR, INCREMENTO, MODULO)
            valores = generador.generar(cantidad)

            print(f"\nCantidad de numeros: {cantidad:,}")
            resultados = [prueba.evaluar(valores) for prueba in pruebas]
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

    print(f"\nResultados guardados en: {ruta_resultados}")


if __name__ == "__main__":
    main()