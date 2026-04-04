import { useState, useRef, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { Sun, Moon, Globe, User, LogOut, ChevronDown } from "lucide-react";
import { useTheme } from "@/shared/hooks/useTheme";
import { useAuth } from "@/shared/lib/auth";
import { changeLanguage, AVAILABLE_LANGUAGES } from "@/i18n";

export function TopBar() {
  const { t, i18n } = useTranslation();
  const { theme, toggleTheme } = useTheme();
  const { session, logout } = useAuth();

  return (
    <header className="sticky top-0 z-20 flex items-center justify-between h-14 px-6 bg-[var(--surface-card)] border-b border-[var(--border-default)]">
      <div />
      <div className="flex items-center gap-2">
        {/* Theme toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded-[var(--radius-md)] text-[var(--text-secondary)] hover:bg-[var(--color-neutral-100)] dark:hover:bg-[var(--color-neutral-800)] transition-colors"
          title={theme === "dark" ? t("shell.light_mode") : t("shell.dark_mode")}
        >
          {theme === "dark" ? (
            <Sun className="w-4.5 h-4.5" />
          ) : (
            <Moon className="w-4.5 h-4.5" />
          )}
        </button>

        {/* Language switcher */}
        <LanguageDropdown currentLang={i18n.language} />

        {/* User menu */}
        <UserMenu
          username={session.username || "User"}
          onLogout={logout}
        />
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

  const current = AVAILABLE_LANGUAGES.find((l) => l.code === currentLang);

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 px-2 py-2 rounded-[var(--radius-md)] text-sm text-[var(--text-secondary)] hover:bg-[var(--color-neutral-100)] dark:hover:bg-[var(--color-neutral-800)] transition-colors"
      >
        <Globe className="w-4.5 h-4.5" />
        <span className="hidden sm:inline">{current?.name || currentLang}</span>
      </button>

      {open && (
        <div className="absolute end-0 top-full mt-1 w-40 bg-[var(--surface-card)] border border-[var(--border-default)] rounded-[var(--radius-lg)] shadow-[var(--shadow-lg)] overflow-hidden">
          {AVAILABLE_LANGUAGES.map((lang) => (
            <button
              key={lang.code}
              onClick={() => {
                changeLanguage(lang.code);
                setOpen(false);
              }}
              className={`w-full px-3 py-2 text-sm text-start hover:bg-[var(--color-neutral-100)] dark:hover:bg-[var(--color-neutral-800)] transition-colors ${
                lang.code === currentLang
                  ? "text-[var(--color-primary-600)] font-medium"
                  : "text-[var(--text-primary)]"
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
}: {
  username: string;
  onLogout: () => void;
}) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const { t } = useTranslation();

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
        className="flex items-center gap-2 px-2 py-1.5 rounded-[var(--radius-md)] text-sm text-[var(--text-secondary)] hover:bg-[var(--color-neutral-100)] dark:hover:bg-[var(--color-neutral-800)] transition-colors"
      >
        <div className="w-7 h-7 rounded-full bg-[var(--color-primary-100)] dark:bg-[var(--color-primary-900)]/30 flex items-center justify-center">
          <User className="w-4 h-4 text-[var(--color-primary-600)]" />
        </div>
        <span className="hidden sm:inline font-medium text-[var(--text-primary)]">
          {username}
        </span>
        <ChevronDown className="w-3.5 h-3.5" />
      </button>

      {open && (
        <div className="absolute end-0 top-full mt-1 w-44 bg-[var(--surface-card)] border border-[var(--border-default)] rounded-[var(--radius-lg)] shadow-[var(--shadow-lg)] overflow-hidden">
          <button
            onClick={() => {
              setOpen(false);
              onLogout();
            }}
            className="flex items-center gap-2 w-full px-3 py-2 text-sm text-[var(--color-danger-600)] hover:bg-[var(--color-neutral-100)] dark:hover:bg-[var(--color-neutral-800)] transition-colors"
          >
            <LogOut className="w-4 h-4" />
            {t("auth.logout")}
          </button>
        </div>
      )}
    </div>
  );
}
