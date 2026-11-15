public final class ResultadoExperimento {
    public final int puntosDentro;
    public final double estimacion;
    public final double error;
    public final double chiCuadrado;
    public final long tiempoNs;

    public ResultadoExperimento(
            int puntosDentro,
            double estimacion,
            double error,
            double chiCuadrado,
            long tiempoNs) {
        this.puntosDentro = puntosDentro;
        this.estimacion = estimacion;
        this.error = error;
        this.chiCuadrado = chiCuadrado;
        this.tiempoNs = tiempoNs;
    }
}
