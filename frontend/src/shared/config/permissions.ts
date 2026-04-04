export const STOCK_PERMISSIONS = {
  VIEW: "stock.view",
  MANAGE: "stock.manage",
  MASTER_MANAGE: "stock.master.manage",
  RECEIVE: "stock.receive",
  ISSUE: "stock.issue",
  TRANSFER: "stock.transfer",
  ADJUST: "stock.adjust",
  ALERT_MANAGE: "stock.alert.manage",
  HISTORY_VIEW: "stock.history.view",
} as const;

export type PermissionCode = (typeof STOCK_PERMISSIONS)[keyof typeof STOCK_PERMISSIONS];
