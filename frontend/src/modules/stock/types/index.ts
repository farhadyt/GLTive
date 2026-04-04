export interface Category {
  id: string;
  code: string;
  name: string;
  description: string;
  parent_category_id: string | null;
  sort_order: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface StockItem {
  id: string;
  item_model_id: string;
  warehouse_id: string;
  internal_code: string | null;
  item_name_override: string | null;
  tracking_type: "quantity_based" | "serialized";
  quantity_on_hand: string;
  quantity_reserved: string;
  quantity_available: string;
  minimum_stock_level_override: string | null;
  last_received_at: string | null;
  last_issued_at: string | null;
  notes: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Movement {
  id: string;
  movement_type: string;
  stock_item_id: string;
  stock_item_name: string;
  quantity: string;
  unit_cost: string | null;
  source_warehouse_name: string | null;
  target_warehouse_name: string | null;
  reference_type: string | null;
  reference_id: string | null;
  reason_code: string | null;
  note: string;
  performed_by_username: string | null;
  performed_at: string;
  created_at: string;
}

export interface DashboardSummary {
  total_active_stock_items: number;
  total_warehouses: number;
  low_stock_count: number;
  recent_movements_count: number;
  serialized_count: number;
  quantity_based_count: number;
}

export interface DashboardMovement {
  id: string;
  movement_type: string;
  stock_item_id: string;
  stock_item_name: string;
  quantity: string;
  performed_at: string;
  performed_by_username: string | null;
  source_warehouse_name: string | null;
  target_warehouse_name: string | null;
}

export interface LowStockItem {
  id: string;
  item_name: string;
  warehouse_code: string;
  warehouse_name: string;
  quantity_on_hand: string;
  quantity_available: string;
  tracking_type: string;
}
