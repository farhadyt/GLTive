import { useTranslation } from "react-i18next";
import { NavLink } from "react-router";
import { PanelLeftClose, PanelLeft } from "lucide-react";
import { NAVIGATION } from "@/shared/config/navigation";
import { usePermission } from "@/shared/lib/permissions";

function NavItemLink({
  item,
  collapsed,
}: {
  item: (typeof NAVIGATION)[0]["items"][0];
  collapsed: boolean;
}) {
  const { t } = useTranslation();
  const hasPermission = usePermission(item.permission || "");
  if (item.permission && !hasPermission) return null;

  const Icon = item.icon;
  return (
    <NavLink
      to={item.path}
      end={item.path === "/stock"}
      className={({ isActive }) =>
        `flex items-center gap-3 px-3 py-2 rounded-[var(--radius-md)] text-sm font-medium transition-colors ${
          isActive
            ? "bg-[var(--color-primary-50)] text-[var(--color-primary-700)] dark:bg-[var(--color-primary-900)]/20 dark:text-[var(--color-primary-400)]"
            : "text-[var(--text-secondary)] hover:bg-[var(--color-neutral-100)] dark:hover:bg-[var(--color-neutral-800)] hover:text-[var(--text-primary)]"
        }`
      }
      title={collapsed ? t(item.label) : undefined}
    >
      <Icon className="w-5 h-5 shrink-0" />
      {!collapsed && <span className="truncate">{t(item.label)}</span>}
    </NavLink>
  );
}

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const { t } = useTranslation();

  return (
    <aside
      className={`fixed top-0 start-0 h-full z-30 flex flex-col bg-[var(--surface-sidebar)] border-e border-[var(--border-default)] transition-[width] duration-200 ${
        collapsed ? "w-16" : "w-60"
      }`}
    >
      {/* Logo */}
      <div className="flex items-center h-14 px-4 border-b border-[var(--border-default)]">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-[var(--radius-md)] bg-[var(--color-primary-600)] flex items-center justify-center">
            <span className="text-white font-bold text-sm">G</span>
          </div>
          {!collapsed && (
            <span className="text-lg font-bold text-[var(--text-primary)] tracking-tight">
              GLTive
            </span>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-2 py-4 space-y-6">
        {NAVIGATION.map((group) => (
          <div key={group.label}>
            {!collapsed && (
              <p className="px-3 mb-2 text-[10px] font-semibold uppercase tracking-wider text-[var(--text-muted)]">
                {t(group.label)}
              </p>
            )}
            <div className="space-y-0.5">
              {group.items.map((item) => (
                <NavItemLink
                  key={item.path}
                  item={item}
                  collapsed={collapsed}
                />
              ))}
            </div>
          </div>
        ))}
      </nav>

      {/* Collapse toggle */}
      <div className="p-2 border-t border-[var(--border-default)]">
        <button
          onClick={onToggle}
          className="flex items-center justify-center w-full p-2 rounded-[var(--radius-md)] text-[var(--text-muted)] hover:bg-[var(--color-neutral-100)] dark:hover:bg-[var(--color-neutral-800)] transition-colors"
          title={
            collapsed
              ? t("shell.expand_sidebar")
              : t("shell.collapse_sidebar")
          }
        >
          {collapsed ? (
            <PanelLeft className="w-5 h-5" />
          ) : (
            <PanelLeftClose className="w-5 h-5" />
          )}
        </button>
      </div>
    </aside>
  );
}
