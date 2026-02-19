"use client";

import { useState, FormEvent, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  login,
  verify2FA,
  isCompanySelection,
  isTwoFactorRequired,
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

  // 2FA state
  const [requires2FA, setRequires2FA] = useState(false);
  const [tempToken, setTempToken] = useState("");
  const [totpCode, setTotpCode] = useState(["", "", "", "", "", ""]);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  // Auto-focus first OTP input when 2FA screen shows
  useEffect(() => {
    if (requires2FA && inputRefs.current[0]) {
      inputRefs.current[0].focus();
    }
  }, [requires2FA]);

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

      if (isTwoFactorRequired(data)) {
        setTempToken(data.temp_token);
        setRequires2FA(true);
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

      if (isTwoFactorRequired(data)) {
        setTempToken(data.temp_token);
        setRequires2FA(true);
        setCompanies(null);
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

  function handleOtpChange(index: number, value: string) {
    if (!/^\d*$/.test(value)) return;

    const newCode = [...totpCode];
    newCode[index] = value.slice(-1);
    setTotpCode(newCode);

    // Auto-advance to next input
    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }

    // Auto-submit when all 6 digits entered
    const fullCode = newCode.join("");
    if (fullCode.length === 6) {
      handle2FAVerify(fullCode);
    }
  }

  function handleOtpKeyDown(index: number, e: React.KeyboardEvent) {
    if (e.key === "Backspace" && !totpCode[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  }

  function handleOtpPaste(e: React.ClipboardEvent) {
    e.preventDefault();
    const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, 6);
    if (pasted.length === 0) return;

    const newCode = [...totpCode];
    for (let i = 0; i < 6; i++) {
      newCode[i] = pasted[i] || "";
    }
    setTotpCode(newCode);

    if (pasted.length === 6) {
      handle2FAVerify(pasted);
    } else {
      inputRefs.current[pasted.length]?.focus();
    }
  }

  async function handle2FAVerify(code?: string) {
    const verifyCode = code || totpCode.join("");
    if (verifyCode.length < 6) {
      setError("Enter your 6-digit authenticator code.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const data = await verify2FA(tempToken, verifyCode);
      storeLoginData(data);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Invalid code");
      setTotpCode(["", "", "", "", "", ""]);
      inputRefs.current[0]?.focus();
    } finally {
      setLoading(false);
    }
  }

  async function handleBackupCode(e: FormEvent) {
    e.preventDefault();
    const backupInput = document.getElementById("backup-code") as HTMLInputElement;
    const code = backupInput?.value?.trim();
    if (!code) {
      setError("Enter your backup code.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const data = await verify2FA(tempToken, code);
      storeLoginData(data);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Invalid backup code");
    } finally {
      setLoading(false);
    }
  }

  // Determine current view
  const currentView = requires2FA
    ? "2fa"
    : companies
    ? "company"
    : "login";

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
              {currentView === "2fa"
                ? "Two-factor authentication"
                : currentView === "company"
                ? "Select your company"
                : "Sign in to your dashboard"}
            </p>
          </div>

          {error && (
            <div className="bg-red-900/30 text-red-400 border border-red-800/30 p-3 rounded-lg text-sm mb-4">
              {error}
            </div>
          )}

          {/* ---- 2FA Verification ---- */}
          {currentView === "2fa" && (
            <div className="space-y-6">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gold/10 border border-gold/20 mb-3">
                  <svg className="w-6 h-6 text-gold" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <p className="text-sm text-dark-200">
                  Enter the 6-digit code from your authenticator app
                </p>
              </div>

              {/* OTP Input */}
              <div className="flex justify-center gap-2" onPaste={handleOtpPaste}>
                {totpCode.map((digit, i) => (
                  <input
                    key={i}
                    ref={(el) => { inputRefs.current[i] = el; }}
                    type="text"
                    inputMode="numeric"
                    maxLength={1}
                    value={digit}
                    onChange={(e) => handleOtpChange(i, e.target.value)}
                    onKeyDown={(e) => handleOtpKeyDown(i, e)}
                    className="w-12 h-14 text-center text-xl font-bold bg-dark-500 border border-dark-400 text-dark-50 rounded-lg focus:ring-2 focus:ring-gold focus:border-gold outline-none"
                    disabled={loading}
                  />
                ))}
              </div>

              <button
                onClick={() => handle2FAVerify()}
                disabled={loading || totpCode.join("").length < 6}
                className="btn-primary w-full disabled:opacity-50"
              >
                {loading ? "Verifying..." : "Verify"}
              </button>

              {/* Backup code option */}
              <details className="group">
                <summary className="text-sm text-dark-300 cursor-pointer hover:text-gold transition-colors text-center">
                  Use a backup code instead
                </summary>
                <form onSubmit={handleBackupCode} className="mt-3 space-y-3">
                  <input
                    id="backup-code"
                    type="text"
                    className="input-field text-center tracking-widest uppercase"
                    placeholder="A1B2C3D4"
                    maxLength={8}
                  />
                  <button
                    type="submit"
                    disabled={loading}
                    className="btn-secondary w-full disabled:opacity-50"
                  >
                    {loading ? "Verifying..." : "Verify Backup Code"}
                  </button>
                </form>
              </details>

              <button
                type="button"
                onClick={() => {
                  setRequires2FA(false);
                  setTempToken("");
                  setTotpCode(["", "", "", "", "", ""]);
                  setError("");
                }}
                className="btn-secondary w-full"
              >
                Back to login
              </button>
            </div>
          )}

          {/* ---- Company Selection ---- */}
          {currentView === "company" && companies && (
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
          )}

          {/* ---- Login Form ---- */}
          {currentView === "login" && (
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
