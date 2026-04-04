import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  fetchDashboardSummary,
  fetchRecentMovements,
  fetchLowStockItems,
  fetchCategories,
  createCategory,
  updateCategory,
  fetchBrands,
  createBrand,
  updateBrand,
  fetchVendors,
  createVendor,
  updateVendor,
  fetchWarehouses,
  createWarehouse,
  updateWarehouse,
  fetchItemModels,
  createItemModel,
  updateItemModel,
  fetchStockItems,
  fetchMovements,
  fetchLookupItems,
  fetchLookupWarehouses,
  receiveQuantity,
  issueQuantity,
  transferQuantity,
  createAdjustmentSession,
  upsertAdjustmentLines,
  confirmAdjustmentSession,
  cancelAdjustmentSession,
} from "../api/stock-api";

// ─── Query Keys ───
export const stockKeys = {
  dashboard: ["stock", "dashboard"] as const,
  recentMovements: ["stock", "dashboard", "recent-movements"] as const,
  lowStock: ["stock", "dashboard", "low-stock"] as const,
  categories: (page: number) => ["stock", "categories", page] as const,
  items: (page: number) => ["stock", "items", page] as const,
  movements: (params: Record<string, unknown>) =>
    ["stock", "movements", params] as const,
};

// ─── Dashboard ───
export function useDashboardSummary() {
  return useQuery({
    queryKey: stockKeys.dashboard,
    queryFn: fetchDashboardSummary,
  });
}

export function useRecentMovements() {
  return useQuery({
    queryKey: stockKeys.recentMovements,
    queryFn: fetchRecentMovements,
  });
}

export function useLowStockItems() {
  return useQuery({
    queryKey: stockKeys.lowStock,
    queryFn: fetchLowStockItems,
  });
}

// ─── Categories ───
export function useCategories(page = 1) {
  return useQuery({
    queryKey: stockKeys.categories(page),
    queryFn: () => fetchCategories(page),
  });
}

export function useCreateCategory() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createCategory,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["stock", "categories"] });
    },
  });
}

export function useUpdateCategory() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<{ code: string; name: string; description: string }> }) =>
      updateCategory(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["stock", "categories"] });
    },
  });
}

// ─── Brands ───
export function useBrands(page = 1) {
  return useQuery({
    queryKey: ["stock", "brands", page] as const,
    queryFn: () => fetchBrands(page),
  });
}

export function useCreateBrand() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createBrand,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["stock", "brands"] }); },
  });
}

export function useUpdateBrand() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Parameters<typeof updateBrand>[1] }) => updateBrand(id, data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["stock", "brands"] }); },
  });
}

// ─── Vendors ───
export function useVendors(page = 1) {
  return useQuery({
    queryKey: ["stock", "vendors", page] as const,
    queryFn: () => fetchVendors(page),
  });
}

export function useCreateVendor() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createVendor,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["stock", "vendors"] }); },
  });
}

export function useUpdateVendor() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Parameters<typeof updateVendor>[1] }) => updateVendor(id, data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["stock", "vendors"] }); },
  });
}

// ─── Warehouses ───
export function useWarehouses(page = 1) {
  return useQuery({
    queryKey: ["stock", "warehouses", page] as const,
    queryFn: () => fetchWarehouses(page),
  });
}

export function useCreateWarehouse() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createWarehouse,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["stock", "warehouses"] }); },
  });
}

export function useUpdateWarehouse() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Parameters<typeof updateWarehouse>[1] }) => updateWarehouse(id, data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["stock", "warehouses"] }); },
  });
}

// ─── Item Models ───
export function useItemModels(page = 1) {
  return useQuery({
    queryKey: ["stock", "item-models", page] as const,
    queryFn: () => fetchItemModels(page),
  });
}

export function useCreateItemModel() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createItemModel,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["stock", "item-models"] }); },
  });
}

export function useUpdateItemModel() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Parameters<typeof updateItemModel>[1] }) => updateItemModel(id, data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["stock", "item-models"] }); },
  });
}

// ─── Stock Items ───
export function useStockItems(page = 1) {
  return useQuery({
    queryKey: stockKeys.items(page),
    queryFn: () => fetchStockItems(page),
  });
}

// ─── Movements ───
export function useMovements(params: Record<string, unknown> = {}) {
  return useQuery({
    queryKey: stockKeys.movements(params),
    queryFn: () => fetchMovements(params as Parameters<typeof fetchMovements>[0]),
  });
}

// ─── Lookups ───
export function useLookupItems() {
  return useQuery({
    queryKey: ["stock", "lookups", "items"] as const,
    queryFn: fetchLookupItems,
    staleTime: 60_000,
  });
}

export function useLookupWarehouses() {
  return useQuery({
    queryKey: ["stock", "lookups", "warehouses"] as const,
    queryFn: fetchLookupWarehouses,
    staleTime: 60_000,
  });
}

// ─── Operation Mutations ───
export function useReceiveQuantity() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: receiveQuantity,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["stock"] });
    },
  });
}

export function useIssueQuantity() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: issueQuantity,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["stock"] });
    },
  });
}

export function useTransferQuantity() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: transferQuantity,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["stock"] });
    },
  });
}

// ─── Adjustment Mutations ───
export function useCreateAdjustmentSession() {
  return useMutation({ mutationFn: createAdjustmentSession });
}

export function useUpsertAdjustmentLines() {
  return useMutation({
    mutationFn: ({ sessionId, lines }: { sessionId: string; lines: Parameters<typeof upsertAdjustmentLines>[1] }) =>
      upsertAdjustmentLines(sessionId, lines),
  });
}

export function useConfirmAdjustment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: confirmAdjustmentSession,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["stock"] });
    },
  });
}

export function useCancelAdjustment() {
  return useMutation({ mutationFn: cancelAdjustmentSession });
}
