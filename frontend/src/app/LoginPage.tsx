import { useState } from "react";
import { useNavigate } from "react-router";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/shared/lib/auth";
import { changeLanguage } from "@/i18n";
import {
  Loader2,
  AtSign,
  LockOpen,
  Eye,
  EyeOff,
  ChevronRight,
  ShieldCheck,
  Warehouse,
} from "lucide-react";

const LANGS = ["EN", "AZ", "RU", "TR"] as const;
const LANG_MAP: Record<string, string> = { EN: "en", AZ: "az", RU: "ru", TR: "tr" };

export function LoginPage() {
  const { i18n } = useTranslation();
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState("");

  const activeLang = i18n.language.toUpperCase().slice(0, 2);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      await login(email, password);
      navigate("/", { replace: true });
    } catch {
      setError("Invalid credentials. Please try again.");
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#0b1326] text-[#dae2fd] relative overflow-hidden">
      {/* Micro-pattern background */}
      <div
        className="absolute inset-0 pointer-events-none opacity-40"
        style={{
          backgroundImage:
            "radial-gradient(circle, rgba(99, 102, 241, 0.15) 1px, transparent 1px)",
          backgroundSize: "24px 24px",
        }}
      />

      {/* Background Soft Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-[#c0c1ff]/10 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-[#5de6ff]/5 blur-[120px] rounded-full pointer-events-none" />

      {/* Login Container */}
      <main className="relative z-10 w-full max-w-md px-6 py-12">
        {/* Header / Logo */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center gap-2 mb-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#c0c1ff] to-[#8083ff] flex items-center justify-center shadow-lg">
              <Warehouse className="w-7 h-7 text-[#0d0096]" />
            </div>
            <h1 className="text-2xl font-black tracking-tighter bg-gradient-to-br from-white to-[#c0c1ff] bg-clip-text text-transparent uppercase">
              GLTive Stock
            </h1>
          </div>
          <p className="text-[#908fa0] font-medium tracking-widest text-[0.6875rem] uppercase">
            Enterprise Stock Management
          </p>
        </div>

        {/* Login Card */}
        <div
          className="bg-[#131b2e]/70 backdrop-blur-2xl p-8 rounded-[1.5rem] border border-white/5"
          style={{ boxShadow: "0 0 80px -20px rgba(99, 102, 241, 0.3)" }}
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email Field */}
            <div className="space-y-2">
              <label
                className="text-xs font-semibold text-[#c7c4d7] uppercase tracking-wider block"
                htmlFor="email"
              >
                Email Address
              </label>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <AtSign className="w-5 h-5 text-[#908fa0] group-focus-within:text-[#c0c1ff] transition-colors" />
                </div>
                <input
                  id="email"
                  type="text"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoComplete="username"
                  autoFocus
                  required
                  className="block w-full bg-[#060e20] border-0 rounded-xl py-3.5 pl-11 pr-4 text-[#dae2fd] placeholder:text-[#908fa0]/50 focus:ring-2 focus:ring-[#c0c1ff]/50 transition-all text-sm"
                  placeholder="name@enterprise.com"
                />
                {/* Bottom accent line on focus */}
                <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-[#c0c1ff] scale-x-0 group-focus-within:scale-x-100 transition-transform origin-left rounded-full" />
              </div>
            </div>

            {/* Password Field */}
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <label
                  className="text-xs font-semibold text-[#c7c4d7] uppercase tracking-wider block"
                  htmlFor="password"
                >
                  Security Key
                </label>
                <a
                  href="#"
                  className="text-[0.6875rem] font-bold text-[#c0c1ff] hover:text-[#e1e0ff] transition-colors uppercase tracking-tight"
                >
                  Forgot password?
                </a>
              </div>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <LockOpen className="w-5 h-5 text-[#908fa0] group-focus-within:text-[#c0c1ff] transition-colors" />
                </div>
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                  required
                  className="block w-full bg-[#060e20] border-0 rounded-xl py-3.5 pl-11 pr-12 text-[#dae2fd] placeholder:text-[#908fa0]/50 focus:ring-2 focus:ring-[#c0c1ff]/50 transition-all text-sm"
                  placeholder="••••••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-4 flex items-center text-[#908fa0] hover:text-[#dae2fd] transition-colors"
                >
                  {showPassword ? (
                    <EyeOff className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </button>
                {/* Bottom accent line on focus */}
                <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-[#c0c1ff] scale-x-0 group-focus-within:scale-x-100 transition-transform origin-left rounded-full" />
              </div>
            </div>

            {/* Remember Me */}
            <div className="flex items-center">
              <div className="flex items-center h-5">
                <input
                  id="remember"
                  type="checkbox"
                  checked={remember}
                  onChange={(e) => setRemember(e.target.checked)}
                  className="w-4 h-4 text-[#c0c1ff] bg-[#060e20] border-white/10 rounded focus:ring-[#c0c1ff]/20 focus:ring-offset-0"
                />
              </div>
              <div className="ml-3 text-sm">
                <label
                  htmlFor="remember"
                  className="font-medium text-[#c7c4d7] select-none cursor-pointer"
                >
                  Remember this terminal
                </label>
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="p-3 rounded-lg bg-[#93000a]/20 border border-[#ffb4ab]/20">
                <p className="text-sm text-[#ffb4ab] font-medium">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-br from-[#c0c1ff] to-[#8083ff] text-[#0d0096] font-bold text-sm uppercase tracking-widest py-4 px-6 rounded-xl shadow-xl shadow-[#c0c1ff]/10 hover:shadow-[#c0c1ff]/20 hover:scale-[1.01] active:scale-[0.98] transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <>
                  Access Platform
                  <ChevronRight className="w-5 h-5" />
                </>
              )}
            </button>
          </form>

          {/* Language Support */}
          <div className="mt-8 pt-6 border-t border-white/5 flex justify-center items-center gap-6">
            {LANGS.map((lang) => (
              <button
                key={lang}
                onClick={() => changeLanguage(LANG_MAP[lang])}
                className={`text-[0.6875rem] font-bold tracking-tighter uppercase transition-colors ${
                  activeLang === lang
                    ? "text-[#c0c1ff]"
                    : "text-[#908fa0] hover:text-[#dae2fd]"
                }`}
              >
                {lang}
              </button>
            ))}
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-10 flex flex-col items-center gap-4">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 px-3 py-1 bg-[#00515d] rounded-full">
              <span className="w-1.5 h-1.5 bg-[#5de6ff] rounded-full animate-pulse" />
              <span className="text-[0.625rem] font-bold text-[#5de6ff] uppercase tracking-widest">
                System Status: Operational
              </span>
            </div>
          </div>
          <div className="flex items-center gap-2 text-[#908fa0]/60 text-[0.75rem] font-medium">
            <ShieldCheck className="w-4 h-4" />
            Multi-tenant secure access enabled
          </div>
        </div>
      </main>

      {/* Branding Element / Decorative */}
      <div className="fixed bottom-8 left-8 hidden lg:block opacity-20 pointer-events-none select-none">
        <div className="text-[8rem] font-black tracking-tighter leading-none text-white">
          G L T
        </div>
      </div>
    </div>
  );
}
