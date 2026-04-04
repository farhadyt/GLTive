import { useState } from "react";
import { useNavigate } from "react-router";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/shared/lib/auth";
import { changeLanguage, AVAILABLE_LANGUAGES } from "@/i18n";
import { LogIn, Loader2, Globe, ChevronDown } from "lucide-react";

export function LoginPage() {
  const { t, i18n } = useTranslation();
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [langOpen, setLangOpen] = useState(false);

  const currentLang = AVAILABLE_LANGUAGES.find((l) => l.code === i18n.language);

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
    <div className="min-h-screen flex items-center justify-center bg-[var(--surface)] px-4 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Radial gradient glow — primary */}
        <div className="absolute top-1/4 left-1/3 w-[600px] h-[600px] bg-[var(--color-primary-container)] rounded-full opacity-[0.04] blur-[120px]" />
        {/* Radial gradient glow — secondary */}
        <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-[var(--color-secondary)] rounded-full opacity-[0.03] blur-[100px]" />
        {/* Subtle grid pattern */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage:
              "linear-gradient(var(--color-outline) 1px, transparent 1px), linear-gradient(90deg, var(--color-outline) 1px, transparent 1px)",
            backgroundSize: "64px 64px",
          }}
        />
      </div>

      {/* Language Selector — Top Right */}
      <div className="absolute top-6 right-6 z-10">
        <div className="relative">
          <button
            onClick={() => setLangOpen(!langOpen)}
            className="flex items-center gap-2 px-3 py-2 rounded-xl bg-[var(--surface-container)] hover:bg-[var(--surface-container-high)] text-[var(--color-on-surface-variant)] text-sm font-medium transition-all border border-white/5"
          >
            <Globe className="w-4 h-4" />
            <span>{currentLang?.name || i18n.language}</span>
            <ChevronDown className={`w-3.5 h-3.5 transition-transform ${langOpen ? "rotate-180" : ""}`} />
          </button>
          {langOpen && (
            <div className="absolute end-0 top-full mt-2 w-44 bg-[var(--surface-container-highest)] border border-white/5 rounded-xl shadow-2xl shadow-black/40 overflow-hidden backdrop-blur-xl z-20">
              {AVAILABLE_LANGUAGES.map((lang) => (
                <button
                  key={lang.code}
                  onClick={() => {
                    changeLanguage(lang.code);
                    setLangOpen(false);
                  }}
                  className={`w-full px-4 py-2.5 text-sm text-start hover:bg-white/5 transition-colors ${
                    lang.code === i18n.language
                      ? "text-[var(--color-primary)] font-semibold"
                      : "text-[var(--color-on-surface)]"
                  }`}
                >
                  {lang.name}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Login Card */}
      <div className="w-full max-w-[420px] relative z-10">
        {/* Logo & Title */}
        <div className="flex flex-col items-center mb-10">
          <div className="w-20 h-20 rounded-2xl btn-primary-gradient flex items-center justify-center mb-6 shadow-2xl shadow-[var(--color-primary)]/30 relative">
            <span className="text-white font-black text-3xl">G</span>
            {/* Pulse ring effect */}
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-primary-container)] opacity-30 animate-ping" style={{ animationDuration: "3s" }} />
          </div>
          <h1 className="text-3xl font-black text-white tracking-tight mb-1">
            GLTive
          </h1>
          <p className="text-sm text-[var(--color-outline)] font-medium tracking-wide">
            {t("auth.login_subtitle")}
          </p>
        </div>

        {/* Form Container */}
        <div className="bg-[var(--surface-container-low)] rounded-2xl p-8 border border-white/5 shadow-2xl shadow-black/30 relative overflow-hidden">
          {/* Subtle top accent line */}
          <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-[var(--color-primary-container)] to-transparent opacity-50" />

          <h2 className="text-lg font-bold text-white mb-1 text-center">
            {t("auth.login_title")}
          </h2>
          <p className="text-xs text-[var(--color-outline)] text-center mb-8">
            Access your operations control center
          </p>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="flex flex-col gap-2">
              <label className="text-[10px] font-bold uppercase tracking-[0.15em] text-[var(--color-outline)]">
                {t("auth.username")}
              </label>
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoComplete="username"
                autoFocus
                required
                className="w-full px-4 py-3.5 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] placeholder:text-[var(--color-outline-variant)] border border-white/5 focus:outline-none focus:border-[var(--color-primary-container)] focus:ring-1 focus:ring-[var(--color-primary-container)] transition-all"
                placeholder="Enter your username"
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-[10px] font-bold uppercase tracking-[0.15em] text-[var(--color-outline)]">
                {t("auth.password")}
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                required
                className="w-full px-4 py-3.5 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] placeholder:text-[var(--color-outline-variant)] border border-white/5 focus:outline-none focus:border-[var(--color-primary-container)] focus:ring-1 focus:ring-[var(--color-primary-container)] transition-all"
                placeholder="Enter your password"
              />
            </div>

            {error && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-[var(--color-error-container)]/10 border border-[var(--color-error)]/20">
                <p className="text-sm text-[var(--color-error)] font-medium">
                  {error}
                </p>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3.5 btn-primary-gradient font-bold rounded-xl flex items-center justify-center gap-2.5 shadow-lg shadow-[var(--color-primary)]/20 text-sm disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:shadow-xl hover:shadow-[var(--color-primary)]/30 active:scale-[0.98]"
            >
              {isLoading ? (
                <Loader2 className="w-4.5 h-4.5 animate-spin" />
              ) : (
                <LogIn className="w-4.5 h-4.5" />
              )}
              {t("auth.login")}
            </button>
          </form>
        </div>

        {/* Footer */}
        <p className="text-center text-[10px] text-[var(--color-outline-variant)] mt-6 tracking-wide uppercase">
          GLTive Platform v0.8 &bull; Industrial Architect
        </p>
      </div>
    </div>
  );
}
