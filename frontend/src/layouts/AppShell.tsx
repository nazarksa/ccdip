import { Blocks, ShieldCheck } from 'lucide-react'
import { Outlet } from 'react-router-dom'

export function AppShell() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-900/80">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <Blocks className="size-6 text-emerald-400" aria-hidden="true" />
            <div>
              <p className="font-semibold">CCDI Platform</p>
              <p className="text-xs text-slate-400">Architecture foundation</p>
            </div>
          </div>
          <span className="flex items-center gap-2 text-sm text-slate-400">
            <ShieldCheck className="size-4" aria-hidden="true" />
            Enterprise controls planned
          </span>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-6 py-12">
        <Outlet />
      </main>
    </div>
  )
}
