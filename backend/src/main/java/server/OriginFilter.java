package server;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

/** Enforce exact browser origins before HTTP handling or WebSocket upgrade. */
public class OriginFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        String origin = ((HttpServletRequest) request).getHeader("Origin");
        // Non-browser health checks and server clients may omit Origin.
        if (origin != null && !ApplicationConfig.PUBLIC_ORIGIN.equals(origin)) {
            ((HttpServletResponse) response).sendError(403, "Origin not allowed");
            return;
        }
        chain.doFilter(request, response);
    }
}
