import { Activity, Database, Globe, Layers, ShieldCheck } from 'lucide-react'
import { useState } from 'react'

export function Navbar() {
  const [lang, setLang] = useState<'en' | 'ar'>('en')

  return (
    <header className="sticky top-0 z-40 flex h-16 w-full items-center justify-between border-b border-slate-800 bg-slate-950/90 px-6 backdrop-blur-md">
      {/* Brand & Platform title */}
      <div className="flex items-center gap-3">
        <div className="flex size-9 items-center justify-center rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
          <Layers className="size-5" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-bold tracking-tight text-white">
              {lang === 'en' ? 'CCDI PLATFORM' : 'منصة ذكاء الإنشاءات السعودية'}
            </span>
            <span className="rounded bg-emerald-500/20 px-1.5 py-0.5 text-[10px] font-semibold text-emerald-400">
              PROD-READY
            </span>
          </div>
          <p className="text-xs text-slate-400">
            {lang === 'en'
              ? 'Saudi Giga-Project Causality & Dependency Intelligence'
              : 'منصة تحليل السببية والاعتماديات للمشاريع الكبرى'}
          </p>
        </div>
      </div>

      {/* System Status Indicators & Controls */}
      <div className="flex items-center gap-4">
        <div className="hidden items-center gap-2 rounded-full border border-slate-800 bg-slate-900/60 px-3 py-1 text-xs text-slate-300 md:flex">
          <span className="flex size-2 rounded-full bg-emerald-400 animate-pulse" />
          <Database className="size-3.5 text-slate-400" />
          <span>PostgreSQL + pgvector &bull; Neo4j &bull; Redis</span>
        </div>

        <div className="hidden items-center gap-2 rounded-full border border-slate-800 bg-slate-900/60 px-3 py-1 text-xs text-slate-300 sm:flex">
          <Activity className="size-3.5 text-emerald-400" />
          <span>CPM Engine: Active</span>
        </div>

        <div className="flex items-center gap-2 border-l border-slate-800 pl-4">
          <button
            onClick={() => setLang(lang === 'en' ? 'ar' : 'en')}
            className="flex items-center gap-1.5 rounded-lg border border-slate-800 bg-slate-900 px-3 py-1.5 text-xs font-medium text-slate-200 transition hover:border-slate-700 hover:bg-slate-800"
            title="Toggle Arabic / English"
          >
            <Globe className="size-3.5 text-emerald-400" />
            <span>{lang === 'en' ? 'العربية (AR)' : 'English (EN)'}</span>
          </button>

          <div className="flex items-center gap-1.5 rounded-lg bg-slate-900 border border-slate-800 px-2.5 py-1.5 text-xs font-medium text-slate-300">
            <ShieldCheck className="size-3.5 text-emerald-400" />
            <span className="text-[11px] font-mono text-slate-400">Tenant: CONTRACTOR-X</span>
          </div>
        </div>
      </div>
    </header>
  )
}
