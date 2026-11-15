import time

from generador_aleatorio import crear_generador

MASCARA_HASH = (1 << 64) - 1

PI_REFERENCIA = 3.141592653589793


def ejecutar_experimento(cantidad, semilla):
    generador = crear_generador(semilla)
    puntos_dentro = 0
    celdas = [0] * 16

    inicio = time.perf_counter_ns()
    for _ in range(cantidad):
        x = 2.0 * generador.siguiente_real() - 1.0
        y = 2.0 * generador.siguiente_real() - 1.0

        if x * x + y * y <= 1.0:
            puntos_dentro += 1

        columna = min(int((x + 1.0) * 2.0), 3)
        fila = min(int((y + 1.0) * 2.0), 3)
        celdas[fila * 4 + columna] += 1
    tiempo_ns = time.perf_counter_ns() - inicio

    estimacion = 4.0 * puntos_dentro / cantidad
    error = abs(estimacion - PI_REFERENCIA)
    esperado = cantidad / 16.0
    chi_cuadrado = sum((observado - esperado) ** 2 / esperado for observado in celdas)

    return {
        "puntos_dentro": puntos_dentro,
        "estimacion": estimacion,
        "error": error,
        "chi_cuadrado": chi_cuadrado,
        "tiempo_ns": tiempo_ns,
    }


def calcular_hash_secuencia(cantidad, semilla):
    generador = crear_generador(semilla)
    resultado = 0xCBF29CE484222325
    for _ in range(cantidad * 2):
        resultado ^= generador.siguiente_entero()
        resultado = (resultado * 0x100000001B3) & MASCARA_HASH
    return f"{resultado:016x}"
