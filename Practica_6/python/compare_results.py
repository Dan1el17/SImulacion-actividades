import csv
from pathlib import Path


def leer_resultados(ruta: Path) -> dict[int, dict[str, str]]:
    with ruta.open(newline="", encoding="utf-8") as archivo:
        return {
            int(fila["cantidad_puntos"]): fila
            for fila in csv.DictReader(archivo)
        }


def main() -> None:
    directorio_resultados = Path(__file__).resolve().parent.parent / "resultados"
    resultados_python = leer_resultados(
        directorio_resultados / "resultados_pi_python.csv"
    )
    resultados_java = leer_resultados(
        directorio_resultados / "resultados_pi_java.csv"
    )

    if resultados_python.keys() != resultados_java.keys():
        raise ValueError("Python y Java no contienen las mismas cantidades")

    columnas = [
        "cantidad_puntos",
        "pi_python",
        "error_python",
        "tiempo_python_segundos",
        "pi_java",
        "error_java",
        "tiempo_java_segundos",
        "secuencia_identica",
    ]
    ruta_comparacion = directorio_resultados / "comparacion_pi.csv"
    with ruta_comparacion.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas,
            lineterminator="\n",
        )
        escritor.writeheader()
        for cantidad in sorted(resultados_python):
            python = resultados_python[cantidad]
            java = resultados_java[cantidad]
            misma_secuencia = (
                python["sha256_secuencia"] == java["sha256_secuencia"]
            )
            mismo_pi = float(python["pi_estimado"]) == float(java["pi_estimado"])
            if not misma_secuencia or not mismo_pi:
                raise ValueError(
                    f"La secuencia o la estimacion difiere para N={cantidad}"
                )
            escritor.writerow(
                {
                    "cantidad_puntos": cantidad,
                    "pi_python": python["pi_estimado"],
                    "error_python": python["error_absoluto"],
                    "tiempo_python_segundos": python["tiempo_segundos"],
                    "pi_java": java["pi_estimado"],
                    "error_java": java["error_absoluto"],
                    "tiempo_java_segundos": java["tiempo_segundos"],
                    "secuencia_identica": "si",
                }
            )

    print(f"Secuencias identicas verificadas para {len(resultados_python)} tamanos.")
    print(f"Tabla comparativa guardada en: {ruta_comparacion}")


if __name__ == "__main__":
    main()
