import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router";
import { EmptyState, Button } from "@/shared/ui";
import { ShieldX } from "lucide-react";

export function AccessDeniedPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <EmptyState
        icon={<ShieldX className="w-16 h-16" />}
        title={t("common.access_denied")}
        description={t("common.access_denied_desc")}
        action={
          <Button variant="secondary" onClick={() => navigate("/")}>
            {t("common.back")}
          </Button>
        }
      />
    </div>
  );
}
