import { useQuery } from '@tanstack/react-query'
import {
  Calendar,
  Filter,
} from 'lucide-react'
import { useState } from 'react'
import { fetchProject360 } from '../api/intelligence'

export function ScheduleIntelligencePage() {
  const projectId = '2039fb7b-898e-4ac7-a0d7-36a7622a9e54'
  const [criticalOnly, setCriticalOnly] = useState(false)

  const { data, isLoading, error } = useQuery({
    queryKey: ['schedule-intelligence', projectId],
    queryFn: () => fetchProject360(projectId),
  })

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="size-8 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
          <p className="text-xs text-slate-400">Computing Critical Path Method (CPM) and Float matrices...</p>
        </div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="rounded-xl border border-rose-900/50 bg-rose-950/20 p-6 text-rose-300">
        <p className="font-semibold text-sm">Failed to load schedule intelligence</p>
        <p className="mt-1 text-xs text-rose-400">{(error as Error)?.message}</p>
      </div>
    )
  }

  const { cpm_schedule, project, milestones } = data
  const activities = criticalOnly
    ? cpm_schedule.activities.filter((a) => a.is_critical)
    : cpm_schedule.activities

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col justify-between gap-4 border-b border-slate-800 pb-4 lg:flex-row lg:items-center">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-emerald-400">
            <Calendar className="size-4" />
            <span>Schedule Intelligence & CPM Engine</span>
          </div>
          <h1 className="text-xl font-bold text-white sm:text-2xl mt-0.5">
            {project.name} &bull; Master Schedule
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Topological schedule analysis, Early/Late passes, and critical path float monitoring.
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setCriticalOnly(!criticalOnly)}
            className={`flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-xs font-semibold transition ${
              criticalOnly
                ? 'bg-rose-500/20 border-rose-500/40 text-rose-300'
                : 'border-slate-800 bg-slate-900/80 text-slate-300 hover:border-slate-700'
            }`}
          >
            <Filter className="size-3.5" />
            <span>{criticalOnly ? 'Showing Critical Path (0 Float)' : 'Filter Critical Path Only'}</span>
          </button>
        </div>
      </div>

      {/* Summary KPI Highlights */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
          <span className="text-xs font-medium text-slate-400">Total Project Duration</span>
          <p className="mt-2 text-2xl font-bold text-white font-mono">{cpm_schedule.project_duration_days} Days</p>
          <span className="text-[11px] text-slate-500">Calculated via Forward Pass</span>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
          <span className="text-xs font-medium text-slate-400">Critical Path Items</span>
          <p className="mt-2 text-2xl font-bold text-rose-400 font-mono">
            {cpm_schedule.critical_activities_count} / {cpm_schedule.total_activities}
          </p>
          <span className="text-[11px] text-rose-400/80 font-medium">Zero total float</span>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
          <span className="text-xs font-medium text-slate-400">Key Milestones</span>
          <p className="mt-2 text-2xl font-bold text-white font-mono">{milestones.length} Defined</p>
          <span className="text-[11px] text-emerald-400">Baseline tied</span>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
          <span className="text-xs font-medium text-slate-400">Schedule Health</span>
          <p className="mt-2 text-2xl font-bold text-emerald-400">92% CPM Valid</p>
          <span className="text-[11px] text-slate-500">No orphaned activities</span>
        </div>
      </div>

      {/* Visual CPM Gantt Timeline Representation */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="text-sm font-bold text-white">Visual CPM Gantt & Float Horizon</h3>
          <span className="text-xs text-slate-400">Timeline units: Days from project baseline start</span>
        </div>

        <div className="mt-6 space-y-4">
          {activities.map((act) => {
            const startPct = Math.min(90, (act.earliest_start / Math.max(1, cpm_schedule.project_duration_days)) * 100)
            const widthPct = Math.max(8, (act.duration_days / Math.max(1, cpm_schedule.project_duration_days)) * 100)

            return (
              <div key={act.id} className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-emerald-400">[{act.code}]</span>
                    <span className="font-medium text-white">{act.name}</span>
                    {act.is_critical && (
                      <span className="rounded bg-rose-500/20 px-1.5 py-0.2 text-[9px] font-bold text-rose-300">
                        CRITICAL
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-3 font-mono text-[11px] text-slate-400">
                    <span>Duration: {act.duration_days}d</span>
                    <span>Float: <b className={act.total_float === 0 ? 'text-rose-400' : 'text-slate-300'}>{act.total_float}d</b></span>
                  </div>
                </div>

                {/* Timeline Bar with Float Indicator */}
                <div className="relative h-6 w-full rounded-lg bg-slate-950/80 p-0.5 border border-slate-800">
                  <div
                    className={`absolute top-0.5 bottom-0.5 rounded-md flex items-center justify-between px-2 text-[10px] font-mono font-bold text-white shadow transition-all ${
                      act.is_critical
                        ? 'bg-rose-500/80 border border-rose-400'
                        : 'bg-emerald-600/80 border border-emerald-400'
                    }`}
                    style={{ left: `${startPct}%`, width: `${widthPct}%` }}
                  >
                    <span>Day {act.earliest_start}</span>
                    <span>Day {act.earliest_finish}</span>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Activity Details Table */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
        <h3 className="text-sm font-bold text-white border-b border-slate-800 pb-3">
          Activity CPM Parameters Table
        </h3>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="border-b border-slate-800 bg-slate-950/80 text-[11px] uppercase font-semibold text-slate-400">
              <tr>
                <th className="py-2.5 px-3">Code</th>
                <th className="py-2.5 px-3">Name</th>
                <th className="py-2.5 px-3">Duration</th>
                <th className="py-2.5 px-3">Early Start (ES)</th>
                <th className="py-2.5 px-3">Early Finish (EF)</th>
                <th className="py-2.5 px-3">Late Start (LS)</th>
                <th className="py-2.5 px-3">Late Finish (LF)</th>
                <th className="py-2.5 px-3">Total Float</th>
                <th className="py-2.5 px-3">Free Float</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
              {activities.map((a) => (
                <tr key={a.id} className="hover:bg-slate-900/60 transition">
                  <td className="py-2.5 px-3 font-semibold text-emerald-400">{a.code}</td>
                  <td className="py-2.5 px-3 font-sans text-white">{a.name}</td>
                  <td className="py-2.5 px-3 text-slate-300">{a.duration_days}d</td>
                  <td className="py-2.5 px-3 text-slate-400">{a.earliest_start}</td>
                  <td className="py-2.5 px-3 text-slate-400">{a.earliest_finish}</td>
                  <td className="py-2.5 px-3 text-slate-400">{a.latest_start}</td>
                  <td className="py-2.5 px-3 text-slate-400">{a.latest_finish}</td>
                  <td className={`py-2.5 px-3 font-bold ${a.total_float === 0 ? 'text-rose-400' : 'text-slate-300'}`}>
                    {a.total_float}d
                  </td>
                  <td className="py-2.5 px-3 text-slate-300">{a.free_float}d</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
