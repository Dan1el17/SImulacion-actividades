import java.util.Arrays;
import java.util.Locale;

public final class EstimacionPi {
    private static final int[] TAMANOS_MUESTRA = {1_000, 10_000, 100_000, 1_000_000};
    private static final int REPETICIONES = 5;

    private EstimacionPi() {
    }

    private static long mediana(long[] valores) {
        Arrays.sort(valores);
        return valores[valores.length / 2];
    }

    private static void ejecutar(long semilla, int repeticiones) {
        System.out.println("n,puntos_dentro,pi_estimado,error_absoluto,chi_cuadrado,tiempo_ms,hash_secuencia");
        for (int cantidad : TAMANOS_MUESTRA) {
            long[] tiempos = new long[repeticiones];
            ResultadoExperimento primero = null;
            for (int i = 0; i < repeticiones; i++) {
                ResultadoExperimento actual = ExperimentoMonteCarlo.ejecutar(cantidad, semilla);
                if (primero == null) {
                    primero = actual;
                } else if (primero.puntosDentro != actual.puntosDentro) {
                    throw new IllegalStateException("Las repeticiones no produjeron los mismos puntos.");
                }
                tiempos[i] = actual.tiempoNs;
            }

            double tiempoMedianoMs = mediana(tiempos) / 1_000_000.0;
            System.out.printf(
                    Locale.ROOT,
                    "%d,%d,%.17g,%.17g,%.17g,%.17g,%s%n",
                    cantidad,
                    primero.puntosDentro,
                    primero.estimacion,
                    primero.error,
                    primero.chiCuadrado,
                    tiempoMedianoMs,
                    ExperimentoMonteCarlo.calcularHashSecuencia(cantidad, semilla));
        }
    }

    public static void main(String[] args) {
        if (args.length > 2) {
            throw new IllegalArgumentException("Uso: java EstimacionPi [semilla] [repeticiones]");
        }
        long semilla = args.length >= 1 ? Long.parseUnsignedLong(args[0]) : 2026L;
        int repeticiones = args.length >= 2 ? Integer.parseInt(args[1]) : REPETICIONES;
        if (semilla < 1 || semilla >= GeneradorCongruencialLineal.MODULO) {
            throw new IllegalArgumentException(
                    "La semilla debe estar entre 1 y " + (GeneradorCongruencialLineal.MODULO - 1) + ".");
        }
        if (repeticiones < 1) {
            throw new IllegalArgumentException("El numero de repeticiones debe ser mayor que cero.");
        }
        ejecutar(semilla, repeticiones);
    }
}
