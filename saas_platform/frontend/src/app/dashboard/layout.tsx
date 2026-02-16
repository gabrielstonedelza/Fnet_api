"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [userName, setUserName] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.replace("/login");
      return;
    }
    try {
      const user = JSON.parse(localStorage.getItem("user") || "{}");
      setUserName(user.full_name || "Admin");
    } catch {
      setUserName("Admin");
    }
  }, [router]);

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("companyId");
    localStorage.removeItem("companies");
    router.replace("/login");
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navbar */}
      <nav className="bg-white border-b border-gray-200 px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-6">
            <Link href="/dashboard" className="text-xl font-bold text-blue-600">
              FNet Finance
            </Link>
            <div className="hidden md:flex items-center gap-4 text-sm">
              <Link
                href="/dashboard"
                className="text-gray-600 hover:text-blue-600 transition-colors"
              >
                Dashboard
              </Link>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">{userName}</span>
            <button
              onClick={handleLogout}
              className="text-sm text-red-600 hover:text-red-700"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Page Content */}
      <main className="p-6">{children}</main>
    </div>
  );
}
