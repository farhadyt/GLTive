import { useTranslation } from "react-i18next";
import { PageHeader, EmptyState } from "@/shared/ui";
import { LayoutDashboard } from "lucide-react";

export function StockDashboardPage() {
  const { t } = useTranslation();

  return (
    <>
      <PageHeader
        title={t("nav.dashboard")}
        breadcrumbs={[
          { label: t("nav.stock"), path: "/stock" },
          { label: t("nav.dashboard") },
        ]}
      />
      <EmptyState
        icon={<LayoutDashboard className="w-12 h-12" />}
        title={t("common.coming_soon")}
        description={t("common.coming_soon_desc")}
      />
    </>
  );
}
