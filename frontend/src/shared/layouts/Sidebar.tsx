import { useTranslation } from "react-i18next";
import { NavLink } from "react-router";
import { PanelLeftClose, PanelLeft, LogOut } from "lucide-react";
import { useAuth } from "@/shared/lib/auth";
import { usePermission } from "@/shared/lib/permissions";
import { NAVIGATION, type NavItem } from "@/shared/config/navigation";

function NavItemLink({ item, collapsed }: { item: NavItem; collapsed: boolean }) {
  const { t } = useTranslation();
  const hasPermission = usePermission(item.permission || "");
  if (item.permission && !hasPermission) return null;

  const Icon = item.icon;
  return (
    <NavLink
      to={item.path}
      end={item.path === "/stock"}
      className={({ isActive }) =>
        `flex items-center gap-3 px-3 py-2 mx-2 rounded-lg transition-all duration-200 ${
          isActive
            ? "bg-[var(--surface-container-highest)] text-white translate-x-0.5"
            : "text-slate-400 hover:text-white hover:bg-[var(--surface-container)]"
        }`
      }
      title={collapsed ? t(item.label) : undefined}
    >
      {({ isActive }) => (
        <>
          <Icon
            className={`w-5 h-5 shrink-0 ${
              isActive ? "text-[var(--color-primary)]" : ""
            }`}
          />
          {!collapsed && <span className="truncate">{t(item.label)}</span>}
        </>
      )}
    </NavLink>
  );
}

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const { t } = useTranslation();
  const { logout } = useAuth();

  return (
    <aside
      className={`fixed left-0 top-0 h-screen z-40 bg-[var(--surface-container-low)] flex flex-col border-r border-white/5 pt-16 pb-4 transition-[width] duration-200 ${
        collapsed ? "w-16" : "w-[240px]"
      }`}
    >
      {/* Logo */}
      <div className={`mb-8 ${collapsed ? "px-3" : "px-6"}`}>
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-[var(--radius-md)] btn-primary-gradient flex items-center justify-center shrink-0">
            <span className="text-white font-bold text-sm">G</span>
          </div>
          {!collapsed && (
            <div>
              <h2 className="text-xl font-black bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-primary-container)] bg-clip-text text-transparent">
                GLTive Stock
              </h2>
              <p className="text-[0.65rem] text-[var(--color-outline)] font-bold uppercase tracking-widest">
                {t("shell.brand_subtitle")}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation — driven by shared/config/navigation.ts */}
      <nav className="flex-1 overflow-y-auto no-scrollbar text-sm font-medium space-y-4">
        {NAVIGATION.map((group) => (
          <div key={group.label}>
            {!collapsed && (
              <p className="px-5 mb-2 text-[10px] font-bold uppercase tracking-widest text-[var(--color-outline)]">
                {t(group.label)}
              </p>
            )}
            <div className="space-y-0.5">
              {group.items.map((item) => (
                <NavItemLink key={item.path} item={item} collapsed={collapsed} />
              ))}
            </div>
          </div>
        ))}
      </nav>

      {/* Footer */}
      <footer className="mt-auto space-y-1">
        <button
          onClick={logout}
          className={`flex items-center gap-3 text-slate-400 hover:text-white py-2 mx-2 hover:bg-[var(--surface-container)] rounded-lg transition-colors w-full text-sm text-left ${
            collapsed ? "justify-center px-0" : "px-3"
          }`}
          title={collapsed ? t("auth.logout") : undefined}
        >
          <LogOut className="w-5 h-5 shrink-0" />
          {!collapsed && <span>{t("auth.logout")}</span>}
        </button>
        <button
          onClick={onToggle}
          className={`flex items-center gap-3 text-[var(--color-outline)] hover:text-white py-2 mx-2 hover:bg-[var(--surface-container)] rounded-lg transition-colors w-full text-sm ${
            collapsed ? "justify-center px-0" : "px-3"
          }`}
        >
          {collapsed ? (
            <PanelLeft className="w-5 h-5" />
          ) : (
            <>
              <PanelLeftClose className="w-5 h-5 shrink-0" />
              <span className="truncate">{t("shell.collapse_sidebar")}</span>
            </>
          )}
        </button>
      </footer>
    </aside>
  );
}
