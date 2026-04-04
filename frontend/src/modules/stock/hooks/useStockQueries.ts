import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  fetchDashboardSummary,
  fetchRecentMovements,
  fetchLowStockItems,
  fetchCategories,
  createCategory,
  updateCategory,
  fetchStockItems,
  fetchMovements,
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
