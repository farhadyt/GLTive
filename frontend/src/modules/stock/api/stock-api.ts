import { apiClient } from "@/shared/lib/api-client";
import type { ApiResponse, PaginatedData } from "@/shared/types/api";
import type {
  Category,
  StockItem,
  Movement,
  DashboardSummary,
  DashboardMovement,
  LowStockItem,
  LookupItem,
  ReceiveQuantityPayload,
  IssueQuantityPayload,
  TransferQuantityPayload,
  AdjustmentSession,
  AdjustmentLineInput,
} from "../types";

// ─── Dashboard ───
export async function fetchDashboardSummary() {
  const res = await apiClient.get<ApiResponse<DashboardSummary>>(
    "/api/v1/stock/dashboard/summary/"
  );
  return res.data.data;
}

export async function fetchRecentMovements() {
  const res = await apiClient.get<ApiResponse<DashboardMovement[]>>(
    "/api/v1/stock/dashboard/recent-movements/"
  );
  return res.data.data;
}

export async function fetchLowStockItems() {
  const res = await apiClient.get<ApiResponse<LowStockItem[]>>(
    "/api/v1/stock/dashboard/low-stock/"
  );
  return res.data.data;
}

// ─── Categories ───
export async function fetchCategories(page = 1, pageSize = 20) {
  const res = await apiClient.get<ApiResponse<PaginatedData<Category>>>(
    "/api/v1/stock/categories/",
    { params: { page, page_size: pageSize } }
  );
  return res.data.data;
}

export async function createCategory(data: { code: string; name: string; description?: string }) {
  const res = await apiClient.post<ApiResponse<Category>>(
    "/api/v1/stock/categories/",
    data
  );
  return res.data.data;
}

export async function updateCategory(id: string, data: Partial<{ code: string; name: string; description: string }>) {
  const res = await apiClient.patch<ApiResponse<Category>>(
    `/api/v1/stock/categories/${id}/`,
    data
  );
  return res.data.data;
}

// ─── Stock Items ───
export async function fetchStockItems(page = 1, pageSize = 20) {
  const res = await apiClient.get<ApiResponse<PaginatedData<StockItem>>>(
    "/api/v1/stock/items/",
    { params: { page, page_size: pageSize } }
  );
  return res.data.data;
}

// ─── Movements ───
export async function fetchMovements(params: {
  page?: number;
  page_size?: number;
  movement_type?: string;
  stock_item_id?: string;
} = {}) {
  const res = await apiClient.get<ApiResponse<PaginatedData<Movement>>>(
    "/api/v1/stock/movements/",
    { params: { page: 1, page_size: 20, ...params } }
  );
  return res.data.data;
}

// ─── Lookups ───
export async function fetchLookupItems() {
  const res = await apiClient.get<LookupItem[]>("/api/v1/stock/lookups/items/");
  return Array.isArray(res.data) ? res.data : (res.data as ApiResponse<LookupItem[]>).data || [];
}

export async function fetchLookupWarehouses() {
  const res = await apiClient.get<LookupItem[]>("/api/v1/stock/lookups/warehouses/");
  return Array.isArray(res.data) ? res.data : (res.data as ApiResponse<LookupItem[]>).data || [];
}

// ─── Operations ───
export async function receiveQuantity(data: ReceiveQuantityPayload) {
  const res = await apiClient.post<ApiResponse<Record<string, unknown>>>(
    "/api/v1/stock/receive/quantity/",
    data
  );
  return res.data.data;
}

export async function issueQuantity(data: IssueQuantityPayload) {
  const res = await apiClient.post<ApiResponse<Record<string, unknown>>>(
    "/api/v1/stock/issue/quantity/",
    data
  );
  return res.data.data;
}

export async function transferQuantity(data: TransferQuantityPayload) {
  const res = await apiClient.post<ApiResponse<Record<string, unknown>>>(
    "/api/v1/stock/transfer/quantity/",
    data
  );
  return res.data.data;
}

// ─── Adjustments ───
export async function createAdjustmentSession(data: { warehouse_id: string; reason?: string }) {
  const res = await apiClient.post<ApiResponse<AdjustmentSession>>(
    "/api/v1/stock/adjustments/",
    data
  );
  return res.data.data;
}

export async function upsertAdjustmentLines(sessionId: string, linesData: AdjustmentLineInput[]) {
  const res = await apiClient.put<ApiResponse<unknown>>(
    `/api/v1/stock/adjustments/${sessionId}/lines/`,
    { lines_data: linesData }
  );
  return res.data.data;
}

export async function confirmAdjustmentSession(sessionId: string) {
  const res = await apiClient.post<ApiResponse<Record<string, unknown>>>(
    `/api/v1/stock/adjustments/${sessionId}/confirm/`
  );
  return res.data.data;
}

export async function cancelAdjustmentSession(sessionId: string) {
  const res = await apiClient.post<ApiResponse<Record<string, unknown>>>(
    `/api/v1/stock/adjustments/${sessionId}/cancel/`
  );
  return res.data.data;
}
