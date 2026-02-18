"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import {
  login,
  isCompanySelection,
  Company,
  LoginSuccessResponse,
} from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Multi-company selection state
  const [companies, setCompanies] = useState<Company[] | null>(null);
  const [selectedCompanyId, setSelectedCompanyId] = useState("");

  function storeLoginData(data: LoginSuccessResponse) {
    localStorage.setItem("token", data.token);
    localStorage.setItem("user", JSON.stringify(data.user));
    localStorage.setItem("membership", JSON.stringify(data.membership));
    // Store the active company ID from the membership
    localStorage.setItem("companyId", data.membership.company);
    localStorage.setItem("companyName", data.membership.company_name);
    localStorage.setItem("role", data.membership.role);
    if (data.companies) {
      localStorage.setItem("companies", JSON.stringify(data.companies));
    }
  }

  async function handleLogin(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await login(email, password);

      if (isCompanySelection(data)) {
        // User belongs to multiple companies — show the selector
        setCompanies(data.companies);
        setSelectedCompanyId(data.companies[0]?.id || "");
        return;
      }

      // Single company — go straight to dashboard
      storeLoginData(data);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  async function handleCompanySelect(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await login(email, password, selectedCompanyId);

      if (isCompanySelection(data)) {
        setError("Please select a company to continue.");
        return;
      }

      storeLoginData(data);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="w-full max-w-md">
        <div className="card">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-gray-900">
              SaaS Financial Platform
            </h1>
            <p className="text-gray-500 mt-2">
              {companies ? "Select your company" : "Sign in to your dashboard"}
            </p>
          </div>

          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm mb-4">
              {error}
            </div>
          )}

          {/* Company Selection Step */}
          {companies ? (
            <form onSubmit={handleCompanySelect} className="space-y-4">
              <p className="text-sm text-gray-600">
                You belong to multiple companies. Choose which one to sign into:
              </p>

              <div className="space-y-2">
                {companies.map((c) => (
                  <label
                    key={c.id}
                    className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${
                      selectedCompanyId === c.id
                        ? "border-blue-500 bg-blue-50"
                        : "border-gray-200 hover:bg-gray-50"
                    }`}
                  >
                    <input
                      type="radio"
                      name="company"
                      value={c.id}
                      checked={selectedCompanyId === c.id}
                      onChange={() => setSelectedCompanyId(c.id)}
                      className="text-blue-600"
                    />
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {c.name}
                      </p>
                      <p className="text-xs text-gray-500 capitalize">
                        Role: {c.role}
                      </p>
                    </div>
                  </label>
                ))}
              </div>

              <button
                type="submit"
                disabled={loading || !selectedCompanyId}
                className="btn-primary w-full disabled:opacity-50"
              >
                {loading ? "Signing in..." : "Continue"}
              </button>

              <button
                type="button"
                onClick={() => {
                  setCompanies(null);
                  setError("");
                }}
                className="btn-secondary w-full"
              >
                Back
              </button>
            </form>
          ) : (
            /* Login Form */
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="input-field"
                  placeholder="admin@example.com"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Password
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input-field"
                  placeholder="Enter your password"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn-primary w-full disabled:opacity-50"
              >
                {loading ? "Signing in..." : "Sign In"}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
