import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router";
import { EmptyState, Button } from "@/shared/ui";
import { FileQuestion } from "lucide-react";

export function NotFoundPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <EmptyState
        icon={<FileQuestion className="w-16 h-16" />}
        title={t("common.not_found")}
        description={t("common.not_found_desc")}
        action={
          <Button variant="secondary" onClick={() => navigate("/")}>
            {t("common.back")}
          </Button>
        }
      />
    </div>
  );
}
