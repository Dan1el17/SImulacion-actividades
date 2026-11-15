import java.util.Locale;

public final class ExperimentoMonteCarlo {
    private static final double PI_REFERENCIA = 3.141592653589793;

    private ExperimentoMonteCarlo() {
    }

    public static ResultadoExperimento ejecutar(int cantidad, long semilla) {
        GeneradorAleatorio generador = GeneradorAleatorioFactory.crear(semilla);
        int puntosDentro = 0;
        int[] celdas = new int[16];

        long inicio = System.nanoTime();
        for (int i = 0; i < cantidad; i++) {
            double x = 2.0 * generador.siguienteReal() - 1.0;
            double y = 2.0 * generador.siguienteReal() - 1.0;

            if (x * x + y * y <= 1.0) {
                puntosDentro++;
            }

            int columna = Math.min((int) ((x + 1.0) * 2.0), 3);
            int fila = Math.min((int) ((y + 1.0) * 2.0), 3);
            celdas[fila * 4 + columna]++;
        }
        long tiempoNs = System.nanoTime() - inicio;

        double estimacion = 4.0 * puntosDentro / cantidad;
        double error = Math.abs(estimacion - PI_REFERENCIA);
        double esperado = cantidad / 16.0;
        double chiCuadrado = 0.0;
        for (int observado : celdas) {
            double diferencia = observado - esperado;
            chiCuadrado += diferencia * diferencia / esperado;
        }

        return new ResultadoExperimento(
                puntosDentro,
                estimacion,
                error,
                chiCuadrado,
                tiempoNs);
    }

    public static String calcularHashSecuencia(int cantidad, long semilla) {
        GeneradorAleatorio generador = GeneradorAleatorioFactory.crear(semilla);
        long resultado = 0xCBF29CE484222325L;
        for (int i = 0; i < cantidad * 2; i++) {
            resultado ^= generador.siguienteEntero();
            resultado *= 0x100000001B3L;
        }
        return String.format(Locale.ROOT, "%016x", resultado);
    }
}
