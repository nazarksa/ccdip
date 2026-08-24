import { useQuery } from '@tanstack/react-query'
import {
  AlertOctagon,
  ArrowRight,
  CheckCircle2,
  ChevronRight,
  Clock,
  DollarSign,
  Layers,
  Network,
  ShieldAlert,
  Truck,
} from 'lucide-react'
import { Link } from 'react-router-dom'
import { fetchPortfolioOverview } from '../api/intelligence'

export function ExecutivePage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['portfolio-overview'],
    queryFn: fetchPortfolioOverview,
  })

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="size-8 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
          <p className="text-xs text-slate-400">Loading enterprise intelligence stream...</p>
        </div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="rounded-xl border border-rose-900/50 bg-rose-950/20 p-6 text-rose-300">
        <div className="flex items-center gap-2 font-semibold">
          <AlertOctagon className="size-5" />
          <span>Error loading intelligence overview</span>
        </div>
        <p className="mt-2 text-xs text-rose-400">
          {(error as Error)?.message ?? 'Could not retrieve data from backend.'}
        </p>
      </div>
    )
  }

  const { portfolio_summary, health_dimensions, earned_value, primary_causal_chain, supplier_bottlenecks, projects } = data

  return (
    <div className="space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col justify-between gap-4 border-b border-slate-800 pb-6 md:flex-row md:items-center">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-emerald-400">
            <span>Executive Command Center</span>
            <span>&bull;</span>
            <span>Kingdom of Saudi Arabia</span>
          </div>
          <h1 className="mt-1 text-2xl font-bold tracking-tight text-white sm:text-3xl">
            Construction Causality & Portfolio Health
          </h1>
          <p className="mt-1 text-xs text-slate-400">
            Real-time causal dependency tracking across giga-projects, supply chains, and contract milestones.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-3 text-right">
            <span className="text-[11px] uppercase tracking-wider text-slate-400">Portfolio Index</span>
            <div className="flex items-center justify-end gap-2 mt-0.5">
              <span className="text-2xl font-black text-emerald-400">{portfolio_summary.portfolio_health_score}</span>
              <span className="text-xs text-slate-400">/ 100</span>
            </div>
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-medium">Active Projects</span>
            <Layers className="size-4 text-emerald-400" />
          </div>
          <p className="mt-2 text-2xl font-bold text-white">{portfolio_summary.total_projects}</p>
          <span className="text-[11px] text-slate-500">100% telemetry coverage</span>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-medium">Active Value (SAR)</span>
            <DollarSign className="size-4 text-emerald-400" />
          </div>
          <p className="mt-2 text-2xl font-bold text-white">
            SAR {(portfolio_summary.total_contract_value_sar / 1000000).toFixed(1)}M
          </p>
          <span className="text-[11px] text-emerald-400 font-medium">Under active administration</span>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-medium">Active Delays & Variance</span>
            <Clock className="size-4 text-amber-400" />
          </div>
          <p className="mt-2 text-2xl font-bold text-amber-400">{portfolio_summary.active_delays_count} Events</p>
          <span className="text-[11px] text-amber-500/90 font-medium">Critical path impacted</span>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-medium">Critical Risks</span>
            <ShieldAlert className="size-4 text-rose-400" />
          </div>
          <p className="mt-2 text-2xl font-bold text-rose-400">{portfolio_summary.critical_risks_count} Registered</p>
          <span className="text-[11px] text-rose-400/80">Mitigation underway</span>
        </div>
      </div>

      {/* Primary Evidence-Backed Causal Chain Breakdown */}
      {primary_causal_chain && (
        <div className="rounded-2xl border border-amber-500/30 bg-gradient-to-b from-amber-950/20 to-slate-900/80 p-6 shadow-xl backdrop-blur-sm">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between border-b border-amber-500/20 pb-4">
            <div className="flex items-center gap-2.5">
              <div className="flex size-8 items-center justify-center rounded-lg bg-amber-500/20 text-amber-400">
                <Network className="size-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-amber-400">
                    Primary Causal Intelligence
                  </span>
                  <span className="rounded bg-amber-500/20 px-2 py-0.5 text-[10px] font-mono font-semibold text-amber-300">
                    Confidence: {(primary_causal_chain.confidence * 100).toFixed(0)}%
                  </span>
                </div>
                <h2 className="text-lg font-semibold text-white mt-0.5">{primary_causal_chain.title}</h2>
              </div>
            </div>
            <Link
              to="/graph-explorer"
              className="inline-flex items-center gap-1.5 rounded-lg bg-amber-500/10 border border-amber-500/30 px-3 py-1.5 text-xs font-medium text-amber-300 hover:bg-amber-500/20 transition"
            >
              <span>Explore Causal Topology</span>
              <ArrowRight className="size-3.5" />
            </Link>
          </div>

          <p className="mt-4 text-xs sm:text-sm text-slate-300 leading-relaxed bg-slate-950/60 p-3.5 rounded-xl border border-slate-800">
            {primary_causal_chain.explanation}
          </p>

          {/* Visual Step-by-Step Chain */}
          <div className="mt-6">
            <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-3">
              Deterministic Propagation Path:
            </p>
            <div className="grid grid-cols-1 gap-2 sm:grid-cols-5">
              {primary_causal_chain.nodes.map((node, index) => (
                <div key={node.id} className="relative flex flex-col justify-between rounded-xl border border-slate-800 bg-slate-900/90 p-3">
                  <div>
                    <span className="text-[10px] font-mono font-medium text-emerald-400 uppercase">
                      Step {index + 1}: {node.entity_type}
                    </span>
                    <p className="mt-1 text-xs font-semibold text-white leading-snug">{node.label}</p>
                  </div>
                  {node.details && (
                    <div className="mt-2 border-t border-slate-800 pt-1.5 text-[10px] text-slate-400">
                      {Object.entries(node.details).map(([k, v]) => (
                        <div key={k} className="flex justify-between">
                          <span className="capitalize">{k.replace('_', ' ')}:</span>
                          <span className="text-slate-200 font-medium">{v}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Verified Evidence Footer */}
          <div className="mt-5 border-t border-amber-500/10 pt-3 flex flex-wrap items-center gap-4 text-xs text-slate-400">
            <span className="font-semibold text-slate-300">Verified Evidence:</span>
            {primary_causal_chain.evidence_items.map((ev, i) => (
              <div key={i} className="flex items-center gap-1.5 rounded-md bg-slate-900 px-2.5 py-1 text-[11px] border border-slate-800">
                <CheckCircle2 className="size-3 text-emerald-400" />
                <span>{ev.claim}</span>
                <span className="text-slate-500 font-mono">({ev.source_type})</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Multidimensional Health & EVM Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Governance Dimensions */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 lg:col-span-2">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="font-semibold text-white text-sm">Governance & Health Dimensions</h3>
            <span className="text-xs text-slate-400">Weighted Multi-Factor Model</span>
          </div>

          <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-3">
            {Object.entries(health_dimensions).map(([name, dim]) => (
              <div key={name} className="rounded-lg border border-slate-800/80 bg-slate-950/40 p-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs capitalize font-medium text-slate-300">{name}</span>
                  <span
                    className={`size-2 rounded-full ${
                      dim.status === 'nominal' || dim.status === 'excellent'
                        ? 'bg-emerald-400'
                        : dim.status === 'watch'
                          ? 'bg-amber-400'
                          : 'bg-rose-400'
                    }`}
                  />
                </div>
                <div className="mt-2 flex items-baseline gap-1">
                  <span className="text-xl font-bold text-white">{dim.score}</span>
                  <span className="text-xs text-slate-500">/ 100</span>
                </div>
                <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-slate-800">
                  <div
                    className={`h-full ${dim.score >= 80 ? 'bg-emerald-500' : dim.score >= 60 ? 'bg-amber-500' : 'bg-rose-500'}`}
                    style={{ width: `${dim.score}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Earned Value Management (EVM) */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="font-semibold text-white text-sm">Earned Value Metrics (EVM)</h3>
            <span className="text-xs text-slate-400 font-mono">SAR Base</span>
          </div>

          <div className="mt-4 space-y-3 text-xs">
            <div className="flex items-center justify-between rounded-lg bg-slate-950/60 p-2.5 border border-slate-800/80">
              <span className="text-slate-400">Schedule Performance (SPI)</span>
              <span className="font-bold font-mono text-amber-400">{earned_value.spi.toFixed(2)} (Lagging)</span>
            </div>
            <div className="flex items-center justify-between rounded-lg bg-slate-950/60 p-2.5 border border-slate-800/80">
              <span className="text-slate-400">Cost Performance (CPI)</span>
              <span className="font-bold font-mono text-emerald-400">{earned_value.cpi.toFixed(2)} (Optimal)</span>
            </div>
            <div className="flex items-center justify-between rounded-lg bg-slate-950/60 p-2.5 border border-slate-800/80">
              <span className="text-slate-400">Earned Value (EV)</span>
              <span className="font-bold font-mono text-white">SAR {(earned_value.ev_sar / 1000000).toFixed(2)}M</span>
            </div>
            <div className="flex items-center justify-between rounded-lg bg-slate-950/60 p-2.5 border border-slate-800/80">
              <span className="text-slate-400">Actual Cost (AC)</span>
              <span className="font-bold font-mono text-white">SAR {(earned_value.ac_sar / 1000000).toFixed(2)}M</span>
            </div>
          </div>
        </div>
      </div>

      {/* Supplier Centrality & Portfolio Projects */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Supplier Single Point of Failure Bottlenecks */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <Truck className="size-4 text-emerald-400" />
              <h3 className="font-semibold text-white text-sm">Critical Supplier Bottlenecks (SPOF)</h3>
            </div>
            <Link to="/supply-chain" className="text-xs text-emerald-400 hover:underline">
              View All
            </Link>
          </div>

          <div className="mt-4 space-y-3">
            {supplier_bottlenecks.map((s) => (
              <div key={s.supplier_id} className="rounded-lg border border-slate-800 bg-slate-950/60 p-3.5">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-white text-xs">{s.supplier_name}</span>
                    <span className="ml-2 font-mono text-[10px] text-slate-400">[{s.supplier_code}]</span>
                  </div>
                  <span className="rounded bg-rose-500/20 px-2 py-0.5 text-[10px] font-semibold text-rose-300">
                    {s.concentration_risk}
                  </span>
                </div>
                <div className="mt-2 grid grid-cols-2 gap-2 text-[11px] text-slate-400">
                  <div>Betweenness: <span className="text-white font-mono">{s.betweenness_centrality}</span></div>
                  <div>Reliability: <span className="text-amber-400 font-mono">{s.lead_time_reliability_pct}%</span></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Portfolio Projects Table */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <Layers className="size-4 text-emerald-400" />
              <h3 className="font-semibold text-white text-sm">Projects Under Governance</h3>
            </div>
            <Link to="/project-360" className="text-xs text-emerald-400 hover:underline">
              Open 360 View
            </Link>
          </div>

          <div className="mt-4 space-y-3">
            {projects.map((p) => (
              <Link
                key={p.id}
                to={`/project-360?id=${p.id}`}
                className="group flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950/60 p-3.5 transition hover:border-slate-700 hover:bg-slate-900"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-white text-xs group-hover:text-emerald-400 transition">
                      {p.name}
                    </span>
                    <span className="font-mono text-[10px] text-slate-500">[{p.code}]</span>
                  </div>
                  <span className="text-[11px] text-slate-400 mt-1 block">
                    Status: <span className="capitalize text-slate-300">{p.status}</span>
                  </span>
                </div>

                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <span className="text-xs font-bold text-emerald-400">{p.health_score} / 100</span>
                    <span className="block text-[10px] text-slate-500">Health Index</span>
                  </div>
                  <ChevronRight className="size-4 text-slate-500 group-hover:text-white transition" />
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
