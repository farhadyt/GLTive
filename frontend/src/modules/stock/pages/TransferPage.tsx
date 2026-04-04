import { useState } from "react";
import { useTranslation } from "react-i18next";
import { ArrowRightLeft, ChevronRight, Loader2 } from "lucide-react";
import { useLookupItems, useLookupWarehouses, useTransferQuantity } from "../hooks/useStockQueries";
import toast from "react-hot-toast";

export function TransferPage() {
  const { t } = useTranslation();
  const { data: items, isLoading: itemsLoading } = useLookupItems();
  const { data: warehouses, isLoading: whLoading } = useLookupWarehouses();
  const mutation = useTransferQuantity();
  const [sourceItemId, setSourceItemId] = useState("");
  const [targetWarehouseId, setTargetWarehouseId] = useState("");
  const [quantity, setQuantity] = useState("");
  const [note, setNote] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      await mutation.mutateAsync({
        source_stock_item_id: sourceItemId,
        target_warehouse_id: targetWarehouseId,
        quantity,
        note: note || undefined,
      });
      toast.success(t("nav.transfer") + " ✓");
      setSourceItemId(""); setTargetWarehouseId(""); setQuantity(""); setNote("");
    } catch (err: unknown) {
      const error = err as { message?: string };
      toast.error(error.message || "Error");
    }
  }

  return (
    <>
      <div className="mb-8">
        <nav className="flex items-center gap-2 text-[var(--color-outline)] text-xs font-medium uppercase tracking-wider mb-2">
          <span>{t("nav.stock")}</span>
          <ChevronRight className="w-3 h-3" />
          <span className="text-[var(--color-primary)]">{t("nav.transfer")}</span>
        </nav>
        <h1 className="text-3xl font-bold text-white tracking-tight">{t("nav.transfer")}</h1>
      </div>

      <div className="max-w-lg">
        <form onSubmit={handleSubmit} className="bg-[var(--surface-container-low)] rounded-2xl p-8 space-y-5 border border-white/5">
          <div className="flex flex-col gap-2">
            <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("common.from")} — {t("nav.items")}</label>
            <select value={sourceItemId} onChange={(e) => setSourceItemId(e.target.value)} required
              className="w-full px-4 py-3 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5 focus:outline-none focus:border-[var(--color-primary-container)]">
              <option value="">{t("common.search")}...</option>
              {!itemsLoading && items?.map((item) => (
                <option key={item.id} value={item.id}>{item.display_name || item.internal_code || item.id.slice(0, 8)}</option>
              ))}
            </select>
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("common.to")} — {t("nav.warehouses")}</label>
            <select value={targetWarehouseId} onChange={(e) => setTargetWarehouseId(e.target.value)} required
              className="w-full px-4 py-3 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5 focus:outline-none focus:border-[var(--color-primary-container)]">
              <option value="">{t("common.search")}...</option>
              {!whLoading && warehouses?.map((wh) => (
                <option key={wh.id} value={wh.id}>{wh.name} ({wh.code})</option>
              ))}
            </select>
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("common.qty")}</label>
            <input type="number" step="0.01" min="0.01" value={quantity} onChange={(e) => setQuantity(e.target.value)} required
              className="w-full px-4 py-3 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5 focus:outline-none focus:border-[var(--color-primary-container)]" />
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">Note</label>
            <textarea value={note} onChange={(e) => setNote(e.target.value)} rows={2}
              className="w-full px-4 py-3 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5 focus:outline-none focus:border-[var(--color-primary-container)] resize-y" />
          </div>
          <button type="submit" disabled={mutation.isPending}
            className="w-full py-3.5 btn-primary-gradient font-bold rounded-xl flex items-center justify-center gap-2 text-sm disabled:opacity-50">
            {mutation.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <ArrowRightLeft className="w-4 h-4" />}
            {t("nav.transfer")}
          </button>
        </form>
      </div>
    </>
  );
}
