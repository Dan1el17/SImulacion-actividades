import csv
import math
import subprocess
import sys
import tempfile
from pathlib import Path

from Python.configuracion import (
    ALFA,
    GRADOS_LIBERTAD,
    TAMANO_MUESTRA,
    VALOR_CRITICO_CHI_CUADRADO,
)


RAIZ = Path(__file__).resolve().parents[1]
RUTA_JAVA = RAIZ / "Java"
RUTA_PYTHON = RAIZ / "Python" / "estimacion_pi.py"
RUTA_RESULTADOS = RAIZ / "Resultados"


def _leer_csv(texto):
    filas = list(csv.DictReader(texto.splitlines()))
    if len(filas) != len(TAMANO_MUESTRA):
        raise RuntimeError("Una implementacion no devolvio todos los tamanos de muestra.")
    return {int(fila["n"]): fila for fila in filas}


def _ejecutar_comando(comando):
    resultado = subprocess.run(comando, check=False, capture_output=True, text=True)
    if resultado.returncode != 0:
        detalle = (resultado.stderr or "").strip() or (resultado.stdout or "").strip()
        raise RuntimeError(f"Fallo el comando {' '.join(comando)}:\n{detalle}")
    return resultado.stdout


def ejecutar_comparacion(semilla, repeticiones):
    with tempfile.TemporaryDirectory(prefix="montecarlo_java_") as compilacion:
        fuentes_java = sorted(RUTA_JAVA.glob("*.java"))
        _ejecutar_comando(
            [
                "javac",
                "--release",
                "8",
                "-Xlint:-options",
                "-encoding",
                "UTF-8",
                "-d",
                compilacion,
                *[str(ruta) for ruta in fuentes_java],
            ]
        )
        salida_java = _ejecutar_comando(
            ["java", "-cp", compilacion, "EstimacionPi", str(semilla), str(repeticiones)]
        )

    salida_python = _ejecutar_comando(
        [sys.executable, str(RUTA_PYTHON), str(semilla), str(repeticiones)]
    )
    resultados_python = _leer_csv(salida_python)
    resultados_java = _leer_csv(salida_java)
    validar_secuencia(resultados_python, resultados_java)
    return resultados_python, resultados_java


def validar_secuencia(resultados_python, resultados_java):
    for cantidad in TAMANO_MUESTRA:
        python = resultados_python[cantidad]
        java = resultados_java[cantidad]
        if python["hash_secuencia"] != java["hash_secuencia"]:
            raise RuntimeError(
                f"Python y Java no generaron la misma secuencia para N={cantidad}."
            )
        if python["puntos_dentro"] != java["puntos_dentro"]:
            raise RuntimeError(f"El conteo no coincide para N={cantidad}.")
        for columna in ("pi_estimado", "error_absoluto", "chi_cuadrado"):
            if not math.isclose(
                float(python[columna]),
                float(java[columna]),
                rel_tol=0.0,
                abs_tol=1e-12,
            ):
                raise RuntimeError(f"El resultado {columna} no coincide para N={cantidad}.")


def guardar_resultados(resultados_python, resultados_java, semilla):
    RUTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    with (RUTA_RESULTADOS / "tabla_comparativa.csv").open(
        "w", newline="", encoding="utf-8"
    ) as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(
            [
                "N",
                "puntos_dentro",
                "pi_estimado_python",
                "error_absoluto_python",
                "tiempo_python_ms_mediana",
                "pi_estimado_java",
                "error_absoluto_java",
                "tiempo_java_ms_mediana",
                "semilla",
                "misma_secuencia",
            ]
        )
        for cantidad in TAMANO_MUESTRA:
            python = resultados_python[cantidad]
            java = resultados_java[cantidad]
            escritor.writerow(
                [
                    cantidad,
                    python["puntos_dentro"],
                    python["pi_estimado"],
                    python["error_absoluto"],
                    python["tiempo_ms"],
                    java["pi_estimado"],
                    java["error_absoluto"],
                    java["tiempo_ms"],
                    semilla,
                    "si",
                ]
            )

    with (RUTA_RESULTADOS / "chi_cuadrado.csv").open(
        "w", newline="", encoding="utf-8"
    ) as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(
            [
                "N",
                "lenguaje",
                "estadistico_chi_cuadrado",
                "grados_libertad",
                "alfa",
                "valor_critico",
                "decision",
            ]
        )
        for cantidad in TAMANO_MUESTRA:
            for lenguaje, resultados in (
                ("Python", resultados_python),
                ("Java", resultados_java),
            ):
                chi = float(resultados[cantidad]["chi_cuadrado"])
                decision = (
                    "no se rechaza uniformidad"
                    if chi <= VALOR_CRITICO_CHI_CUADRADO
                    else "se rechaza uniformidad"
                )
                escritor.writerow(
                    [
                        cantidad,
                        lenguaje,
                        resultados[cantidad]["chi_cuadrado"],
                        GRADOS_LIBERTAD,
                        ALFA,
                        VALOR_CRITICO_CHI_CUADRADO,
                        decision,
                    ]
                )
