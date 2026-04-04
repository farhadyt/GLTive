import { useTranslation } from "react-i18next";
import { PageHeader, EmptyState } from "@/shared/ui";
import { History } from "lucide-react";

export function MovementsPage() {
  const { t } = useTranslation();

  return (
    <>
      <PageHeader
        title={t("nav.movements")}
        breadcrumbs={[
          { label: t("nav.stock"), path: "/stock" },
          { label: t("nav.movements") },
        ]}
      />
      <EmptyState
        icon={<History className="w-12 h-12" />}
        title={t("common.coming_soon")}
        description={t("common.coming_soon_desc")}
      />
    </>
  );
}
