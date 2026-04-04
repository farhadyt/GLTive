import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Warehouse as WarehouseIcon, ChevronRight, Plus, Pencil } from "lucide-react";
import { useWarehouses, useCreateWarehouse, useUpdateWarehouse } from "../hooks/useStockQueries";
import { Skeleton } from "@/shared/ui";
import type { Warehouse } from "../types";
import toast from "react-hot-toast";

export function WarehousesPage() {
  const { t } = useTranslation();
  const [page, setPage] = useState(1);
  const { data, isLoading } = useWarehouses(page);
  const [modalOpen, setModalOpen] = useState(false);
  const [editItem, setEditItem] = useState<Warehouse | null>(null);

  return (
    <>
      <div className="mb-8 flex justify-between items-end">
        <div>
          <nav className="flex items-center gap-2 text-[var(--color-outline)] text-xs font-medium uppercase tracking-wider mb-2">
            <span>{t("nav.stock")}</span><ChevronRight className="w-3 h-3" />
            <span className="text-[var(--color-primary)]">{t("nav.warehouses")}</span>
          </nav>
          <h1 className="text-3xl font-bold text-white tracking-tight">{t("nav.warehouses")}</h1>
        </div>
        <button onClick={() => { setEditItem(null); setModalOpen(true); }}
          className="btn-primary-gradient font-semibold rounded-xl flex items-center gap-2 px-5 py-2.5 text-sm">
          <Plus className="w-4 h-4" /> {t("common.create")}
        </button>
      </div>

      <div className="bg-[var(--surface-container-low)] rounded-2xl overflow-hidden">
        {isLoading ? (
          <div className="p-6 space-y-3">{Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} variant="rect" height="44px" />)}</div>
        ) : data && data.items.length > 0 ? (
          <>
            <table className="w-full text-left border-collapse">
              <thead className="text-[10px] text-[var(--color-outline)] uppercase font-black tracking-widest">
                <tr>
                  <th className="px-6 py-4">{t("common.status")}</th>
                  <th className="px-6 py-4">{t("common.code")}</th>
                  <th className="px-6 py-4">{t("dashboard.item_name")}</th>
                  <th className="px-6 py-4">{t("common.description")}</th>
                  <th className="px-6 py-4">{t("common.type")}</th>
                  <th className="px-6 py-4 text-right">{t("common.actions")}</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                {data.items.map((item, i) => (
                  <tr key={item.id} className={`hover:bg-white/5 transition-colors ${i % 2 ? "bg-white/[0.02]" : ""}`}>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-black uppercase ${item.is_active ? "bg-[var(--color-on-secondary-container)] text-[var(--color-secondary)]" : "bg-[var(--color-error-container)] text-[var(--color-error)]"}`}>
                        {item.is_active ? t("common.active") : t("common.inactive")}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-mono text-[var(--color-primary)]">{item.code}</td>
                    <td className="px-6 py-4 font-bold text-white">{item.name}</td>
                    <td className="px-6 py-4 text-[var(--color-outline)] truncate max-w-[200px]">{item.description || "—"}</td>
                    <td className="px-6 py-4">
                      {item.is_default && <span className="px-2 py-0.5 rounded-full text-[10px] font-black uppercase bg-[var(--color-primary)]/10 text-[var(--color-primary)]">Default</span>}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button onClick={() => { setEditItem(item); setModalOpen(true); }}
                        className="text-[var(--color-primary)] hover:bg-[var(--color-primary)]/10 p-1.5 rounded-lg transition-colors">
                        <Pencil className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {data.pagination.total_pages > 1 && (
              <div className="flex items-center justify-between px-6 py-4 border-t border-white/5">
                <span className="text-xs text-[var(--color-outline)]">{data.pagination.total_items} {t("common.units")}</span>
                <div className="flex gap-2">
                  <button disabled={page <= 1} onClick={() => setPage(p => p - 1)} className="px-3 py-1.5 text-xs rounded-lg bg-[var(--surface-container-highest)] text-white disabled:opacity-30">←</button>
                  <span className="px-3 py-1.5 text-xs text-[var(--color-outline)]">{page} / {data.pagination.total_pages}</span>
                  <button disabled={page >= data.pagination.total_pages} onClick={() => setPage(p => p + 1)} className="px-3 py-1.5 text-xs rounded-lg bg-[var(--surface-container-highest)] text-white disabled:opacity-30">→</button>
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="p-16 flex flex-col items-center justify-center text-center">
            <WarehouseIcon className="w-16 h-16 text-[var(--color-outline)]/30 mb-6" />
            <h3 className="text-xl font-bold text-white mb-2">{t("common.no_data")}</h3>
          </div>
        )}
      </div>

      {modalOpen && <WarehouseModal warehouse={editItem} onClose={() => setModalOpen(false)} />}
    </>
  );
}

function WarehouseModal({ warehouse, onClose }: { warehouse: Warehouse | null; onClose: () => void }) {
  const { t } = useTranslation();
  const isEdit = !!warehouse;
  const createMut = useCreateWarehouse();
  const updateMut = useUpdateWarehouse();
  const [code, setCode] = useState(warehouse?.code || "");
  const [name, setName] = useState(warehouse?.name || "");
  const [description, setDescription] = useState(warehouse?.description || "");
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setFieldErrors({});
    try {
      if (isEdit) await updateMut.mutateAsync({ id: warehouse!.id, data: { code, name, description } });
      else await createMut.mutateAsync({ code, name, description });
      toast.success("✓");
      onClose();
    } catch (err: unknown) {
      const error = err as { fieldErrors?: Record<string, string[]>; message?: string };
      if (error.fieldErrors) {
        const mapped: Record<string, string> = {};
        for (const [k, v] of Object.entries(error.fieldErrors)) mapped[k] = Array.isArray(v) ? v[0] : String(v);
        setFieldErrors(mapped);
      } else toast.error(error.message || "Error");
    }
  }

  const isPending = createMut.isPending || updateMut.isPending;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />
      <div className="relative z-10 w-full max-w-md bg-[var(--surface-container)] rounded-2xl border border-white/5 shadow-2xl">
        <div className="p-6 border-b border-white/5">
          <h2 className="text-lg font-bold text-white">{isEdit ? t("common.edit") : t("common.create")} — {t("nav.warehouses")}</h2>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("common.code")} *</label>
            <input value={code} onChange={(e) => setCode(e.target.value)} required disabled={isEdit} className="w-full px-4 py-3 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5 focus:outline-none focus:border-[var(--color-primary-container)] disabled:opacity-50" />
            {fieldErrors.code && <p className="text-xs text-[var(--color-error)]">{fieldErrors.code}</p>}
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("dashboard.item_name")} *</label>
            <input value={name} onChange={(e) => setName(e.target.value)} required className="w-full px-4 py-3 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5 focus:outline-none focus:border-[var(--color-primary-container)]" />
            {fieldErrors.name && <p className="text-xs text-[var(--color-error)]">{fieldErrors.name}</p>}
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("common.description")}</label>
            <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={2} className="w-full px-4 py-3 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5 focus:outline-none focus:border-[var(--color-primary-container)] resize-y" />
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" onClick={onClose} className="px-5 py-2.5 text-sm font-medium text-[var(--color-on-surface-variant)] bg-[var(--surface-container-highest)] rounded-xl hover:bg-[var(--surface-bright)] transition-colors">{t("common.cancel")}</button>
            <button type="submit" disabled={isPending} className="px-5 py-2.5 text-sm font-bold btn-primary-gradient rounded-xl disabled:opacity-50">{isPending ? t("common.loading") : isEdit ? t("common.save") : t("common.create")}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
