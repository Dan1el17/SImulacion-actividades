package practica6;

import java.util.Arrays;

public final class KolmogorovSmirnovTest implements UniformityTest {
    @Override
    public TestResult evaluate(double[] values) {
        if (values.length == 0) {
            throw new IllegalArgumentException("La secuencia no puede estar vacia");
        }
        double[] sorted = values.clone();
        Arrays.sort(sorted);

        double statistic = 0;
        for (int index = 0; index < sorted.length; index++) {
            double value = sorted[index];
            if (!(value >= 0 && value < 1)) {
                throw new IllegalArgumentException("Todos los valores deben pertenecer a [0, 1)");
            }
            double upperDifference = (index + 1.0) / sorted.length - value;
            double lowerDifference = value - index / (double) sorted.length;
            statistic = Math.max(statistic, Math.max(upperDifference, lowerDifference));
        }

        double rootN = Math.sqrt(sorted.length);
        double lambda = (rootN + 0.12 + 0.11 / rootN) * statistic;
        return new TestResult("Kolmogorov-Smirnov", statistic, kolmogorovSurvival(lambda));
    }

    private static double kolmogorovSurvival(double lambda) {
        if (lambda <= 0) {
            return 1;
        }
        if (lambda < 0.82) {
            double sum = 0;
            for (int index = 1; index < 100_000; index++) {
                double odd = 2 * index - 1;
                double term = Math.exp(
                        -(odd * odd * Math.PI * Math.PI) / (8 * lambda * lambda));
                sum += term;
                if (term < 1e-16 * Math.max(sum, 1e-300)) {
                    break;
                }
            }
            return clamp01(1 - Math.sqrt(2 * Math.PI) * sum / lambda);
        }

        double sum = 0;
        for (int index = 1; index < 100_000; index++) {
            double term = 2 * Math.exp(-2.0 * index * index * lambda * lambda);
            sum += (index % 2 == 1) ? term : -term;
            if (term < 1e-16 * Math.max(Math.abs(sum), 1e-300)) {
                break;
            }
        }
        return clamp01(sum);
    }

    private static double clamp01(double value) {
        return Math.max(0, Math.min(1, value));
    }
}
