import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Box, ChevronRight, Plus, Pencil } from "lucide-react";
import { useItemModels, useCreateItemModel, useUpdateItemModel } from "../hooks/useStockQueries";
import { Skeleton } from "@/shared/ui";
import type { ItemModel } from "../types";
import toast from "react-hot-toast";

export function ItemModelsPage() {
  const { t } = useTranslation();
  const [page, setPage] = useState(1);
  const { data, isLoading } = useItemModels(page);
  const [modalOpen, setModalOpen] = useState(false);
  const [editItem, setEditItem] = useState<ItemModel | null>(null);

  return (
    <>
      <div className="mb-8 flex justify-between items-end">
        <div>
          <nav className="flex items-center gap-2 text-[var(--color-outline)] text-xs font-medium uppercase tracking-wider mb-2">
            <span>{t("nav.stock")}</span><ChevronRight className="w-3 h-3" />
            <span className="text-[var(--color-primary)]">{t("nav.item_models")}</span>
          </nav>
          <h1 className="text-3xl font-bold text-white tracking-tight">{t("nav.item_models")}</h1>
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
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead className="text-[10px] text-[var(--color-outline)] uppercase font-black tracking-widest">
                  <tr>
                    <th className="px-6 py-4">{t("common.status")}</th>
                    <th className="px-6 py-4">{t("dashboard.item_name")}</th>
                    <th className="px-6 py-4">{t("common.code")}</th>
                    <th className="px-6 py-4">{t("common.tracking")}</th>
                    <th className="px-6 py-4">{t("common.description")}</th>
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
                      <td className="px-6 py-4 font-bold text-white">{item.model_name}</td>
                      <td className="px-6 py-4 font-mono text-[var(--color-primary)]">{item.model_code || "—"}</td>
                      <td className="px-6 py-4">
                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-black uppercase ${item.tracking_type === "serialized" ? "bg-[var(--color-primary)]/10 text-[var(--color-primary)]" : "bg-[var(--surface-container-highest)] text-[var(--color-outline)]"}`}>
                          {item.tracking_type === "serialized" ? t("common.serial") : t("common.qty")}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-[var(--color-outline)] truncate max-w-[200px]">{item.description || "—"}</td>
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
            </div>
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
            <Box className="w-16 h-16 text-[var(--color-outline)]/30 mb-6" />
            <h3 className="text-xl font-bold text-white mb-2">{t("common.no_data")}</h3>
          </div>
        )}
      </div>

      {modalOpen && <ItemModelModal itemModel={editItem} onClose={() => setModalOpen(false)} />}
    </>
  );
}

function ItemModelModal({ itemModel, onClose }: { itemModel: ItemModel | null; onClose: () => void }) {
  const { t } = useTranslation();
  const isEdit = !!itemModel;
  const createMut = useCreateItemModel();
  const updateMut = useUpdateItemModel();
  const [modelName, setModelName] = useState(itemModel?.model_name || "");
  const [modelCode, setModelCode] = useState(itemModel?.model_code || "");
  const [categoryId, setCategoryId] = useState(itemModel?.category_id || "");
  const [trackingType, setTrackingType] = useState(itemModel?.tracking_type || "quantity_based");
  const [description, setDescription] = useState(itemModel?.description || "");
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  // We need categories for the dropdown — use lookup
  const [categories, setCategories] = useState<Array<{ id: string; code?: string; name?: string }>>([]);
  useState(() => {
    import("../api/stock-api").then(mod => {
      mod.fetchCategories(1, 100).then(data => {
        setCategories(data.items.map(c => ({ id: c.id, code: c.code, name: c.name })));
      }).catch(() => {});
    });
  });

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setFieldErrors({});
    try {
      if (isEdit) {
        await updateMut.mutateAsync({ id: itemModel!.id, data: { model_name: modelName, model_code: modelCode || undefined, category_id: categoryId, description } });
      } else {
        await createMut.mutateAsync({ category_id: categoryId, model_name: modelName, tracking_type: trackingType, model_code: modelCode || undefined, description });
      }
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
  const inputCls = "w-full px-4 py-3 text-sm rounded-xl bg-[var(--surface-container-lowest)] text-[var(--color-on-surface)] border border-white/5 focus:outline-none focus:border-[var(--color-primary-container)]";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />
      <div className="relative z-10 w-full max-w-md bg-[var(--surface-container)] rounded-2xl border border-white/5 shadow-2xl">
        <div className="p-6 border-b border-white/5">
          <h2 className="text-lg font-bold text-white">{isEdit ? t("common.edit") : t("common.create")} — {t("nav.item_models")}</h2>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("nav.categories")} *</label>
            <select value={categoryId} onChange={(e) => setCategoryId(e.target.value)} required className={inputCls}>
              <option value="">—</option>
              {categories.map(c => <option key={c.id} value={c.id}>{c.name} ({c.code})</option>)}
            </select>
            {fieldErrors.category_id && <p className="text-xs text-[var(--color-error)]">{fieldErrors.category_id}</p>}
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("dashboard.item_name")} *</label>
            <input value={modelName} onChange={(e) => setModelName(e.target.value)} required className={inputCls} />
            {fieldErrors.model_name && <p className="text-xs text-[var(--color-error)]">{fieldErrors.model_name}</p>}
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("common.code")}</label>
              <input value={modelCode} onChange={(e) => setModelCode(e.target.value)} className={inputCls} />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("common.tracking")} *</label>
              <select value={trackingType} onChange={(e) => setTrackingType(e.target.value as "quantity_based" | "serialized")} disabled={isEdit} className={`${inputCls} disabled:opacity-50`}>
                <option value="quantity_based">{t("common.qty")}</option>
                <option value="serialized">{t("common.serial")}</option>
              </select>
            </div>
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-[var(--color-on-surface-variant)] uppercase tracking-wider">{t("common.description")}</label>
            <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={2} className={`${inputCls} resize-y`} />
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
