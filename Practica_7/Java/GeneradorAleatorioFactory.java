public final class GeneradorAleatorioFactory {
    private GeneradorAleatorioFactory() {
    }

    public static GeneradorAleatorio crear(long semilla) {
        return new GeneradorCongruencialLineal(semilla);
    }
}
