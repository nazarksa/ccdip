import { useQuery } from '@tanstack/react-query'
import {
  Truck,
} from 'lucide-react'
import { fetchSupplierBottlenecks } from '../api/intelligence'

export function SupplyChainPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['supply-chain-bottlenecks'],
    queryFn: fetchSupplierBottlenecks,
  })

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="size-8 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
          <p className="text-xs text-slate-400">Analyzing supplier centrality and concentration risk...</p>
        </div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="rounded-xl border border-rose-900/50 bg-rose-950/20 p-6 text-rose-300">
        <p className="font-semibold text-sm">Failed to load supply chain bottlenecks</p>
        <p className="mt-1 text-xs text-rose-400">{(error as Error)?.message}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-emerald-400">
          <Truck className="size-4" />
          <span>Supply Chain & Bottleneck Intelligence</span>
        </div>
        <h1 className="text-xl font-bold text-white sm:text-2xl mt-0.5">
          Single Points of Failure (SPOF) & Centrality Analysis
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Graph centrality metrics, multi-project supplier dependencies, and alternative supplier readiness.
        </p>
      </div>

      {/* Supplier Centrality Matrix Table */}
      <div className="space-y-4">
        {data.map((supplier) => (
          <div
            key={supplier.supplier_id}
            className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur shadow-lg"
          >
            <div className="flex flex-col justify-between gap-4 border-b border-slate-800 pb-4 sm:flex-row sm:items-center">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold text-emerald-400">[{supplier.supplier_code}]</span>
                  <h3 className="text-base font-bold text-white">{supplier.supplier_name}</h3>
                </div>
                <span className="text-xs text-slate-400 mt-0.5 block">
                  Connected to <b className="text-white font-mono">{supplier.supplied_projects_count}</b> Giga-Project Clusters
                </span>
              </div>

              <div className="flex items-center gap-3">
                <span
                  className={`rounded-full px-3 py-1 text-xs font-bold ${
                    supplier.concentration_risk.includes('High')
                      ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                      : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  }`}
                >
                  {supplier.concentration_risk}
                </span>
              </div>
            </div>

            {/* Metrics Breakdown */}
            <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div className="rounded-xl bg-slate-950/60 p-3.5 border border-slate-800">
                <span className="text-[11px] text-slate-400">Betweenness Centrality</span>
                <p className="text-xl font-bold font-mono text-white mt-1">{supplier.betweenness_centrality}</p>
                <span className="text-[10px] text-slate-500">Critical bridge between clusters</span>
              </div>

              <div className="rounded-xl bg-slate-950/60 p-3.5 border border-slate-800">
                <span className="text-[11px] text-slate-400">Lead Time Reliability</span>
                <p className="text-xl font-bold font-mono text-amber-400 mt-1">{supplier.lead_time_reliability_pct}%</p>
                <span className="text-[10px] text-slate-500">Past 90 days delivery adherence</span>
              </div>

              <div className="rounded-xl bg-slate-950/60 p-3.5 border border-slate-800">
                <span className="text-[11px] text-slate-400">Supplied Strategic Materials</span>
                <div className="mt-1 flex flex-wrap gap-1">
                  {supplier.supplied_materials.map((m, i) => (
                    <span key={i} className="rounded bg-slate-800 px-2 py-0.5 text-[10px] text-slate-300">
                      {m}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Alternative Suppliers Readiness */}
            <div className="mt-5 border-t border-slate-800 pt-4">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 block mb-2">
                Pre-Qualified Alternate Suppliers (Risk Mitigation)
              </span>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                {supplier.alternative_suppliers.map((alt, i) => (
                  <div
                    key={i}
                    className="flex items-center justify-between rounded-lg bg-slate-950/40 p-3 border border-slate-800/80"
                  >
                    <div>
                      <span className="text-xs font-medium text-white">{alt.name}</span>
                      <span className="block text-[10px] text-slate-500">Lead time: {alt.lead_time_days} days</span>
                    </div>
                    <span className="rounded bg-emerald-500/10 px-2 py-0.5 text-[10px] font-semibold text-emerald-400 border border-emerald-500/20">
                      {alt.readiness}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
