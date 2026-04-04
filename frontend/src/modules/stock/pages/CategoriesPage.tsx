import { useTranslation } from "react-i18next";
import { PageHeader, EmptyState } from "@/shared/ui";
import { Tags } from "lucide-react";

export function CategoriesPage() {
  const { t } = useTranslation();

  return (
    <>
      <PageHeader
        title={t("nav.categories")}
        breadcrumbs={[
          { label: t("nav.stock"), path: "/stock" },
          { label: t("nav.categories") },
        ]}
      />
      <EmptyState
        icon={<Tags className="w-12 h-12" />}
        title={t("common.coming_soon")}
        description={t("common.coming_soon_desc")}
      />
    </>
  );
}
