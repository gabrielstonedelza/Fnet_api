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
    <div className="min-h-screen bg-gray-50">
      {/* Top Navbar */}
      <nav className="bg-white border-b border-gray-200 px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-6">
            <Link href="/dashboard" className="text-xl font-bold text-blue-600">
              Merchant+
            </Link>
            {companyName && (
              <span className="hidden md:inline text-sm text-gray-500 border-l border-gray-200 pl-4">
                {companyName}
              </span>
            )}
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-700">{userName}</p>
              {role && (
                <p className="text-xs text-gray-400 capitalize">{role}</p>
              )}
            </div>
            <button
              onClick={handleLogout}
              className="text-sm text-red-600 hover:text-red-700 font-medium"
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
