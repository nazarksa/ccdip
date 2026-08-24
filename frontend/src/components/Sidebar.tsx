import {
  AlertTriangle,
  Calendar,
  Compass,
  FileCheck,
  LayoutDashboard,
  Network,
  Truck,
  Zap,
} from 'lucide-react'
import { NavLink } from 'react-router-dom'

const NAV_ITEMS = [
  {
    path: '/',
    label: 'Executive Command Center',
    labelAr: 'مركز القيادة التنفيذي',
    icon: LayoutDashboard,
  },
  {
    path: '/project-360',
    label: 'Project 360 View',
    labelAr: 'عرض المشروع 360',
    icon: Compass,
  },
  {
    path: '/graph-explorer',
    label: 'Causality & Graph Explorer',
    labelAr: 'مستكشف شبكة السببية',
    icon: Network,
    badge: 'GraphRAG',
  },
  {
    path: '/schedule',
    label: 'Schedule Intelligence & CPM',
    labelAr: 'ذكاء الجدول والمسار الحرج',
    icon: Calendar,
  },
  {
    path: '/scenarios',
    label: 'What-If Simulation Sandbox',
    labelAr: 'محاكاة سيناريوهات التأثير',
    icon: Zap,
    badge: 'Sandbox',
  },
  {
    path: '/supply-chain',
    label: 'Supply Chain & SPOF Analysis',
    labelAr: 'سلاسل الإمداد ونقاط الاختناق',
    icon: Truck,
  },
  {
    path: '/evidence',
    label: 'Evidence & Claim Vault',
    labelAr: 'خزينة الأدلة والتوثيق',
    icon: FileCheck,
  },
]

export function Sidebar() {
  return (
    <aside className="flex w-64 flex-col justify-between border-r border-slate-800 bg-slate-950 p-4">
      <div className="space-y-6">
        <div>
          <p className="px-3 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
            Intelligence Modules
          </p>
          <nav className="mt-3 space-y-1">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  end={item.path === '/'}
                  className={({ isActive }) =>
                    `group flex items-center justify-between rounded-lg px-3 py-2.5 text-xs font-medium transition ${
                      isActive
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-sm'
                        : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'
                    }`
                  }
                >
                  <div className="flex items-center gap-2.5">
                    <Icon className="size-4 shrink-0 text-slate-400 group-hover:text-emerald-400 transition-colors" />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[9px] font-semibold text-slate-300">
                      {item.badge}
                    </span>
                  )}
                </NavLink>
              )
            })}
          </nav>
        </div>

        <div className="rounded-lg border border-slate-800/80 bg-slate-900/40 p-3 text-xs">
          <div className="flex items-center gap-1.5 text-amber-400 font-semibold mb-1">
            <AlertTriangle className="size-3.5" />
            <span>Active Causal Alert</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Supplier Z delivery delay (+12d) propagating into Milestone M17 via Activity A45.
          </p>
        </div>
      </div>

      {/* Footer Info */}
      <div className="border-t border-slate-800/80 pt-3 text-[11px] text-slate-500 space-y-1">
        <div className="flex items-center justify-between">
          <span>Engine Status</span>
          <span className="text-emerald-400 font-mono">100% OK</span>
        </div>
        <div className="flex items-center justify-between">
          <span>Version</span>
          <span className="font-mono text-slate-400">v0.1.0 Enterprise</span>
        </div>
      </div>
    </aside>
  )
}
