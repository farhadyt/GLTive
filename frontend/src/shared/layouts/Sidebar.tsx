import { useTranslation } from "react-i18next";
import { NavLink } from "react-router";
import {
  LayoutDashboard,
  Tags,
  Bookmark,
  Truck,
  Warehouse,
  Box,
  Package,
  PackagePlus,
  PackageMinus,
  ArrowRightLeft,
  ClipboardCheck,
  Bell,
  HelpCircle,
  LogOut,
  Plus,
} from "lucide-react";
import { useAuth } from "@/shared/lib/auth";

const NAV_ITEMS = [
  { label: "nav.dashboard", path: "/stock", icon: LayoutDashboard, end: true },
  { label: "nav.categories", path: "/stock/categories", icon: Tags },
  { label: "nav.brands", path: "/stock/brands", icon: Bookmark },
  { label: "nav.vendors", path: "/stock/vendors", icon: Truck },
  { label: "nav.warehouses", path: "/stock/warehouses", icon: Warehouse },
  { label: "nav.item_models", path: "/stock/item-models", icon: Box },
  { label: "nav.items", path: "/stock/items", icon: Package },
  { type: "divider" as const },
  { label: "nav.receive", path: "/stock/receive", icon: PackagePlus },
  { label: "nav.issue", path: "/stock/issue", icon: PackageMinus },
  { label: "nav.transfer", path: "/stock/transfer", icon: ArrowRightLeft },
  { label: "nav.adjustments", path: "/stock/adjustments", icon: ClipboardCheck },
  { label: "nav.alerts", path: "/stock/alerts", icon: Bell },
] as const;

export function Sidebar() {
  const { t } = useTranslation();
  const { logout } = useAuth();

  return (
    <aside className="fixed left-0 top-0 h-screen w-[240px] z-40 bg-[var(--surface-container-low)] flex flex-col border-r border-white/5 pt-16 pb-4">
      {/* Logo Section */}
      <div className="px-6 mb-8">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-[var(--radius-md)] btn-primary-gradient flex items-center justify-center">
            <span className="text-white font-bold text-sm">G</span>
          </div>
          <div>
            <h2 className="text-xl font-black bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-primary-container)] bg-clip-text text-transparent">
              GLTive Stock
            </h2>
            <p className="text-[0.65rem] text-[var(--color-outline)] font-bold uppercase tracking-widest">
              Industrial Architect
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto no-scrollbar text-sm font-medium space-y-1">
        {NAV_ITEMS.map((item, i) => {
          if ("type" in item && item.type === "divider") {
            return <div key={i} className="h-px bg-white/5 mx-4 my-2" />;
          }
          if (!("path" in item)) return null;
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={"end" in item && item.end}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 mx-2 rounded-lg transition-all duration-200 ${
                  isActive
                    ? "bg-[var(--surface-container-highest)] text-white translate-x-0.5"
                    : "text-slate-400 hover:text-white hover:bg-[var(--surface-container)]"
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <Icon
                    className={`w-5 h-5 shrink-0 ${
                      isActive ? "text-[var(--color-primary)]" : ""
                    }`}
                  />
                  <span>{t(item.label)}</span>
                </>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* New Entry Button */}
      <div className="px-4 py-2">
        <button className="w-full py-2.5 btn-primary-gradient font-semibold rounded-xl flex items-center justify-center gap-2 shadow-lg shadow-[var(--color-primary)]/20 text-sm">
          <Plus className="w-5 h-5" />
          {t("common.create")}
        </button>
      </div>

      {/* Footer */}
      <footer className="mt-auto space-y-1">
        <a
          href="#"
          className="flex items-center gap-3 text-slate-400 hover:text-white px-3 py-2 mx-2 hover:bg-[var(--surface-container)] rounded-lg transition-colors text-sm"
        >
          <HelpCircle className="w-5 h-5" />
          <span>Support</span>
        </a>
        <button
          onClick={logout}
          className="flex items-center gap-3 text-slate-400 hover:text-white px-3 py-2 mx-2 hover:bg-[var(--surface-container)] rounded-lg transition-colors w-full text-sm text-left"
        >
          <LogOut className="w-5 h-5" />
          <span>{t("auth.logout")}</span>
        </button>
      </footer>
    </aside>
  );
}
