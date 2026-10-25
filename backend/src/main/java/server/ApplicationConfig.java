package server;

public class ApplicationConfig {
    private static final String ENV_DEBUG = "DEBUG_MODE";
    private static final String ENV_DATABASE_URL = "DATABASE_URL";

    public static boolean DEBUG = System.getenv(ENV_DEBUG) != null;
    public static String DATABASE_URI = System.getenv(ENV_DATABASE_URL);
    // Preserve the live deployment's configurable public origin, with a safe default.
    public static final String PUBLIC_ORIGIN = publicOrigin();

    private static String publicOrigin() {
        String value = System.getenv("PUBLIC_ORIGIN");
        if (value == null || value.isBlank()) value = "https://secret-hitler.ashayc.com";
        java.net.URI uri = java.net.URI.create(value);
        if (!"https".equals(uri.getScheme()) || uri.getHost() == null
                || uri.getRawUserInfo() != null || uri.getRawQuery() != null
                || uri.getRawFragment() != null || !uri.getRawPath().isEmpty()
                || value.contains("*")) {
            throw new IllegalArgumentException("PUBLIC_ORIGIN must be an exact HTTPS origin without path");
        }
        return value;
    }
}
