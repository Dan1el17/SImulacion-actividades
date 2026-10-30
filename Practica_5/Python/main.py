import matplotlib.pyplot as plt

from generador import GeneradorCongruencial


def main():
    cantidad = 10_000
    generador = GeneradorCongruencial(semilla=12345)
    valores = generador.generar(cantidad)

    print("Primeros 20 valores de X:")
    for indice, valor in enumerate(valores[:20], start=1):
        print(f"X{indice} = {valor}")

    estados = [generador.semilla, *valores]
    plt.scatter(estados[:-1], estados[1:], s=8)
    plt.xlabel("X(n)")
    plt.ylabel("X(n+1)")
    plt.title("Generador Congruencial Lineal")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
