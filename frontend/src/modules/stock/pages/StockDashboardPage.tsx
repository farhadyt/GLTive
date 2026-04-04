import { useTranslation } from "react-i18next";
import {
  Package,
  Warehouse as WarehouseIcon,
  AlertTriangle,
  ArrowRightLeft,
  QrCode,
  TrendingUp,
  Zap,
  ShieldCheck,
  History,
  ChevronRight,
  PackagePlus,
  ArrowUpDown,
  Settings2,
} from "lucide-react";

export function StockDashboardPage() {
  const { t } = useTranslation();

  return (
    <>
      {/* Breadcrumbs & Header */}
      <div className="mb-8 flex justify-between items-end">
        <div>
          <nav className="flex items-center gap-2 text-[var(--color-outline)] text-xs font-medium uppercase tracking-wider mb-2">
            <span>{t("nav.stock")}</span>
            <ChevronRight className="w-3 h-3" />
            <span className="text-[var(--color-primary)]">{t("nav.dashboard")}</span>
          </nav>
          <h1 className="text-3xl font-bold text-white tracking-tight">
            {t("nav.dashboard")}
          </h1>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 bg-[var(--surface-container-low)] rounded-lg text-xs font-semibold text-[var(--color-secondary)]">
            <span className="w-2 h-2 rounded-full bg-[var(--color-secondary)] animate-pulse-dot" />
            {t("dashboard.live_feed").toUpperCase()}
          </div>
          <button className="bg-[var(--surface-container-highest)] text-white px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 hover:bg-[var(--surface-bright)] transition-colors">
            {t("common.this_week")}
          </button>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
        {/* {t("dashboard.total_active_stock")} */}
        <div className="bg-[var(--surface-container-low)] p-6 rounded-xl border-l-4 border-[var(--color-primary)] relative overflow-hidden">
          <div className="flex justify-between items-start mb-4">
            <p className="text-[var(--color-outline)] text-xs font-bold uppercase tracking-widest">
              {t("dashboard.total_active_stock")}
            </p>
            <Package className="w-5 h-5 text-[var(--color-primary)]/50" />
          </div>
          <div className="flex items-end gap-3">
            <span className="text-4xl font-bold text-white tracking-tight">42.8k</span>
            <span className="text-[var(--color-secondary)] text-xs font-bold pb-1 flex items-center gap-0.5">
              <TrendingUp className="w-3.5 h-3.5" />
              +12%
            </span>
          </div>
          <div className="mt-4 h-1 w-full bg-[var(--surface-container)] rounded-full overflow-hidden">
            <div className="h-full bg-[var(--color-primary)] w-[75%] rounded-full" />
          </div>
        </div>

        {/* {t("dashboard.total_warehouses")} */}
        <div className="bg-[var(--surface-container-low)] p-6 rounded-xl relative overflow-hidden">
          <div className="flex justify-between items-start mb-4">
            <p className="text-[var(--color-outline)] text-xs font-bold uppercase tracking-widest">
              {t("dashboard.total_warehouses")}
            </p>
            <WarehouseIcon className="w-5 h-5 text-[var(--color-outline)]" />
          </div>
          <div className="flex items-end gap-3">
            <span className="text-4xl font-bold text-white tracking-tight">18</span>
            <span className="text-[var(--color-outline)] text-xs font-bold pb-1">{t("common.global").toUpperCase()}</span>
          </div>
          <div className="mt-4 flex gap-1">
            <div className="h-2 w-full bg-[var(--color-primary)]/20 rounded-sm" />
            <div className="h-2 w-full bg-[var(--color-primary)]/40 rounded-sm" />
            <div className="h-2 w-full bg-[var(--color-primary)] rounded-sm" />
          </div>
        </div>

        {/* {t("dashboard.low_stock_alerts")} */}
        <div className="bg-[var(--surface-container-low)] p-6 rounded-xl border-l-4 border-[var(--color-error)] relative overflow-hidden">
          <div className="flex justify-between items-start mb-4">
            <p className="text-[var(--color-outline)] text-xs font-bold uppercase tracking-widest">
              {t("dashboard.low_stock_alerts")}
            </p>
            <AlertTriangle className="w-5 h-5 text-[var(--color-error)]/50" />
          </div>
          <div className="flex items-end gap-3">
            <span className="text-4xl font-bold text-white tracking-tight">124</span>
            <span className="px-2 py-0.5 bg-[var(--color-error)]/10 text-[var(--color-error)] rounded-full text-[10px] font-black tracking-tighter mb-1 uppercase">
              {t("common.danger").toUpperCase()}
            </span>
          </div>
          <p className="mt-4 text-xs text-[var(--color-outline)] italic leading-tight">
            {t("dashboard.requires_procurement")}
          </p>
        </div>

        {/* Movements */}
        <div className="bg-[var(--surface-container-low)] p-6 rounded-xl relative overflow-hidden">
          <div className="flex justify-between items-start mb-4">
            <p className="text-[var(--color-outline)] text-xs font-bold uppercase tracking-widest">
              {t("dashboard.movements_title")}
            </p>
            <ArrowRightLeft className="w-5 h-5 text-[var(--color-outline)]" />
          </div>
          <div className="flex items-end gap-3">
            <span className="text-4xl font-bold text-white tracking-tight">3,102</span>
            <span className="text-[var(--color-secondary)] text-xs font-bold pb-1 flex items-center gap-0.5">
              <Zap className="w-3.5 h-3.5" />
              {t("common.active").toUpperCase()}
            </span>
          </div>
          <div className="mt-4 flex items-center justify-between">
            <span className="text-[10px] text-[var(--color-outline)]">{t("common.out").toUpperCase()}: 1.4k</span>
            <span className="text-[10px] text-[var(--color-outline)]">{t("common.in").toUpperCase()}: 1.7k</span>
          </div>
        </div>

        {/* {t("dashboard.serialized_items")} */}
        <div className="bg-[var(--surface-container-low)] p-6 rounded-xl relative overflow-hidden">
          <div className="flex justify-between items-start mb-4">
            <p className="text-[var(--color-outline)] text-xs font-bold uppercase tracking-widest">
              {t("dashboard.serialized_items")}
            </p>
            <QrCode className="w-5 h-5 text-[var(--color-outline)]" />
          </div>
          <div className="flex items-end gap-3">
            <span className="text-4xl font-bold text-white tracking-tight">9,420</span>
          </div>
          <div className="mt-4 text-[10px] text-[var(--color-outline)] flex items-center gap-2">
            <ShieldCheck className="w-3.5 h-3.5 text-[var(--color-secondary)]" />
            98% {t("dashboard.scan_accuracy").toUpperCase()}
          </div>
        </div>
      </div>

      {/* Middle Section: Bento Style */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-8">
        {/* Recent Movements Feed */}
        <div className="lg:col-span-5 bg-[var(--surface-container-low)] rounded-2xl overflow-hidden shadow-xl flex flex-col h-[520px]">
          <div className="p-6 border-b border-white/5 flex justify-between items-center bg-[var(--surface-container-highest)]/20">
            <h3 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
              <History className="w-4 h-4 text-[var(--color-secondary)]" />
              {t("dashboard.recent_movements")}
            </h3>
            <button className="text-xs text-[var(--color-primary)] font-semibold hover:underline">
              {t("common.view_all")}
            </button>
          </div>
          <div className="flex-1 overflow-y-auto no-scrollbar p-6 space-y-4">
            <MovementEntry
              icon={<PackagePlus className="w-5 h-5" />}
              iconBg="bg-[var(--color-on-secondary-container)]"
              iconColor="text-[var(--color-secondary)]"
              title="Item: CX-900 Turbine"
              subtitle="Stock In • Batch #9012"
              value="+124"
              valueColor="text-[var(--color-secondary)]"
              time="2m ago"
            />
            <MovementEntry
              icon={<ArrowUpDown className="w-5 h-5" />}
              iconBg="bg-[var(--surface-container-highest)]"
              iconColor="text-[var(--color-primary)]"
              title="Lithium Cell Packs"
              subtitle="Transfer • WH-01 to WH-04"
              value="500"
              valueColor="text-white"
              time="15m ago"
            />
            <MovementEntry
              icon={<ArrowRightLeft className="w-5 h-5" />}
              iconBg="bg-[var(--color-error-container)]/30"
              iconColor="text-[var(--color-error)]"
              title="Steel Beams H-Type"
              subtitle="Stock Out • Order #TX-45"
              value="-22"
              valueColor="text-[var(--color-error)]"
              time="45m ago"
            />
            <MovementEntry
              icon={<PackagePlus className="w-5 h-5" />}
              iconBg="bg-[var(--color-on-secondary-container)]"
              iconColor="text-[var(--color-secondary)]"
              title="Hydraulic Pump"
              subtitle="Stock In • Vendor: GlobalInd"
              value="+15"
              valueColor="text-[var(--color-secondary)]"
              time="1h ago"
            />
            <MovementEntry
              icon={<Settings2 className="w-5 h-5" />}
              iconBg="bg-[var(--surface-container-highest)]"
              iconColor="text-[var(--color-outline)]"
              title="Copper Wire Spool"
              subtitle="Adjustment • Audit Correction"
              value="-3"
              valueColor="text-white"
              time="3h ago"
            />
          </div>
        </div>

        {/* Critical Low Stock Alerts */}
        <div className="lg:col-span-7 bg-[var(--surface-container-low)] rounded-2xl overflow-hidden shadow-xl flex flex-col h-[520px]">
          <div className="p-6 border-b border-white/5 flex justify-between items-center bg-[var(--surface-container-highest)]/20">
            <h3 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-[var(--color-error)]" />
              {t("dashboard.critical_low_stock")}
            </h3>
            <span className="px-2 py-1 bg-[var(--color-error-container)] text-[var(--color-error)] rounded text-[10px] font-black">
              12 {t("dashboard.critical").toUpperCase()}
            </span>
          </div>
          <div className="flex-1 overflow-x-auto no-scrollbar">
            <table className="w-full text-left border-collapse">
              <thead className="bg-[var(--surface-container-lowest)]/50 text-[10px] text-[var(--color-outline)] uppercase font-black tracking-widest">
                <tr>
                  <th className="px-6 py-4">{t("dashboard.item_name")}</th>
                  <th className="px-6 py-4">{t("dashboard.warehouse")}</th>
                  <th className="px-6 py-4 text-center">{t("dashboard.available")}</th>
                  <th className="px-6 py-4 text-center">{t("dashboard.threshold")}</th>
                  <th className="px-6 py-4 text-right">{t("dashboard.action")}</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                <AlertRow name="Titanium Bolt M8" warehouse="Main Logistics Hub" available={42} threshold={500} />
                <AlertRow name="Compressor Fan Blade" warehouse="Warehouse B-South" available={5} threshold={25} alt />
                <AlertRow name="Circuit Board K-4" warehouse="North Depot" available={112} threshold={1000} />
                <AlertRow name="Industrial Lubricant SL" warehouse="Central Storage" available={18} threshold={60} alt />
                <AlertRow name="Safety Goggles" warehouse="East Wing" available={204} threshold={250} />
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Stock Distribution */}
      <div className="bg-[var(--surface-container-low)] rounded-2xl p-8 shadow-xl">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h3 className="text-sm font-bold text-white uppercase tracking-widest">
              {t("dashboard.stock_distribution")}
            </h3>
            <p className="text-xs text-[var(--color-outline)] mt-1">
              {t("dashboard.distribution_desc")}
            </p>
          </div>
          <div className="flex items-center gap-4 text-[10px] font-bold uppercase text-[var(--color-outline)]">
            <span className="flex items-center gap-1.5">
              <span className="w-3 h-1.5 bg-[var(--color-primary)] rounded-sm" /> {t("common.on_hand")}
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-3 h-1.5 bg-[var(--color-secondary)] rounded-sm" /> {t("common.reserved")}
            </span>
          </div>
        </div>
        <div className="space-y-5">
          <DistributionBar label="Mechanical Parts" value={12400} percentage={95} />
          <DistributionBar label="Electrical Components" value={8902} percentage={72} />
          <DistributionBar label="Raw Materials" value={5320} percentage={55} />
          <DistributionBar label="Facility Supplies" value={3850} percentage={40} />
          <DistributionBar label="Safety Equipment" value={2980} percentage={32} reserved />
        </div>
      </div>
    </>
  );
}

function MovementEntry({
  icon,
  iconBg,
  iconColor,
  title,
  subtitle,
  value,
  valueColor,
  time,
}: {
  icon: React.ReactNode;
  iconBg: string;
  iconColor: string;
  title: string;
  subtitle: string;
  value: string;
  valueColor: string;
  time: string;
}) {
  return (
    <div className="flex items-center justify-between p-3 bg-[var(--surface)] rounded-xl hover:bg-[var(--surface-container)] transition-colors">
      <div className="flex items-center gap-4">
        <div className={`w-10 h-10 rounded-lg ${iconBg} flex items-center justify-center ${iconColor}`}>
          {icon}
        </div>
        <div>
          <h4 className="text-sm font-bold text-white">{title}</h4>
          <p className="text-[10px] text-[var(--color-outline)] uppercase tracking-tight">{subtitle}</p>
        </div>
      </div>
      <div className="text-right">
        <p className={`text-sm font-black ${valueColor}`}>{value}</p>
        <p className="text-[10px] text-[var(--color-outline)] italic">{time}</p>
      </div>
    </div>
  );
}

function AlertRow({
  name,
  warehouse,
  available,
  threshold,
  alt = false,
}: {
  name: string;
  warehouse: string;
  available: number;
  threshold: number;
  alt?: boolean;
}) {
  const { t } = useTranslation();
  return (
    <tr className={`hover:bg-white/5 transition-colors ${alt ? "bg-white/[0.02]" : ""}`}>
      <td className="px-6 py-4 font-bold text-white">{name}</td>
      <td className="px-6 py-4 text-slate-400">{warehouse}</td>
      <td className="px-6 py-4 text-center">
        <span className="text-[var(--color-error)] font-black">{available.toLocaleString()}</span>
      </td>
      <td className="px-6 py-4 text-center text-[var(--color-outline)]">{threshold.toLocaleString()}</td>
      <td className="px-6 py-4 text-right">
        <button className="text-[var(--color-primary)] text-xs font-bold uppercase tracking-tighter hover:bg-[var(--color-primary)]/10 px-3 py-1 rounded transition-colors">
          {t("common.reorder")}
        </button>
      </td>
    </tr>
  );
}

function DistributionBar({
  label,
  value,
  percentage,
  reserved = false,
}: {
  label: string;
  value: number;
  percentage: number;
  reserved?: boolean;
}) {
  const { t } = useTranslation();
  return (
    <div>
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-white">{label}</span>
        <span className="text-xs font-bold text-[var(--color-outline)]">
          {value.toLocaleString()} {t("common.units")}
        </span>
      </div>
      <div className="h-2 w-full bg-[var(--surface-container)] rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${reserved ? "bg-[var(--color-secondary)]" : "bg-[var(--color-primary)]"}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
