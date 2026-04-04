import { useState } from "react";
import { useNavigate } from "react-router";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/shared/lib/auth";
import { LogIn, Loader2 } from "lucide-react";

export function LoginPage() {
  const { t } = useTranslation();
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      await login(username, password);
      navigate("/", { replace: true });
    } catch {
      setError(t("auth.login_error"));
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--surface)] px-4">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="flex flex-col items-center mb-10">
          <div className="w-16 h-16 rounded-2xl btn-primary-gradient flex items-center justify-center mb-5 shadow-lg shadow-[var(--color-primary)]/20">
            <span className="text-white font-black text-2xl">G</span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">
            {t("auth.login_title")}
          </h1>
          <p className="text-sm text-[var(--color-outline)] mt-1">
            {t("auth.login_subtitle")}
          </p>
        </div>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="bg-[var(--surface-container-low)] rounded-2xl p-8 space-y-5 border border-white/5"
        >
          <div className="flex flex-col gap-2">
            <label className="text-xs font-bold uppercase tracking-widest text-[var(--color-outline)]">
              {t("auth.username")}
            </label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              autoFocus
              required
              className="w-full px-4 py-3 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] placeholder:text-[var(--color-outline)] border-none focus:outline-none focus:ring-2 focus:ring-[var(--color-primary-container)] transition-all"
              placeholder={t("auth.username")}
            />
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-xs font-bold uppercase tracking-widest text-[var(--color-outline)]">
              {t("auth.password")}
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
              className="w-full px-4 py-3 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] placeholder:text-[var(--color-outline)] border-none focus:outline-none focus:ring-2 focus:ring-[var(--color-primary-container)] transition-all"
              placeholder={t("auth.password")}
            />
          </div>
          {error && (
            <p className="text-sm text-[var(--color-error)] text-center font-medium">
              {error}
            </p>
          )}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 btn-primary-gradient font-semibold rounded-xl flex items-center justify-center gap-2 shadow-lg shadow-[var(--color-primary)]/20 text-sm disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <LogIn className="w-4 h-4" />
            )}
            {t("auth.login")}
          </button>
        </form>
      </div>
    </div>
  );
}
