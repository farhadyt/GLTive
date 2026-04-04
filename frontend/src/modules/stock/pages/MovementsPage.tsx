import { useTranslation } from "react-i18next";
import { History, ChevronRight } from "lucide-react";

export function MovementsPage() {
  const { t } = useTranslation();

  return (
    <>
      <div className="mb-8">
        <nav className="flex items-center gap-2 text-[var(--color-outline)] text-xs font-medium uppercase tracking-wider mb-2">
          <span>{t("nav.stock")}</span>
          <ChevronRight className="w-3 h-3" />
          <span className="text-[var(--color-primary)]">{t("nav.movements")}</span>
        </nav>
        <h1 className="text-3xl font-bold text-white tracking-tight">
          {t("nav.movements")}
        </h1>
      </div>
      <div className="bg-[var(--surface-container-low)] rounded-2xl p-16 flex flex-col items-center justify-center text-center">
        <History className="w-16 h-16 text-[var(--color-outline)]/30 mb-6" />
        <h3 className="text-xl font-bold text-white mb-2">{t("common.coming_soon")}</h3>
        <p className="text-sm text-[var(--color-outline)] max-w-sm">{t("common.coming_soon_desc")}</p>
      </div>
    </>
  );
}
