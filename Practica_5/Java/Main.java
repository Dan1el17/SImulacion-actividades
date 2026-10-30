public class Main {
    public static void main(String[] args) {
        int cantidad = 10_000;
        GeneradorCongruencial generador = new GeneradorCongruencial(12345L);
        long[] valores = generador.generar(cantidad);

        System.out.println("Primeros 20 valores de X:");
        for (int i = 0; i < 20; i++) {
            System.out.println("X" + (i + 1) + " = " + valores[i]);
        }
    }
}
