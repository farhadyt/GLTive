import { useState } from "react";
import { useNavigate } from "react-router";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/shared/lib/auth";
import { changeLanguage } from "@/i18n";
import { Lock, AtSign, Eye, EyeOff, Loader2, ChevronRight, Shield, ShieldCheck } from "lucide-react";

const LANGS = ["EN", "AZ", "RU", "TR"] as const;
const LANG_MAP: Record<string, string> = { EN: "en", AZ: "az", RU: "ru", TR: "tr" };

export function LoginPage() {
  const { t, i18n } = useTranslation();
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState("");

  const activeLang = i18n.language.toUpperCase().slice(0, 2);

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
    <div className="min-h-screen flex items-center justify-center bg-[var(--surface)] relative overflow-hidden">
      {/* Outer frame border */}
      <div className="absolute inset-3 rounded-2xl border border-[var(--color-outline-variant)]/30 pointer-events-none" />

      {/* Subtle background glow */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] bg-[var(--color-primary-container)] rounded-full opacity-[0.03] blur-[150px] pointer-events-none" />

      {/* GLT watermark — bottom left */}
      <div className="absolute bottom-8 left-8 text-[120px] font-black text-white/[0.04] leading-none tracking-tighter select-none pointer-events-none">
        GLT
      </div>

      {/* Main content */}
      <div className="w-full max-w-[440px] relative z-10 px-4">
        {/* Logo */}
        <div className="flex items-center justify-center gap-3 mb-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-primary-container)] flex items-center justify-center shadow-lg shadow-[var(--color-primary)]/20">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <span className="text-2xl font-black text-white tracking-tight">
            GLTIVE STOCK
          </span>
        </div>
        <p className="text-center text-[11px] font-bold uppercase tracking-[0.25em] text-[var(--color-primary)] mb-10">
          Enterprise Stock Management
        </p>

        {/* Form card */}
        <div className="relative">
          {/* Dashed border effect */}
          <div className="absolute -inset-px rounded-2xl border border-dashed border-[var(--color-outline-variant)]/30 pointer-events-none" />

          <form
            onSubmit={handleSubmit}
            className="bg-[var(--surface-container-low)]/80 backdrop-blur-sm rounded-2xl p-8 space-y-5"
          >
            {/* Email / Username field */}
            <div className="flex flex-col gap-2">
              <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[var(--color-on-surface-variant)]">
                Email Address
              </label>
              <div className="relative">
                <AtSign className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--color-outline)]" />
                <input
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  autoComplete="username"
                  autoFocus
                  required
                  className="w-full pl-10 pr-4 py-3 text-sm rounded-lg bg-[var(--surface-container)] text-[var(--color-on-surface)] placeholder:text-[var(--color-outline)] border border-[var(--color-outline-variant)]/20 focus:outline-none focus:border-[var(--color-primary-container)] transition-all"
                  placeholder="name@enterprise.com"
                />
              </div>
            </div>

            {/* Password field */}
            <div className="flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <label className="text-[10px] font-black uppercase tracking-[0.2em] text-[var(--color-on-surface-variant)]">
                  Security Key
                </label>
                <button
                  type="button"
                  className="text-[10px] font-bold uppercase tracking-wider text-[var(--color-primary)] hover:text-[var(--color-primary-container)] transition-colors"
                >
                  Forgot Password?
                </button>
              </div>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--color-outline)]" />
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                  required
                  className="w-full pl-10 pr-10 py-3 text-sm rounded-lg bg-[var(--surface-container)] text-[var(--color-on-surface)] placeholder:text-[var(--color-outline)] border border-[var(--color-outline-variant)]/20 focus:outline-none focus:border-[var(--color-primary-container)] transition-all"
                  placeholder="••••••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[var(--color-outline)] hover:text-[var(--color-on-surface-variant)] transition-colors"
                >
                  {showPassword ? (
                    <EyeOff className="w-4 h-4" />
                  ) : (
                    <Eye className="w-4 h-4" />
                  )}
                </button>
              </div>
            </div>

            {/* Remember checkbox */}
            <label className="flex items-center gap-2.5 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={remember}
                onChange={(e) => setRemember(e.target.checked)}
                className="w-4 h-4 rounded border-[var(--color-outline-variant)]/30 bg-[var(--surface-container)] text-[var(--color-primary-container)] focus:ring-[var(--color-primary-container)] focus:ring-offset-0"
              />
              <span className="text-sm text-[var(--color-on-surface-variant)]">
                Remember this terminal
              </span>
            </label>

            {/* Error */}
            {error && (
              <div className="p-3 rounded-lg bg-[var(--color-error-container)]/10 border border-[var(--color-error)]/20">
                <p className="text-sm text-[var(--color-error)] font-medium">{error}</p>
              </div>
            )}

            {/* Submit button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3.5 btn-primary-gradient font-bold rounded-xl flex items-center justify-center gap-2 text-sm disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:shadow-lg hover:shadow-[var(--color-primary)]/20 active:scale-[0.98] border border-[var(--color-primary)]/20 uppercase tracking-wider"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <>
                  Access Platform
                  <ChevronRight className="w-4 h-4" />
                </>
              )}
            </button>

            {/* Language selector */}
            <div className="flex items-center justify-center gap-4 pt-2">
              {LANGS.map((lang) => (
                <button
                  key={lang}
                  type="button"
                  onClick={() => changeLanguage(LANG_MAP[lang])}
                  className={`text-xs font-bold tracking-wider transition-colors ${
                    activeLang === lang
                      ? "text-[var(--color-primary)]"
                      : "text-[var(--color-outline)] hover:text-[var(--color-on-surface-variant)]"
                  }`}
                >
                  {lang}
                </button>
              ))}
            </div>
          </form>
        </div>

        {/* System status */}
        <div className="flex flex-col items-center mt-8 gap-2">
          <div className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-[var(--color-on-secondary-container)]/80 border border-[var(--color-secondary)]/20">
            <span className="w-2 h-2 rounded-full bg-[var(--color-secondary)] animate-pulse-dot" />
            <span className="text-[10px] font-black uppercase tracking-[0.15em] text-[var(--color-secondary)]">
              System Status: Operational
            </span>
          </div>
          <div className="flex items-center gap-1.5 text-[var(--color-outline)]">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span className="text-[11px]">Multi-tenant secure access enabled</span>
          </div>
        </div>
      </div>
    </div>
  );
}
