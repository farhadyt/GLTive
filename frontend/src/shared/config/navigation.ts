import type { LucideIcon } from "lucide-react";
import {
  LayoutDashboard,
  Package,
  Tags,
  History,
} from "lucide-react";
import { STOCK_PERMISSIONS } from "./permissions";

export interface NavItem {
  label: string;
  path: string;
  icon: LucideIcon;
  permission?: string;
  children?: NavItem[];
}

export interface NavGroup {
  label: string;
  items: NavItem[];
}

/**
 * Navigation registry — ONLY routes that exist in the router.
 * When a new page is implemented and added to router.tsx,
 * add it here too. Do NOT add routes that lead to 404.
 */
export const NAVIGATION: NavGroup[] = [
  {
    label: "nav.stock",
    items: [
      {
        label: "nav.dashboard",
        path: "/stock",
        icon: LayoutDashboard,
        permission: STOCK_PERMISSIONS.VIEW,
      },
      {
        label: "nav.categories",
        path: "/stock/categories",
        icon: Tags,
        permission: STOCK_PERMISSIONS.VIEW,
      },
      {
        label: "nav.items",
        path: "/stock/items",
        icon: Package,
        permission: STOCK_PERMISSIONS.VIEW,
      },
      {
        label: "nav.movements",
        path: "/stock/movements",
        icon: History,
        permission: STOCK_PERMISSIONS.HISTORY_VIEW,
      },
    ],
  },
];
