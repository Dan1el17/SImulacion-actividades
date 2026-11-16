package practica6;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.HexFormat;
import java.util.List;
import java.util.Locale;

public final class EstimacionPi {
    private static final long SEMILLA = 123;
    private static final long MULTIPLICADOR = 1_103_515_245;
    private static final long INCREMENTO = 12_345;
    private static final long MODULO = 1L << 31;
    private static final int[] TAMANOS_MUESTRA = {1_000, 10_000, 100_000, 1_000_000};
    private static final double SIGNIFICANCIA = 0.05;
    private static final int INTERVALOS = 10;

    private EstimacionPi() {}

    public static void main(String[] args) throws IOException, NoSuchAlgorithmException {
        Path directorioResultados = buscarDirectorioResultados();
        ejecutarPruebasUniformidad(directorioResultados);

        Path rutaResultados = directorioResultados.resolve("resultados_pi_java.csv");
        try (BufferedWriter escritor = Files.newBufferedWriter(rutaResultados)) {
            escritor.write(
                    "cantidad_puntos,puntos_dentro,pi_estimado,error_absoluto,"
                            + "tiempo_segundos,sha256_secuencia");
            escritor.newLine();

            for (int cantidad : TAMANOS_MUESTRA) {
                ResultadoPi resultado = estimarPi(cantidad);
                double error = Math.abs(Math.PI - resultado.piEstimado());
                escritor.write(String.format(
                        Locale.ROOT,
                        "%d,%s,%s,%s,%s,%s",
                        cantidad,
                        resultado.puntosDentro(),
                        Double.toString(resultado.piEstimado()),
                        Double.toString(error),
                        Double.toString(resultado.tiempoSegundos()),
                        resultado.sha256Secuencia()));
                escritor.newLine();
                System.out.printf(
                        Locale.ROOT,
                        "N=%d, pi=%.8f, error=%.8f, tiempo=%.6f s%n",
                        cantidad,
                        resultado.piEstimado(),
                        error,
                        resultado.tiempoSegundos());
            }
        }

        System.out.println("Resultados guardados en: " + rutaResultados.toAbsolutePath());
    }

    private static Path buscarDirectorioResultados() throws IOException {
        Path directorioActual = Path.of("").toAbsolutePath();
        Path resultados = directorioActual.resolve("resultados");
        if (Files.isDirectory(resultados)) {
            return resultados;
        }

        Path directorioPadre = directorioActual.getParent();
        if (directorioPadre != null) {
            resultados = directorioPadre.resolve("resultados");
            if (Files.isDirectory(resultados)) {
                return resultados;
            }
        }

        throw new IOException(
                "No se encontro la carpeta resultados. Ejecute desde Practica_6 o Practica_6/java.");
    }

    private static void ejecutarPruebasUniformidad(Path directorioResultados)
            throws IOException {
        List<UniformityTest> pruebas = List.of(
                new ChiSquaredTest(INTERVALOS),
                new KolmogorovSmirnovTest());
        Path rutaResultados = directorioResultados.resolve("resultados_uniformidad_java.csv");
        double[] valoresGrafica = null;

        try (BufferedWriter escritor = Files.newBufferedWriter(rutaResultados)) {
            escritor.write(
                    "cantidad,frecuencias_observadas,frecuencia_esperada,"
                            + "chi_cuadrado,p_chi_cuadrado,decision_chi_cuadrado,"
                            + "estadistico_ks,p_ks,decision_ks,tiempo_total_segundos");
            escritor.newLine();

            for (int indice = 0; indice < TAMANOS_MUESTRA.length; indice++) {
                int cantidad = TAMANOS_MUESTRA[indice];
                long inicio = System.nanoTime();
                double[] valores = generarValores(cantidad);
                TestResult resultadoChi = pruebas.get(0).evaluate(valores);
                TestResult resultadoKs = pruebas.get(1).evaluate(valores);
                double tiempo = (System.nanoTime() - inicio) / 1_000_000_000.0;
                int[] frecuencias = contarFrecuencias(valores, INTERVALOS);

                escritor.write(String.format(
                        Locale.ROOT,
                        "%d,\"%s\",%s,%s,%s,%s,%s,%s,%s,%s",
                        cantidad,
                        frecuenciasComoTexto(frecuencias),
                        Double.toString((double) cantidad / INTERVALOS),
                        Double.toString(resultadoChi.statistic()),
                        Double.toString(resultadoChi.pValue()),
                        resultadoChi.decision(SIGNIFICANCIA),
                        Double.toString(resultadoKs.statistic()),
                        Double.toString(resultadoKs.pValue()),
                        resultadoKs.decision(SIGNIFICANCIA),
                        Double.toString(tiempo)));
                escritor.newLine();

                System.out.printf(
                        Locale.ROOT,
                        "%nCantidad de numeros: %,d%n"
                                + "Chi-cuadrado: estadistico=%.6f, p=%.6f, %s%n"
                                + "Kolmogorov-Smirnov: estadistico=%.6f, p=%.6f, %s%n"
                                + "Tiempo de generacion y pruebas: %.6f s%n",
                        cantidad,
                        resultadoChi.statistic(),
                        resultadoChi.pValue(),
                        resultadoChi.decision(SIGNIFICANCIA),
                        resultadoKs.statistic(),
                        resultadoKs.pValue(),
                        resultadoKs.decision(SIGNIFICANCIA),
                        tiempo);

                if (indice == TAMANOS_MUESTRA.length - 1) {
                    valoresGrafica = valores;
                }
            }
        }

        guardarGraficaKs(
                valoresGrafica,
                directorioResultados.resolve("ecdf_ks_java.svg"));
        System.out.println(
                "Resultados de uniformidad guardados en: "
                        + rutaResultados.toAbsolutePath());
        System.out.println(
                "Grafica KS guardada en: "
                        + directorioResultados.resolve("ecdf_ks_java.svg").toAbsolutePath());
    }

    private static double[] generarValores(int cantidad) {
        LCG generador = new LCG(SEMILLA, MULTIPLICADOR, INCREMENTO, MODULO);
        double[] valores = new double[cantidad];
        for (int indice = 0; indice < cantidad; indice++) {
            valores[indice] = generador.siguiente();
        }
        return valores;
    }

    private static int[] contarFrecuencias(double[] valores, int intervalos) {
        int[] frecuencias = new int[intervalos];
        for (double valor : valores) {
            frecuencias[(int) (valor * intervalos)]++;
        }
        return frecuencias;
    }

    private static String frecuenciasComoTexto(int[] frecuencias) {
        StringBuilder texto = new StringBuilder();
        for (int indice = 0; indice < frecuencias.length; indice++) {
            if (indice > 0) {
                texto.append(';');
            }
            texto.append(frecuencias[indice]);
        }
        return texto.toString();
    }

    private static void guardarGraficaKs(double[] valores, Path ruta)
            throws IOException {
        double[] ordenados = valores.clone();
        Arrays.sort(ordenados);
        int ancho = 800;
        int alto = 500;
        int margen = 60;
        StringBuilder empirica = new StringBuilder();
        int puntos = 2_000;

        for (int indice = 0; indice <= puntos; indice++) {
            int muestra = Math.min(
                    ordenados.length - 1,
                    (int) ((long) indice * ordenados.length / puntos));
            double x = margen + ordenados[muestra] * (ancho - 2.0 * margen);
            double y = alto - margen
                    - ((muestra + 1.0) / ordenados.length) * (alto - 2.0 * margen);
            empirica.append(indice == 0 ? "M " : " L ")
                    .append(String.format(Locale.ROOT, "%.2f %.2f", x, y));
        }

        String svg = """
                <svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500">
                  <rect width="800" height="500" fill="white"/>
                  <text x="400" y="28" text-anchor="middle" font-family="sans-serif" font-size="18">Prueba Kolmogorov-Smirnov</text>
                  <path d="M 60 440 L 740 60" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="8 6"/>
                  <path d="%s" fill="none" stroke="#2563eb" stroke-width="1.5"/>
                  <path d="M 60 60 L 60 440 L 740 440" fill="none" stroke="#333" stroke-width="1"/>
                  <text x="400" y="482" text-anchor="middle" font-family="sans-serif" font-size="14">Valor generado</text>
                  <text x="18" y="250" text-anchor="middle" font-family="sans-serif" font-size="14" transform="rotate(-90 18 250)">Probabilidad acumulada</text>
                  <text x="580" y="100" font-family="sans-serif" font-size="13" fill="#dc2626">Uniforme teorica</text>
                  <text x="580" y="122" font-family="sans-serif" font-size="13" fill="#2563eb">Acumulada empirica</text>
                </svg>
                """.formatted(empirica);
        Files.writeString(ruta, svg);
    }

    private static ResultadoPi estimarPi(int cantidad)
            throws NoSuchAlgorithmException {
        LCG generador = new LCG(SEMILLA, MULTIPLICADOR, INCREMENTO, MODULO);
        MessageDigest resumen = MessageDigest.getInstance("SHA-256");
        ByteBuffer estados = ByteBuffer.allocate(Long.BYTES * 2);
        int puntosDentro = 0;
        long inicio = System.nanoTime();

        for (int indice = 0; indice < cantidad; indice++) {
            long xEntero = generador.siguienteEntero();
            long yEntero = generador.siguienteEntero();
            estados.clear();
            estados.putLong(xEntero);
            estados.putLong(yEntero);
            resumen.update(estados.array());

            double x = (double) xEntero / generador.getModulo();
            double y = (double) yEntero / generador.getModulo();
            if (x * x + y * y <= 1) {
                puntosDentro++;
            }
        }

        double tiempo = (System.nanoTime() - inicio) / 1_000_000_000.0;
        double piEstimado = 4.0 * puntosDentro / cantidad;
        String hash = HexFormat.of().formatHex(resumen.digest());
        return new ResultadoPi(cantidad, puntosDentro, piEstimado, hash, tiempo);
    }

    private record ResultadoPi(
            int cantidadPuntos,
            int puntosDentro,
            double piEstimado,
            String sha256Secuencia,
            double tiempoSegundos) {}
}
