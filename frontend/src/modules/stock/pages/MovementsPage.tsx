import { useState } from "react";
import { useTranslation } from "react-i18next";
import { History, ChevronRight } from "lucide-react";
import { useMovements } from "../hooks/useStockQueries";
import { Skeleton } from "@/shared/ui";

const MOVEMENT_TYPES = [
  { value: "", label: "All" },
  { value: "stock_in", label: "Stock In" },
  { value: "stock_out", label: "Stock Out" },
  { value: "transfer_in", label: "Transfer In" },
  { value: "transfer_out", label: "Transfer Out" },
  { value: "adjustment_plus", label: "Adjust +" },
  { value: "adjustment_minus", label: "Adjust −" },
];

export function MovementsPage() {
  const { t } = useTranslation();
  const [page, setPage] = useState(1);
  const [typeFilter, setTypeFilter] = useState("");
  const params = {
    page,
    page_size: 20,
    ...(typeFilter ? { movement_type: typeFilter } : {}),
  };
  const { data, isLoading } = useMovements(params);

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

      {/* Filter */}
      <div className="mb-6 flex items-center gap-3">
        <span className="text-xs text-[var(--color-outline)] font-bold uppercase tracking-wider">
          {t("common.filter")}:
        </span>
        <div className="flex gap-1.5">
          {MOVEMENT_TYPES.map((mt) => (
            <button
              key={mt.value}
              onClick={() => { setTypeFilter(mt.value); setPage(1); }}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
                typeFilter === mt.value
                  ? "bg-[var(--color-primary)]/20 text-[var(--color-primary)]"
                  : "bg-[var(--surface-container-highest)] text-[var(--color-outline)] hover:text-white"
              }`}
            >
              {mt.label}
            </button>
          ))}
        </div>
      </div>

      {/* Table */}
      <div className="bg-[var(--surface-container-low)] rounded-2xl overflow-hidden">
        {isLoading ? (
          <div className="p-6 space-y-3">
            {Array.from({ length: 8 }).map((_, i) => (
              <Skeleton key={i} variant="rect" height="44px" />
            ))}
          </div>
        ) : data && data.items.length > 0 ? (
          <>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead className="text-[10px] text-[var(--color-outline)] uppercase font-black tracking-widest">
                  <tr>
                    <th className="px-6 py-4">Type</th>
                    <th className="px-6 py-4">{t("dashboard.item_name")}</th>
                    <th className="px-6 py-4 text-right">Qty</th>
                    <th className="px-6 py-4">From</th>
                    <th className="px-6 py-4">To</th>
                    <th className="px-6 py-4">By</th>
                    <th className="px-6 py-4 text-right">Date</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  {data.items.map((mv, i) => (
                    <tr
                      key={mv.id}
                      className={`hover:bg-white/5 transition-colors ${i % 2 ? "bg-white/[0.02]" : ""}`}
                    >
                      <td className="px-6 py-4">
                        <MovementBadge type={mv.movement_type} />
                      </td>
                      <td className="px-6 py-4 font-bold text-white">{mv.stock_item_name}</td>
                      <td className="px-6 py-4 text-right font-black text-white">
                        {mv.quantity}
                      </td>
                      <td className="px-6 py-4 text-[var(--color-outline)]">
                        {mv.source_warehouse_name || "—"}
                      </td>
                      <td className="px-6 py-4 text-[var(--color-outline)]">
                        {mv.target_warehouse_name || "—"}
                      </td>
                      <td className="px-6 py-4 text-[var(--color-outline)]">
                        {mv.performed_by_username || "—"}
                      </td>
                      <td className="px-6 py-4 text-right text-[var(--color-outline)] text-xs">
                        {new Date(mv.performed_at).toLocaleString()}
                      </td>
                    </tr>
                  ))}
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
            <History className="w-16 h-16 text-[var(--color-outline)]/30 mb-6" />
            <h3 className="text-xl font-bold text-white mb-2">{t("common.no_data")}</h3>
          </div>
        )}
      </div>
    </>
  );
}

function MovementBadge({ type }: { type: string }) {
  const colors: Record<string, string> = {
    stock_in: "bg-[var(--color-on-secondary-container)] text-[var(--color-secondary)]",
    stock_out: "bg-[var(--color-error-container)] text-[var(--color-error)]",
    transfer_in: "bg-[var(--color-primary)]/10 text-[var(--color-primary)]",
    transfer_out: "bg-[var(--color-primary)]/10 text-[var(--color-primary)]",
    adjustment_plus: "bg-[var(--color-on-secondary-container)] text-[var(--color-secondary)]",
    adjustment_minus: "bg-[var(--color-error-container)] text-[var(--color-error)]",
  };
  return (
    <span className={`px-2 py-0.5 rounded-full text-[10px] font-black uppercase ${colors[type] || "bg-[var(--surface-container-highest)] text-[var(--color-outline)]"}`}>
      {type.replace(/_/g, " ")}
    </span>
  );
}
