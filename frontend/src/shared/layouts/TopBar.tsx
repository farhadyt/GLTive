import { useState, useRef, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { Globe, Bell, User } from "lucide-react";
import { useAuth } from "@/shared/lib/auth";
import { changeLanguage, AVAILABLE_LANGUAGES } from "@/i18n";

export function TopBar() {
  const { t, i18n } = useTranslation();
  const { session, logout } = useAuth();

  return (
    <header className="fixed top-0 right-0 left-0 z-50 flex items-center justify-between px-6 glass h-[56px] border-b border-white/5 shadow-2xl shadow-black/20">
      <div className="flex items-center gap-4">
        <span className="text-lg font-bold tracking-tighter text-white">
          GLTive Stock Manager
        </span>
      </div>
      <div className="flex items-center gap-2">
        <button className="p-2 hover:bg-white/5 transition-all duration-200 rounded-lg text-slate-400">
          <Bell className="w-5 h-5" />
        </button>
        <LanguageDropdown currentLang={i18n.language} />
        <UserMenu username={session.username} onLogout={logout} t={t} />
      </div>
    </header>
  );
}

function LanguageDropdown({ currentLang }: { currentLang: string }) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen(!open)}
        className="p-2 hover:bg-white/5 transition-all duration-200 rounded-lg text-slate-400"
      >
        <Globe className="w-5 h-5" />
      </button>
      {open && (
        <div className="absolute end-0 top-full mt-2 w-40 bg-[var(--surface-container-highest)] border border-white/5 rounded-xl shadow-2xl shadow-black/30 overflow-hidden">
          {AVAILABLE_LANGUAGES.map((lang) => (
            <button
              key={lang.code}
              onClick={() => {
                changeLanguage(lang.code);
                setOpen(false);
              }}
              className={`w-full px-4 py-2.5 text-sm text-start hover:bg-white/5 transition-colors ${
                lang.code === currentLang
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
  );
}

function UserMenu({
  username,
  onLogout,
  t,
}: {
  username: string | null;
  onLogout: () => void;
  t: (key: string) => string;
}) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen(!open)}
        className="w-8 h-8 rounded-full bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-primary-container)] flex items-center justify-center ml-2 cursor-pointer"
      >
        <User className="w-4 h-4 text-white" />
      </button>
      {open && (
        <div className="absolute end-0 top-full mt-2 w-48 bg-[var(--surface-container-highest)] border border-white/5 rounded-xl shadow-2xl shadow-black/30 overflow-hidden">
          {username && (
            <div className="px-4 py-3 border-b border-white/5">
              <p className="text-sm font-semibold text-white truncate">{username}</p>
            </div>
          )}
          <button
            onClick={() => {
              setOpen(false);
              onLogout();
            }}
            className="flex items-center gap-2 w-full px-4 py-2.5 text-sm text-[var(--color-error)] hover:bg-white/5 transition-colors"
          >
            {t("auth.logout")}
          </button>
        </div>
      )}
    </div>
  );
}
