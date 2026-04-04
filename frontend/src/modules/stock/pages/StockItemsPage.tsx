import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Package, ChevronRight } from "lucide-react";
import { useStockItems } from "../hooks/useStockQueries";
import { Skeleton } from "@/shared/ui";

export function StockItemsPage() {
  const { t } = useTranslation();
  const [page, setPage] = useState(1);
  const { data, isLoading } = useStockItems(page);

  return (
    <>
      <div className="mb-8">
        <nav className="flex items-center gap-2 text-[var(--color-outline)] text-xs font-medium uppercase tracking-wider mb-2">
          <span>{t("nav.stock")}</span>
          <ChevronRight className="w-3 h-3" />
          <span className="text-[var(--color-primary)]">{t("nav.items")}</span>
        </nav>
        <h1 className="text-3xl font-bold text-white tracking-tight">
          {t("nav.items")}
        </h1>
      </div>

      <div className="bg-[var(--surface-container-low)] rounded-2xl overflow-hidden">
        {isLoading ? (
          <div className="p-6 space-y-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <Skeleton key={i} variant="rect" height="44px" />
            ))}
          </div>
        ) : data && data.items.length > 0 ? (
          <>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead className="text-[10px] text-[var(--color-outline)] uppercase font-black tracking-widest">
                  <tr>
                    <th className="px-6 py-4">{t("common.status")}</th>
                    <th className="px-6 py-4">Code</th>
                    <th className="px-6 py-4">Tracking</th>
                    <th className="px-6 py-4 text-right">{t("common.on_hand")}</th>
                    <th className="px-6 py-4 text-right">{t("common.reserved")}</th>
                    <th className="px-6 py-4 text-right">{t("dashboard.available")}</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  {data.items.map((item, i) => {
                    const available = parseFloat(item.quantity_available);
                    const minLevel = item.minimum_stock_level_override
                      ? parseFloat(item.minimum_stock_level_override)
                      : null;
                    const isLow = minLevel !== null && available <= minLevel;

                    return (
                      <tr
                        key={item.id}
                        className={`hover:bg-white/5 transition-colors ${i % 2 ? "bg-white/[0.02]" : ""}`}
                      >
                        <td className="px-6 py-4">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-black uppercase ${
                            item.is_active
                              ? "bg-[var(--color-on-secondary-container)] text-[var(--color-secondary)]"
                              : "bg-[var(--color-error-container)] text-[var(--color-error)]"
                          }`}>
                            {item.is_active ? t("common.active") : "Inactive"}
                          </span>
                        </td>
                        <td className="px-6 py-4 font-mono text-[var(--color-primary)]">
                          {item.internal_code || item.id.slice(0, 8)}
                        </td>
                        <td className="px-6 py-4">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-black uppercase ${
                            item.tracking_type === "serialized"
                              ? "bg-[var(--color-primary)]/10 text-[var(--color-primary)]"
                              : "bg-[var(--surface-container-highest)] text-[var(--color-outline)]"
                          }`}>
                            {item.tracking_type === "serialized" ? "Serial" : "Qty"}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-right font-bold text-white">
                          {parseFloat(item.quantity_on_hand).toLocaleString()}
                        </td>
                        <td className="px-6 py-4 text-right text-[var(--color-outline)]">
                          {parseFloat(item.quantity_reserved).toLocaleString()}
                        </td>
                        <td className="px-6 py-4 text-right">
                          <span className={`font-black ${isLow ? "text-[var(--color-error)]" : "text-white"}`}>
                            {available.toLocaleString()}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            {data.pagination.total_pages > 1 && (
              <div className="flex items-center justify-between px-6 py-4 border-t border-white/5">
                <span className="text-xs text-[var(--color-outline)]">
                  {data.pagination.total_items} {t("common.units")}
                </span>
                <div className="flex gap-2">
                  <button
                    disabled={page <= 1}
                    onClick={() => setPage((p) => p - 1)}
                    className="px-3 py-1.5 text-xs rounded-lg bg-[var(--surface-container-highest)] text-white disabled:opacity-30"
                  >
                    ←
                  </button>
                  <span className="px-3 py-1.5 text-xs text-[var(--color-outline)]">
                    {page} / {data.pagination.total_pages}
                  </span>
                  <button
                    disabled={page >= data.pagination.total_pages}
                    onClick={() => setPage((p) => p + 1)}
                    className="px-3 py-1.5 text-xs rounded-lg bg-[var(--surface-container-highest)] text-white disabled:opacity-30"
                  >
                    →
                  </button>
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="p-16 flex flex-col items-center justify-center text-center">
            <Package className="w-16 h-16 text-[var(--color-outline)]/30 mb-6" />
            <h3 className="text-xl font-bold text-white mb-2">{t("common.no_data")}</h3>
          </div>
        )}
      </div>
    </>
  );
}
