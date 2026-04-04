import { useState } from "react";
import { useTranslation } from "react-i18next";
import { ClipboardCheck, ChevronRight, Loader2, Plus, Check, X } from "lucide-react";
import {
  useLookupWarehouses,
  useLookupItems,
  useCreateAdjustmentSession,
  useUpsertAdjustmentLines,
  useConfirmAdjustment,
  useCancelAdjustment,
} from "../hooks/useStockQueries";
import type { AdjustmentLineInput } from "../types";
import toast from "react-hot-toast";

export function AdjustmentsPage() {
  const { t } = useTranslation();
  const { data: warehouses } = useLookupWarehouses();
  const { data: items } = useLookupItems();
  const createSession = useCreateAdjustmentSession();
  const upsertLines = useUpsertAdjustmentLines();
  const confirmAdj = useConfirmAdjustment();
  const cancelAdj = useCancelAdjustment();

  const [step, setStep] = useState<"create" | "lines" | "done">("create");
  const [warehouseId, setWarehouseId] = useState("");
  const [reason, setReason] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [sessionCode, setSessionCode] = useState("");
  const [lines, setLines] = useState<AdjustmentLineInput[]>([{ stock_item_id: "", counted_quantity: "", note: "" }]);

  async function handleCreateSession(e: React.FormEvent) {
    e.preventDefault();
    try {
      const session = await createSession.mutateAsync({ warehouse_id: warehouseId, reason });
      setSessionId(session.id);
      setSessionCode(session.session_code);
      setStep("lines");
      toast.success(t("common.create") + " ✓ — " + session.session_code);
    } catch (err: unknown) {
      toast.error((err as { message?: string }).message || "Error");
    }
  }

  function addLine() {
    setLines([...lines, { stock_item_id: "", counted_quantity: "", note: "" }]);
  }

  function updateLine(idx: number, field: keyof AdjustmentLineInput, value: string) {
    const updated = [...lines];
    updated[idx] = { ...updated[idx], [field]: value };
    setLines(updated);
  }

  async function handleSaveLines() {
    const validLines = lines.filter((l) => l.stock_item_id && l.counted_quantity);
    if (validLines.length === 0) return;
    try {
      await upsertLines.mutateAsync({ sessionId, lines: validLines });
      toast.success(t("common.save") + " ✓");
    } catch (err: unknown) {
      toast.error((err as { message?: string }).message || "Error");
    }
  }

  async function handleConfirm() {
    try {
      await handleSaveLines();
      await confirmAdj.mutateAsync(sessionId);
      toast.success(t("common.confirm") + " ✓");
      setStep("done");
    } catch (err: unknown) {
      toast.error((err as { message?: string }).message || "Error");
    }
  }

  async function handleCancel() {
    try {
      await cancelAdj.mutateAsync(sessionId);
      toast.success(t("common.cancel") + " ✓");
      setStep("done");
    } catch (err: unknown) {
      toast.error((err as { message?: string }).message || "Error");
    }
  }

  function handleReset() {
    setStep("create");
    setWarehouseId("");
    setReason("");
    setSessionId("");
    setSessionCode("");
    setLines([{ stock_item_id: "", counted_quantity: "", note: "" }]);
  }

  return (
    <>
      <div className="mb-8">
        <nav className="flex items-center gap-2 text-[var(--color-outline)] text-xs font-medium uppercase tracking-wider mb-2">
          <span>{t("nav.stock")}</span>
          <ChevronRight className="w-3 h-3" />
          <span className="text-[var(--color-primary)]">{t("nav.adjustments")}</span>
        </nav>
        <h1 className="text-3xl font-bold text-white tracking-tight">{t("nav.adjustments")}</h1>
      </div>

      {step === "create" && (
        <div className="max-w-lg">
          <form onSubmit={handleCreateSession} className="bg-[var(--surface-container-low)] rounded-2xl p-8 space-y-5 border border-white/5">
            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("nav.warehouses")}</label>
              <select value={warehouseId} onChange={(e) => setWarehouseId(e.target.value)} required
                className="w-full px-4 py-3 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5 focus:outline-none focus:border-[var(--color-primary-container)]">
                <option value="">{t("common.search")}...</option>
                {warehouses?.map((wh) => (
                  <option key={wh.id} value={wh.id}>{wh.name} ({wh.code})</option>
                ))}
              </select>
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("common.description")}</label>
              <textarea value={reason} onChange={(e) => setReason(e.target.value)} rows={2}
                className="w-full px-4 py-3 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5 focus:outline-none focus:border-[var(--color-primary-container)] resize-y" />
            </div>
            <button type="submit" disabled={createSession.isPending}
              className="w-full py-3.5 btn-primary-gradient font-bold rounded-xl flex items-center justify-center gap-2 text-sm disabled:opacity-50">
              {createSession.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <ClipboardCheck className="w-4 h-4" />}
              {t("common.create")}
            </button>
          </form>
        </div>
      )}

      {step === "lines" && (
        <div className="max-w-3xl">
          <div className="bg-[var(--surface-container-low)] rounded-2xl p-8 border border-white/5">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-bold text-white">{sessionCode}</h2>
                <p className="text-xs text-[var(--color-outline)] uppercase tracking-wider">Draft</p>
              </div>
              <button onClick={addLine} className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-[var(--color-primary)] bg-[var(--color-primary)]/10 rounded-lg hover:bg-[var(--color-primary)]/20 transition-colors">
                <Plus className="w-3.5 h-3.5" /> Add Line
              </button>
            </div>

            <div className="space-y-3 mb-6">
              {lines.map((line, idx) => (
                <div key={idx} className="flex gap-3 items-end">
                  <div className="flex-1">
                    {idx === 0 && <label className="text-[10px] font-semibold text-[var(--color-outline)] uppercase tracking-wider mb-1 block">{t("nav.items")}</label>}
                    <select value={line.stock_item_id} onChange={(e) => updateLine(idx, "stock_item_id", e.target.value)}
                      className="w-full px-3 py-2.5 text-sm rounded-lg bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5">
                      <option value="">—</option>
                      {items?.map((item) => (
                        <option key={item.id} value={item.id}>{item.display_name || item.id.slice(0, 8)}</option>
                      ))}
                    </select>
                  </div>
                  <div className="w-32">
                    {idx === 0 && <label className="text-[10px] font-semibold text-[var(--color-outline)] uppercase tracking-wider mb-1 block">{t("common.qty")}</label>}
                    <input type="number" step="0.01" min="0" value={line.counted_quantity} onChange={(e) => updateLine(idx, "counted_quantity", e.target.value)}
                      className="w-full px-3 py-2.5 text-sm rounded-lg bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5" />
                  </div>
                  <div className="w-40">
                    {idx === 0 && <label className="text-[10px] font-semibold text-[var(--color-outline)] uppercase tracking-wider mb-1 block">Note</label>}
                    <input value={line.note || ""} onChange={(e) => updateLine(idx, "note", e.target.value)}
                      className="w-full px-3 py-2.5 text-sm rounded-lg bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5" />
                  </div>
                </div>
              ))}
            </div>

            <div className="flex gap-3">
              <button onClick={handleConfirm} disabled={confirmAdj.isPending || upsertLines.isPending}
                className="flex-1 py-3 btn-primary-gradient font-bold rounded-xl flex items-center justify-center gap-2 text-sm disabled:opacity-50">
                {confirmAdj.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Check className="w-4 h-4" />}
                {t("common.confirm")}
              </button>
              <button onClick={handleCancel} disabled={cancelAdj.isPending}
                className="px-6 py-3 bg-[var(--surface-container-highest)] text-[var(--color-error)] font-bold rounded-xl flex items-center justify-center gap-2 text-sm disabled:opacity-50 hover:bg-[var(--surface-bright)] transition-colors">
                {cancelAdj.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <X className="w-4 h-4" />}
                {t("common.cancel")}
              </button>
            </div>
          </div>
        </div>
      )}

      {step === "done" && (
        <div className="max-w-lg bg-[var(--surface-container-low)] rounded-2xl p-16 flex flex-col items-center justify-center text-center border border-white/5">
          <ClipboardCheck className="w-16 h-16 text-[var(--color-secondary)] mb-6" />
          <h3 className="text-xl font-bold text-white mb-2">{sessionCode}</h3>
          <p className="text-sm text-[var(--color-outline)] mb-6">{t("nav.adjustments")} — {t("common.confirm")}</p>
          <button onClick={handleReset}
            className="px-5 py-2.5 text-sm font-medium text-white bg-[var(--surface-container-highest)] rounded-xl hover:bg-[var(--surface-bright)] transition-colors">
            {t("common.create")} {t("nav.adjustments")}
          </button>
        </div>
      )}
    </>
  );
}
