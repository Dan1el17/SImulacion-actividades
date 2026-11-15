import csv
import statistics
import sys

from experimento_montecarlo import calcular_hash_secuencia, ejecutar_experimento
from configuracion import REPETICIONES, TAMANO_MUESTRA
from generador_aleatorio import MODULO


def ejecutar(semilla, repeticiones):
    salida = csv.writer(sys.stdout, lineterminator="\n")
    salida.writerow(
        [
            "n",
            "puntos_dentro",
            "pi_estimado",
            "error_absoluto",
            "chi_cuadrado",
            "tiempo_ms",
            "hash_secuencia",
        ]
    )

    for cantidad in TAMANO_MUESTRA:
        mediciones = [ejecutar_experimento(cantidad, semilla) for _ in range(repeticiones)]
        primera = mediciones[0]
        if any(medicion["puntos_dentro"] != primera["puntos_dentro"] for medicion in mediciones):
            raise RuntimeError("Las repeticiones no produjeron los mismos puntos.")

        tiempo_mediano_ms = statistics.median(
            medicion["tiempo_ns"] for medicion in mediciones
        ) / 1_000_000.0
        salida.writerow(
            [
                cantidad,
                primera["puntos_dentro"],
                format(primera["estimacion"], ".17g"),
                format(primera["error"], ".17g"),
                format(primera["chi_cuadrado"], ".17g"),
                format(tiempo_mediano_ms, ".17g"),
                calcular_hash_secuencia(cantidad, semilla),
            ]
        )


def main():
    if len(sys.argv) > 3:
        raise SystemExit("Uso: python3 estimacion_pi.py [semilla] [repeticiones]")

    semilla = int(sys.argv[1]) if len(sys.argv) >= 2 else 2026
    repeticiones = int(sys.argv[2]) if len(sys.argv) >= 3 else REPETICIONES
    if not 1 <= semilla < MODULO:
        raise SystemExit(f"La semilla debe estar entre 1 y {MODULO - 1}.")
    if repeticiones < 1:
        raise SystemExit("El numero de repeticiones debe ser mayor que cero.")
    ejecutar(semilla, repeticiones)


if __name__ == "__main__":
    main()
