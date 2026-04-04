import { useState } from "react";
import { useNavigate } from "react-router";
import { useTranslation } from "react-i18next";
import { useAuth } from "@/shared/lib/auth";
import { Button, Input } from "@/shared/ui";
import { LogIn } from "lucide-react";

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
    <div className="min-h-screen flex items-center justify-center bg-[var(--surface-bg)] px-4">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-[var(--color-primary-600)] flex items-center justify-center mb-4 shadow-[var(--shadow-lg)]">
            <span className="text-white font-bold text-2xl">G</span>
          </div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">
            {t("auth.login_title")}
          </h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            {t("auth.login_subtitle")}
          </p>
        </div>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="bg-[var(--surface-card)] border border-[var(--border-default)] rounded-[var(--radius-xl)] p-6 shadow-[var(--shadow-md)] space-y-4"
        >
          <Input
            label={t("auth.username")}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            autoFocus
            required
          />
          <Input
            label={t("auth.password")}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
          {error && (
            <p className="text-sm text-[var(--color-danger-500)] text-center">
              {error}
            </p>
          )}
          <Button
            type="submit"
            loading={isLoading}
            icon={<LogIn className="w-4 h-4" />}
            className="w-full"
          >
            {t("auth.login")}
          </Button>
        </form>
      </div>
    </div>
  );
}
