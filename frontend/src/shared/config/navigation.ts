import type { LucideIcon } from "lucide-react";
import {
  LayoutDashboard,
  Package,
  Tags,
  History,
  PackagePlus,
  PackageMinus,
  ArrowRightLeft,
  ClipboardCheck,
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
        label: "nav.receive",
        path: "/stock/receive",
        icon: PackagePlus,
        permission: STOCK_PERMISSIONS.RECEIVE,
      },
      {
        label: "nav.issue",
        path: "/stock/issue",
        icon: PackageMinus,
        permission: STOCK_PERMISSIONS.ISSUE,
      },
      {
        label: "nav.transfer",
        path: "/stock/transfer",
        icon: ArrowRightLeft,
        permission: STOCK_PERMISSIONS.TRANSFER,
      },
      {
        label: "nav.adjustments",
        path: "/stock/adjustments",
        icon: ClipboardCheck,
        permission: STOCK_PERMISSIONS.ADJUST,
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
