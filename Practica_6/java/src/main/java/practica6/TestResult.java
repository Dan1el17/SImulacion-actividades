package practica6;

public record TestResult(String name, double statistic, double pValue) {
    public String decision(double significance) {
        if (!(significance > 0 && significance < 1)) {
            throw new IllegalArgumentException("La significancia debe estar entre 0 y 1");
        }
        return pValue < significance ? "Se rechaza H0" : "No se rechaza H0";
    }
}
