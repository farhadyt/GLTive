import { useTranslation } from "react-i18next";
import {
  Package,
  Warehouse as WarehouseIcon,
  AlertTriangle,
  ArrowRightLeft,
  QrCode,
  ChevronRight,
  History,
} from "lucide-react";
import {
  useDashboardSummary,
  useRecentMovements,
  useLowStockItems,
} from "../hooks/useStockQueries";
import { Skeleton } from "@/shared/ui";

export function StockDashboardPage() {
  const { t } = useTranslation();
  const { data: summary, isLoading: summaryLoading } = useDashboardSummary();
  const { data: movements, isLoading: movementsLoading } = useRecentMovements();
  const { data: lowStock, isLoading: lowStockLoading } = useLowStockItems();

  return (
    <>
      {/* Header */}
      <div className="mb-8">
        <nav className="flex items-center gap-2 text-[var(--color-outline)] text-xs font-medium uppercase tracking-wider mb-2">
          <span>{t("nav.stock")}</span>
          <ChevronRight className="w-3 h-3" />
          <span className="text-[var(--color-primary)]">{t("nav.dashboard")}</span>
        </nav>
        <h1 className="text-3xl font-bold text-white tracking-tight">
          {t("nav.dashboard")}
        </h1>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
        <KpiCard
          label={t("dashboard.total_active_stock")}
          value={summaryLoading ? null : summary?.total_active_stock_items}
          icon={<Package className="w-5 h-5 text-[var(--color-primary)]/50" />}
          accent="primary"
        />
        <KpiCard
          label={t("dashboard.total_warehouses")}
          value={summaryLoading ? null : summary?.total_warehouses}
          icon={<WarehouseIcon className="w-5 h-5 text-[var(--color-outline)]" />}
        />
        <KpiCard
          label={t("dashboard.low_stock_alerts")}
          value={summaryLoading ? null : summary?.low_stock_count}
          icon={<AlertTriangle className="w-5 h-5 text-[var(--color-error)]/50" />}
          accent="error"
          badge={summary?.low_stock_count ? t("common.danger").toUpperCase() : undefined}
        />
        <KpiCard
          label={t("dashboard.movements_title")}
          value={summaryLoading ? null : summary?.recent_movements_count}
          icon={<ArrowRightLeft className="w-5 h-5 text-[var(--color-outline)]" />}
        />
        <KpiCard
          label={t("dashboard.serialized_items")}
          value={summaryLoading ? null : summary?.serialized_count}
          icon={<QrCode className="w-5 h-5 text-[var(--color-outline)]" />}
        />
      </div>

      {/* Middle: Movements + Low Stock */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Recent Movements */}
        <div className="lg:col-span-5 bg-[var(--surface-container-low)] rounded-2xl overflow-hidden flex flex-col max-h-[520px]">
          <div className="p-6 border-b border-white/5 flex justify-between items-center">
            <h3 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
              <History className="w-4 h-4 text-[var(--color-secondary)]" />
              {t("dashboard.recent_movements")}
            </h3>
          </div>
          <div className="flex-1 overflow-y-auto no-scrollbar p-4 space-y-2">
            {movementsLoading ? (
              Array.from({ length: 4 }).map((_, i) => (
                <Skeleton key={i} variant="rect" height="56px" />
              ))
            ) : movements && movements.length > 0 ? (
              movements.map((mv) => (
                <div
                  key={mv.id}
                  className="flex items-center justify-between p-3 bg-[var(--surface)] rounded-xl hover:bg-[var(--surface-container)] transition-colors"
                >
                  <div>
                    <p className="text-sm font-bold text-white">{mv.stock_item_name}</p>
                    <p className="text-[10px] text-[var(--color-outline)] uppercase tracking-tight">
                      {mv.movement_type.replace(/_/g, " ")}
                      {mv.source_warehouse_name && ` • ${mv.source_warehouse_name}`}
                      {mv.target_warehouse_name && ` → ${mv.target_warehouse_name}`}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className={`text-sm font-black ${
                      mv.movement_type.includes("in") || mv.movement_type.includes("plus")
                        ? "text-[var(--color-secondary)]"
                        : mv.movement_type.includes("out") || mv.movement_type.includes("minus")
                        ? "text-[var(--color-error)]"
                        : "text-white"
                    }`}>
                      {mv.movement_type.includes("in") || mv.movement_type.includes("plus") ? "+" : ""}
                      {mv.quantity}
                    </p>
                    <p className="text-[10px] text-[var(--color-outline)] italic">
                      {new Date(mv.performed_at).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-sm text-[var(--color-outline)] text-center py-8">
                {t("common.no_data")}
              </p>
            )}
          </div>
        </div>

        {/* Low Stock Alerts */}
        <div className="lg:col-span-7 bg-[var(--surface-container-low)] rounded-2xl overflow-hidden flex flex-col max-h-[520px]">
          <div className="p-6 border-b border-white/5 flex justify-between items-center">
            <h3 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-[var(--color-error)]" />
              {t("dashboard.critical_low_stock")}
            </h3>
          </div>
          <div className="flex-1 overflow-x-auto no-scrollbar">
            {lowStockLoading ? (
              <div className="p-4 space-y-3">
                {Array.from({ length: 4 }).map((_, i) => (
                  <Skeleton key={i} variant="rect" height="44px" />
                ))}
              </div>
            ) : lowStock && lowStock.length > 0 ? (
              <table className="w-full text-left border-collapse">
                <thead className="bg-[var(--surface-container-lowest)]/50 text-[10px] text-[var(--color-outline)] uppercase font-black tracking-widest">
                  <tr>
                    <th className="px-6 py-4">{t("dashboard.item_name")}</th>
                    <th className="px-6 py-4">{t("dashboard.warehouse")}</th>
                    <th className="px-6 py-4 text-center">{t("dashboard.available")}</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  {lowStock.map((item) => (
                    <tr key={item.id} className="hover:bg-white/5 transition-colors">
                      <td className="px-6 py-4 font-bold text-white">{item.item_name}</td>
                      <td className="px-6 py-4 text-slate-400">{item.warehouse_name}</td>
                      <td className="px-6 py-4 text-center">
                        <span className="text-[var(--color-error)] font-black">
                          {item.quantity_available}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="text-sm text-[var(--color-outline)] text-center py-8">
                {t("common.no_data")}
              </p>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

function KpiCard({
  label,
  value,
  icon,
  accent,
  badge,
}: {
  label: string;
  value: number | null | undefined;
  icon: React.ReactNode;
  accent?: "primary" | "error";
  badge?: string;
}) {
  return (
    <div
      className={`bg-[var(--surface-container-low)] p-6 rounded-xl relative overflow-hidden ${
        accent === "primary"
          ? "border-l-4 border-[var(--color-primary)]"
          : accent === "error"
          ? "border-l-4 border-[var(--color-error)]"
          : ""
      }`}
    >
      <div className="flex justify-between items-start mb-4">
        <p className="text-[var(--color-outline)] text-xs font-bold uppercase tracking-widest">
          {label}
        </p>
        {icon}
      </div>
      <div className="flex items-end gap-3">
        {value === null || value === undefined ? (
          <Skeleton variant="rect" width="80px" height="36px" />
        ) : (
          <span className="text-4xl font-bold text-white tracking-tight">
            {value.toLocaleString()}
          </span>
        )}
        {badge && (
          <span className="px-2 py-0.5 bg-[var(--color-error)]/10 text-[var(--color-error)] rounded-full text-[10px] font-black mb-1 uppercase">
            {badge}
          </span>
        )}
      </div>
    </div>
  );
}
