import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router";
import { FileQuestion } from "lucide-react";

export function NotFoundPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
      <FileQuestion className="w-20 h-20 text-[var(--color-outline)]/30 mb-6" />
      <h2 className="text-2xl font-bold text-white mb-2">{t("common.not_found")}</h2>
      <p className="text-sm text-[var(--color-outline)] mb-6 max-w-sm">{t("common.not_found_desc")}</p>
      <button
        onClick={() => navigate("/")}
        className="bg-[var(--surface-container-highest)] text-white px-5 py-2.5 rounded-xl text-sm font-medium hover:bg-[var(--surface-bright)] transition-colors"
      >
        {t("common.back")}
      </button>
    </div>
  );
}
