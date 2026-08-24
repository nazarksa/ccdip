import { useQuery } from '@tanstack/react-query'
import {
  Calendar,
  Compass,
  CreditCard,
  FileCheck,
  FileText,
  HelpCircle,
  ShieldAlert,
} from 'lucide-react'
import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { fetchProject360 } from '../api/intelligence'

type TabType = 'overview' | 'schedule' | 'commercial' | 'risks' | 'engineering' | 'documents'

export function Project360Page() {
  const [searchParams] = useSearchParams()
  const projectId = searchParams.get('id') ?? '2039fb7b-898e-4ac7-a0d7-36a7622a9e54'
  const [activeTab, setActiveTab] = useState<TabType>('overview')

  const { data, isLoading, error } = useQuery({
    queryKey: ['project-360', projectId],
    queryFn: () => fetchProject360(projectId),
  })

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="size-8 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
          <p className="text-xs text-slate-400">Assembling Project 360 multi-source intelligence...</p>
        </div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="rounded-xl border border-rose-900/50 bg-rose-950/20 p-6 text-rose-300">
        <p className="font-semibold text-sm">Error loading project 360 data</p>
        <p className="mt-1 text-xs text-rose-400">{(error as Error)?.message}</p>
      </div>
    )
  }

  const { project, health, cpm_schedule, causal_chains, contracts, financials, risks, delays, engineering_and_quality, documents } = data

  return (
    <div className="space-y-6">
      {/* Project Banner */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 backdrop-blur-md">
        <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
          <div>
            <div className="flex items-center gap-2">
              <span className="rounded bg-emerald-500/20 px-2 py-0.5 font-mono text-[11px] font-bold text-emerald-400">
                {project.code}
              </span>
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Kingdom of Saudi Arabia Giga-Project
              </span>
            </div>
            <h1 className="mt-1.5 text-2xl font-bold text-white sm:text-3xl">{project.name}</h1>
            <p className="mt-1 text-xs text-slate-400">{project.description ?? 'Master project delivery package under active governance.'}</p>
          </div>

          <div className="flex items-center gap-3">
            <div className="rounded-xl border border-slate-800 bg-slate-950/80 px-4 py-2.5 text-right">
              <span className="text-[10px] uppercase font-semibold text-slate-400">Project Health</span>
              <div className="flex items-center justify-end gap-1.5 mt-0.5">
                <span className="text-2xl font-black text-emerald-400">{health.overall_score}</span>
                <span className="text-xs text-slate-500">/ 100</span>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mt-6 flex flex-wrap gap-1 border-t border-slate-800 pt-4">
          {[
            { id: 'overview', label: 'Overview & Health', icon: Compass },
            { id: 'schedule', label: 'CPM Schedule & Float', icon: Calendar, badge: `${cpm_schedule.activities.length}` },
            { id: 'commercial', label: 'Commercial & Finance', icon: CreditCard, badge: `${contracts.length}` },
            { id: 'risks', label: 'Risks & Delays', icon: ShieldAlert, badge: `${risks.length + delays.length}` },
            { id: 'engineering', label: 'Quality & RFIs', icon: HelpCircle, badge: `${engineering_and_quality.rfis.length}` },
            { id: 'documents', label: 'Documents & Evidence', icon: FileCheck, badge: `${documents.length}` },
          ].map((tab) => {
            const Icon = tab.icon
            const isActive = activeTab === tab.id
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as TabType)}
                className={`flex items-center gap-2 rounded-lg px-3.5 py-2 text-xs font-medium transition ${
                  isActive
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    : 'text-slate-400 hover:bg-slate-800/80 hover:text-slate-200'
                }`}
              >
                <Icon className="size-3.5" />
                <span>{tab.label}</span>
                {tab.badge && (
                  <span className="rounded bg-slate-800 px-1.5 py-0.2 text-[10px] font-mono text-slate-400">
                    {tab.badge}
                  </span>
                )}
              </button>
            )
          })}
        </div>
      </div>

      {/* Tab Content: OVERVIEW */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
            <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 lg:col-span-2">
              <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-3">
                Health Dimension Scoring
              </h3>
              <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-3">
                {Object.entries(health.dimensions).map(([name, dim]) => (
                  <div key={name} className="rounded-lg border border-slate-800/80 bg-slate-950/40 p-3">
                    <span className="text-xs capitalize font-medium text-slate-400">{name}</span>
                    <p className="mt-1 text-xl font-bold text-white">{dim.score} / 100</p>
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

            <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
              <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-3">
                Schedule Critical Metrics
              </h3>
              <div className="mt-4 space-y-3 text-xs">
                <div className="flex justify-between rounded-lg bg-slate-950/60 p-2.5 border border-slate-800">
                  <span className="text-slate-400">Project Duration</span>
                  <span className="font-bold text-white font-mono">{cpm_schedule.project_duration_days} Days</span>
                </div>
                <div className="flex justify-between rounded-lg bg-slate-950/60 p-2.5 border border-slate-800">
                  <span className="text-slate-400">Critical Path Items</span>
                  <span className="font-bold text-rose-400 font-mono">{cpm_schedule.critical_activities_count} Activities</span>
                </div>
                <div className="flex justify-between rounded-lg bg-slate-950/60 p-2.5 border border-slate-800">
                  <span className="text-slate-400">Active Delays</span>
                  <span className="font-bold text-amber-400 font-mono">{delays.length} Registered</span>
                </div>
              </div>
            </div>
          </div>

          {/* Active Causal Chains for this Project */}
          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
            <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-3">
              Identified Causal Paths
            </h3>
            <div className="mt-4 space-y-4">
              {causal_chains.map((chain) => (
                <div key={chain.chain_id} className="rounded-lg border border-amber-500/20 bg-slate-950/60 p-4">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-amber-300 text-xs">{chain.title}</span>
                    <span className="rounded bg-amber-500/20 px-2 py-0.5 text-[10px] font-mono text-amber-400">
                      Confidence: {(chain.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                  <p className="mt-2 text-xs text-slate-300 leading-relaxed">{chain.explanation}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab Content: SCHEDULE & CPM */}
      {activeTab === 'schedule' && (
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h3 className="text-sm font-semibold text-white">Critical Path Method (CPM) Activity Schedule</h3>
              <p className="text-xs text-slate-400 mt-0.5">Calculated Early/Late Start, Total Float, and Free Float</p>
            </div>
            <span className="rounded bg-rose-500/20 px-2.5 py-1 text-xs font-semibold text-rose-300">
              {cpm_schedule.critical_activities_count} Critical Activities
            </span>
          </div>

          <div className="mt-4 overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="border-b border-slate-800 bg-slate-950/80 text-[11px] uppercase font-semibold text-slate-400">
                <tr>
                  <th className="py-3 px-3">Code</th>
                  <th className="py-3 px-3">Activity Name</th>
                  <th className="py-3 px-3">Duration</th>
                  <th className="py-3 px-3">Progress</th>
                  <th className="py-3 px-3">ES / EF</th>
                  <th className="py-3 px-3">LS / LF</th>
                  <th className="py-3 px-3">Total Float</th>
                  <th className="py-3 px-3">Critical Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                {cpm_schedule.activities.map((act) => (
                  <tr key={act.id} className="hover:bg-slate-900/80 transition">
                    <td className="py-3 px-3 font-semibold text-emerald-400">{act.code}</td>
                    <td className="py-3 px-3 font-sans text-white">{act.name}</td>
                    <td className="py-3 px-3 text-slate-300">{act.duration_days}d</td>
                    <td className="py-3 px-3 text-slate-300">{act.percent_complete}%</td>
                    <td className="py-3 px-3 text-slate-400">
                      Day {act.earliest_start} &rarr; Day {act.earliest_finish}
                    </td>
                    <td className="py-3 px-3 text-slate-400">
                      Day {act.latest_start} &rarr; Day {act.latest_finish}
                    </td>
                    <td className="py-3 px-3">
                      <span className={act.total_float === 0 ? 'text-rose-400 font-bold' : 'text-slate-300'}>
                        {act.total_float} days
                      </span>
                    </td>
                    <td className="py-3 px-3">
                      {act.is_critical ? (
                        <span className="rounded bg-rose-500/20 px-2 py-0.5 text-[10px] font-bold text-rose-300">
                          CRITICAL PATH
                        </span>
                      ) : (
                        <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] text-slate-400">
                          Float Available
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab Content: COMMERCIAL & FINANCE */}
      {activeTab === 'commercial' && (
        <div className="space-y-6">
          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
            <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-3">Contracts & Subcontracts</h3>
            <div className="mt-4 space-y-3">
              {contracts.map((c) => (
                <div key={c.id} className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950/60 p-3.5">
                  <div>
                    <span className="font-mono text-xs font-bold text-emerald-400">{c.number}</span>
                    <h4 className="text-xs font-semibold text-white mt-0.5">{c.title}</h4>
                    <span className="text-[11px] text-slate-400 capitalize">Type: {c.contract_type}</span>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-bold font-mono text-white">
                      SAR {c.value_sar.toLocaleString()}
                    </span>
                    <span className="block text-[10px] text-emerald-400 font-medium capitalize">{c.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
              <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-3">Invoices</h3>
              <div className="mt-4 space-y-2 text-xs">
                {financials.invoices.map((inv) => (
                  <div key={inv.id} className="flex justify-between items-center bg-slate-950/60 p-2.5 rounded-lg border border-slate-800">
                    <div>
                      <span className="font-mono font-semibold text-slate-200">{inv.number}</span>
                      <span className="block text-[10px] text-slate-500">{inv.date}</span>
                    </div>
                    <span className="font-mono font-bold text-emerald-400">SAR {inv.amount_sar.toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
              <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-3">Payments Settled</h3>
              <div className="mt-4 space-y-2 text-xs">
                {financials.payments.map((p) => (
                  <div key={p.id} className="flex justify-between items-center bg-slate-950/60 p-2.5 rounded-lg border border-slate-800">
                    <div>
                      <span className="font-mono font-semibold text-slate-200">{p.reference}</span>
                      <span className="block text-[10px] text-slate-500">{p.date}</span>
                    </div>
                    <span className="font-mono font-bold text-emerald-400">SAR {p.amount_sar.toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab Content: RISKS & DELAYS */}
      {activeTab === 'risks' && (
        <div className="space-y-6">
          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
            <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-3">Registered Risks</h3>
            <div className="mt-4 space-y-3">
              {risks.map((r) => (
                <div key={r.id} className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950/60 p-3.5">
                  <div>
                    <span className="font-mono text-xs font-bold text-rose-400">{r.code}</span>
                    <h4 className="text-xs font-semibold text-white mt-0.5">{r.title}</h4>
                  </div>
                  <div className="text-right text-xs">
                    <span className="text-slate-400">Probability: <b className="text-white">{r.probability}%</b></span>
                    <span className="block font-mono text-amber-400 font-semibold">Impact: SAR {r.impact_sar.toLocaleString()}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
            <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-3">Active Delay Events</h3>
            <div className="mt-4 space-y-3">
              {delays.map((d) => (
                <div key={d.id} className="flex items-center justify-between rounded-lg border border-amber-500/20 bg-slate-950/60 p-3.5">
                  <div>
                    <span className="font-mono text-xs font-bold text-amber-400">{d.code}</span>
                    <h4 className="text-xs font-semibold text-white mt-0.5">{d.title}</h4>
                  </div>
                  <span className="font-mono text-xs font-bold text-rose-400">+{d.delay_days} Days Slip</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab Content: QUALITY & RFIs */}
      {activeTab === 'engineering' && (
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-3">RFIs & Technical Submittals</h3>
          <div className="mt-4 space-y-3">
            {engineering_and_quality.rfis.map((rfi) => (
              <div key={rfi.id} className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950/60 p-3.5">
                <div>
                  <span className="font-mono text-xs font-bold text-emerald-400">{rfi.number}</span>
                  <p className="text-xs font-semibold text-white mt-0.5">{rfi.subject}</p>
                </div>
                <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] capitalize text-slate-300">{rfi.status}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab Content: DOCUMENTS & EVIDENCE */}
      {activeTab === 'documents' && (
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-3">Project Documents & Source Evidence</h3>
          <div className="mt-4 space-y-3">
            {documents.map((doc) => (
              <div key={doc.id} className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950/60 p-3.5">
                <div className="flex items-center gap-3">
                  <FileText className="size-4 text-emerald-400" />
                  <div>
                    <span className="font-mono text-[11px] text-slate-500">{doc.number}</span>
                    <h4 className="text-xs font-semibold text-white">{doc.title}</h4>
                  </div>
                </div>
                <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] capitalize text-slate-300">{doc.document_type}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
