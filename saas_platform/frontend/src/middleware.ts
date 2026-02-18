import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/**
 * Merchant+ Security Middleware
 *
 * OWASP-aligned security headers for the Next.js frontend.
 * Maps to Security+ domains:
 *   - 1.0 Threats, Attacks, and Vulnerabilities (XSS, clickjacking)
 *   - 3.0 Architecture and Design (defense-in-depth)
 *   - 4.0 Implementation (secure headers, CSP, HSTS)
 */
export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // Strict-Transport-Security — force HTTPS for 1 year + preload
  response.headers.set(
    "Strict-Transport-Security",
    "max-age=31536000; includeSubDomains; preload"
  );

  // Content-Security-Policy — restrict resource origins
  response.headers.set(
    "Content-Security-Policy",
    [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' 'unsafe-eval'", // Next.js requires inline scripts
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: blob:",
      "font-src 'self' data:",
      "connect-src 'self' ws: wss: http://localhost:* https://merchantplusgh.com",
      "frame-ancestors 'none'", // Clickjacking prevention
      "base-uri 'self'",
      "form-action 'self'",
    ].join("; ")
  );

  // Prevent MIME-type sniffing
  response.headers.set("X-Content-Type-Options", "nosniff");

  // Prevent clickjacking (legacy, CSP frame-ancestors is preferred)
  response.headers.set("X-Frame-Options", "DENY");

  // Referrer policy — don't leak URLs to third parties
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");

  // Permissions-Policy — disable unused browser features
  response.headers.set(
    "Permissions-Policy",
    "camera=(), microphone=(), geolocation=(), interest-cohort=()"
  );

  // Prevent search engines from caching sensitive pages
  if (request.nextUrl.pathname.startsWith("/dashboard")) {
    response.headers.set(
      "Cache-Control",
      "no-store, no-cache, must-revalidate, proxy-revalidate"
    );
    response.headers.set("Pragma", "no-cache");
    response.headers.set("Expires", "0");
  }

  return response;
}

export const config = {
  matcher: [
    // Apply to all routes except static files and API proxy
    "/((?!_next/static|_next/image|favicon.ico).*)",
  ],
};
