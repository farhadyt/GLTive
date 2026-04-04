import { useTranslation } from "react-i18next";
import { PageHeader, EmptyState } from "@/shared/ui";
import { Package } from "lucide-react";

export function StockItemsPage() {
  const { t } = useTranslation();

  return (
    <>
      <PageHeader
        title={t("nav.items")}
        breadcrumbs={[
          { label: t("nav.stock"), path: "/stock" },
          { label: t("nav.items") },
        ]}
      />
      <EmptyState
        icon={<Package className="w-12 h-12" />}
        title={t("common.coming_soon")}
        description={t("common.coming_soon_desc")}
      />
    </>
  );
}
