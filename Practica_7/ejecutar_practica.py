import sys

from Python.comparacion import RUTA_RESULTADOS, ejecutar_comparacion, guardar_resultados
from Python.configuracion import REPETICIONES
from Python.graficas import crear_graficas
from Python.generador_aleatorio import MODULO


def main():
    if len(sys.argv) > 2:
        raise SystemExit("Uso: python3 ejecutar_practica.py [semilla]")
    semilla = int(sys.argv[1]) if len(sys.argv) == 2 else 2026
    if not 1 <= semilla < MODULO:
        raise SystemExit(f"La semilla debe estar entre 1 y {MODULO - 1}.")

    resultados_python, resultados_java = ejecutar_comparacion(semilla, REPETICIONES)
    guardar_resultados(resultados_python, resultados_java, semilla)
    crear_graficas(resultados_python, resultados_java)

    print("Experimentos completados: Python y Java generaron la misma secuencia.")
    print(f"Tabla y analisis chi-cuadrado: {RUTA_RESULTADOS}")
    print("Graficas creadas: estimacion_pi.png, error_absoluto.png, tiempo_ejecucion.png, chi_cuadrado.png")
    print(f"Tiempo reportado: mediana de {REPETICIONES} ejecuciones por tamano de muestra.")


if __name__ == "__main__":
    main()
