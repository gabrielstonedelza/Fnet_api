import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Merchant+ | Admin Dashboard",
  description: "Merchant+ — Financial transaction management for agents and merchants",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
