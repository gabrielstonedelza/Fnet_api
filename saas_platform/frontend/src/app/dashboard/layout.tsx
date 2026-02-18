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
  const [companyName, setCompanyName] = useState("");
  const [role, setRole] = useState("");

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
    setCompanyName(localStorage.getItem("companyName") || "");
    setRole(localStorage.getItem("role") || "");
  }, [router]);

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("membership");
    localStorage.removeItem("companyId");
    localStorage.removeItem("companyName");
    localStorage.removeItem("role");
    localStorage.removeItem("companies");
    router.replace("/login");
  }

  return (
    <div className="min-h-screen bg-dark">
      {/* Top Navbar */}
      <nav className="bg-dark-600 border-b border-dark-400 px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-6">
            <Link href="/dashboard" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gold flex items-center justify-center">
                <span className="text-dark text-sm font-black">M+</span>
              </div>
              <span className="text-xl font-bold text-gold">Merchant+</span>
            </Link>
            {companyName && (
              <span className="hidden md:inline text-sm text-dark-200 border-l border-dark-400 pl-4">
                {companyName}
              </span>
            )}
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium text-dark-50">{userName}</p>
              {role && (
                <p className="text-xs text-dark-300 capitalize">{role}</p>
              )}
            </div>
            <button
              onClick={handleLogout}
              className="text-sm text-red-400 hover:text-red-300 font-medium transition-colors"
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
