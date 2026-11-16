package practica6;

final class SpecialFunctions {
    private static final double[] LANCZOS = {
        676.5203681218851,
        -1259.1392167224028,
        771.32342877765313,
        -176.61502916214059,
        12.507343278686905,
        -0.13857109526572012,
        9.9843695780195716e-6,
        1.5056327351493116e-7
    };
    private static final double EPSILON = 1e-14;
    private static final double TINY = 1e-300;

    private SpecialFunctions() {}

    static double regularizedGammaQ(double shape, double x) {
        if (!(shape > 0) || x < 0) {
            throw new IllegalArgumentException("Argumentos invalidos para gamma incompleta");
        }
        if (x == 0) {
            return 1;
        }
        if (x < shape + 1) {
            double term = 1 / shape;
            double sum = term;
            double denominator = shape;
            for (int iteration = 1; iteration < 100_000; iteration++) {
                denominator++;
                term *= x / denominator;
                sum += term;
                if (Math.abs(term) <= Math.abs(sum) * EPSILON) {
                    break;
                }
            }
            double p = sum * Math.exp(-x + shape * Math.log(x) - logGamma(shape));
            return clamp01(1 - p);
        }

        double b = x + 1 - shape;
        double c = 1 / TINY;
        double d = 1 / Math.max(Math.abs(b), TINY);
        if (b < 0) {
            d = -d;
        }
        double h = d;
        for (int iteration = 1; iteration < 100_000; iteration++) {
            double an = -iteration * (iteration - shape);
            b += 2;
            d = an * d + b;
            if (Math.abs(d) < TINY) {
                d = TINY;
            }
            c = b + an / c;
            if (Math.abs(c) < TINY) {
                c = TINY;
            }
            d = 1 / d;
            double delta = d * c;
            h *= delta;
            if (Math.abs(delta - 1) <= EPSILON) {
                break;
            }
        }
        return clamp01(Math.exp(-x + shape * Math.log(x) - logGamma(shape)) * h);
    }

    private static double logGamma(double value) {
        if (value < 0.5) {
            return Math.log(Math.PI)
                    - Math.log(Math.sin(Math.PI * value))
                    - logGamma(1 - value);
        }
        double adjusted = value - 1;
        double sum = 0.99999999999980993;
        for (int index = 0; index < LANCZOS.length; index++) {
            sum += LANCZOS[index] / (adjusted + index + 1);
        }
        double t = adjusted + LANCZOS.length - 0.5;
        return 0.5 * Math.log(2 * Math.PI)
                + (adjusted + 0.5) * Math.log(t)
                - t
                + Math.log(sum);
    }

    private static double clamp01(double value) {
        return Math.max(0, Math.min(1, value));
    }
}
