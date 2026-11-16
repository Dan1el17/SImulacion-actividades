package practica6;

public final class ChiSquaredTest implements UniformityTest {
    private final int intervals;

    public ChiSquaredTest(int intervals) {
        if (intervals <= 0) {
            throw new IllegalArgumentException("La cantidad de intervalos debe ser positiva");
        }
        this.intervals = intervals;
    }

    @Override
    public TestResult evaluate(double[] values) {
        validate(values);
        double expected = (double) values.length / intervals;
        if (expected < 5) {
            throw new IllegalArgumentException(
                    "Chi-cuadrado requiere una frecuencia esperada de al menos 5");
        }

        int[] observed = new int[intervals];
        for (double value : values) {
            int interval = (int) (value * intervals);
            observed[interval]++;
        }

        double statistic = 0;
        for (int frequency : observed) {
            double difference = frequency - expected;
            statistic += difference * difference / expected;
        }
        double pValue = SpecialFunctions.regularizedGammaQ(
                (intervals - 1) / 2.0,
                statistic / 2.0);
        return new TestResult("Chi-cuadrado", statistic, pValue);
    }

    private static void validate(double[] values) {
        if (values.length == 0) {
            throw new IllegalArgumentException("La secuencia no puede estar vacia");
        }
        for (double value : values) {
            if (!(value >= 0 && value < 1)) {
                throw new IllegalArgumentException("Todos los valores deben pertenecer a [0, 1)");
            }
        }
    }
}
