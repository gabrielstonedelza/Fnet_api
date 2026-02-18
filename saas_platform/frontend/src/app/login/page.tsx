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
        setCompanies(data.companies);
        setSelectedCompanyId(data.companies[0]?.id || "");
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
    <div className="min-h-screen flex items-center justify-center bg-dark">
      {/* Subtle radial gold glow */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gold/5 rounded-full blur-3xl" />
      </div>

      <div className="w-full max-w-md relative z-10">
        <div className="card glow-gold">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gold mb-4">
              <span className="text-dark text-2xl font-black">M+</span>
            </div>
            <h1 className="text-2xl font-bold text-dark-50">
              Merchant+
            </h1>
            <p className="text-dark-200 mt-2">
              {companies ? "Select your company" : "Sign in to your dashboard"}
            </p>
          </div>

          {error && (
            <div className="bg-red-900/30 text-red-400 border border-red-800/30 p-3 rounded-lg text-sm mb-4">
              {error}
            </div>
          )}

          {companies ? (
            <form onSubmit={handleCompanySelect} className="space-y-4">
              <p className="text-sm text-dark-200">
                You belong to multiple companies. Choose which one to sign into:
              </p>

              <div className="space-y-2">
                {companies.map((c) => (
                  <label
                    key={c.id}
                    className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${
                      selectedCompanyId === c.id
                        ? "border-gold bg-gold/10"
                        : "border-dark-400 hover:bg-dark-500"
                    }`}
                  >
                    <input
                      type="radio"
                      name="company"
                      value={c.id}
                      checked={selectedCompanyId === c.id}
                      onChange={() => setSelectedCompanyId(c.id)}
                      className="accent-gold"
                    />
                    <div>
                      <p className="text-sm font-medium text-dark-50">
                        {c.name}
                      </p>
                      <p className="text-xs text-dark-300 capitalize">
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
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-dark-200 mb-1">
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
                <label className="block text-sm font-medium text-dark-200 mb-1">
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
