/** @type {import('next').NextConfig} */
const nextConfig = {
  // Proxy API requests to Django backend during development
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/api/:path*",
      },
      {
        source: "/ws/:path*",
        destination: "http://localhost:8000/ws/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
