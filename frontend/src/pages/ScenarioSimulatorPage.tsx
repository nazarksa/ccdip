import { useMutation } from '@tanstack/react-query'
import {
  CheckCircle2,
  Play,
  Sparkles,
  Zap,
} from 'lucide-react'
import { useState } from 'react'
import { simulateScenario } from '../api/intelligence'
import type { ScenarioSimulationResult } from '../types'

export function ScenarioSimulatorPage() {
  const [disruptionType, setDisruptionType] = useState('supplier_outage')
  const [targetEntityName, setTargetEntityName] = useState('Supplier Z')
  const [simulatedDelayDays, setSimulatedDelayDays] = useState(15)
  const [result, setResult] = useState<ScenarioSimulationResult | null>(null)

  const mutation = useMutation({
    mutationFn: simulateScenario,
    onSuccess: (data) => {
      setResult(data)
    },
  })

  const handleSimulate = (e: React.FormEvent) => {
    e.preventDefault()
    mutation.mutate({
      disruption_type: disruptionType,
      target_entity_name: targetEntityName,
      simulated_delay_days: Number(simulatedDelayDays),
    })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-emerald-400">
          <Zap className="size-4" />
          <span>What-If Scenario Simulation Sandbox</span>
        </div>
        <h1 className="text-xl font-bold text-white sm:text-2xl mt-0.5">
          Predictive Impact & Delay Propagation Sandbox
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Simulate supply chain failures, supplier lead-time slippage, or scope adjustments without mutating production data.
        </p>
      </div>

      {/* Scenario Control Panel */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur">
        <form onSubmit={handleSimulate} className="grid grid-cols-1 gap-5 md:grid-cols-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Disruption Category
            </label>
            <select
              value={disruptionType}
              onChange={(e) => setDisruptionType(e.target.value)}
              className="w-full rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
            >
              <option value="supplier_outage">Supplier Lead Time Delay</option>
              <option value="material_shortage">Material Shortage / Stockout</option>
              <option value="activity_delay">Critical Activity Slippage</option>
              <option value="contract_dispute">Subcontractor Suspension</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Target Entity
            </label>
            <input
              type="text"
              value={targetEntityName}
              onChange={(e) => setTargetEntityName(e.target.value)}
              placeholder="e.g. Supplier Z"
              className="w-full rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-xs text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Simulated Delay (Days): <b className="text-emerald-400 font-mono">{simulatedDelayDays}d</b>
            </label>
            <input
              type="range"
              min="1"
              max="60"
              step="1"
              value={simulatedDelayDays}
              onChange={(e) => setSimulatedDelayDays(Number(e.target.value))}
              className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500 mt-2"
            />
          </div>

          <div className="flex items-end">
            <button
              type="submit"
              disabled={mutation.isPending}
              className="w-full flex items-center justify-center gap-2 rounded-lg bg-emerald-500 px-4 py-2.5 text-xs font-bold text-slate-950 transition hover:bg-emerald-400 disabled:opacity-50"
            >
              {mutation.isPending ? (
                <div className="size-4 animate-spin rounded-full border-2 border-slate-950 border-t-transparent" />
              ) : (
                <Play className="size-3.5 fill-current" />
              )}
              <span>Run Simulation</span>
            </button>
          </div>
        </form>
      </div>

      {/* Simulation Results Display */}
      {result && (
        <div className="space-y-6">
          {/* Variance Summary Banner */}
          <div className="rounded-2xl border border-amber-500/30 bg-gradient-to-r from-amber-950/20 via-slate-900 to-slate-900 p-6 shadow-xl">
            <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
              <div>
                <span className="font-mono text-[10px] font-bold uppercase text-amber-400">
                  Scenario Execution ID: {result.scenario_id}
                </span>
                <h3 className="text-lg font-bold text-white mt-0.5">
                  Simulation Outcome: {result.target_entity} (+{result.simulated_delay_days}d Disruption)
                </h3>
              </div>

              <div className="flex items-center gap-4">
                <div className="rounded-xl bg-slate-950/80 border border-slate-800 px-4 py-2 text-right">
                  <span className="text-[10px] uppercase text-slate-400 font-semibold">Projected Schedule Slip</span>
                  <p className="text-xl font-black text-rose-400 font-mono">{result.variance.duration_delta_days}</p>
                </div>
                <div className="rounded-xl bg-slate-950/80 border border-slate-800 px-4 py-2 text-right">
                  <span className="text-[10px] uppercase text-slate-400 font-semibold">Cost Impact Exposure</span>
                  <p className="text-xl font-black text-amber-400 font-mono">{result.variance.cost_delta_sar}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Baseline vs Scenario Diff Cards */}
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-2">
                Baseline (Unmodified State)
              </h4>
              <div className="mt-4 space-y-3 text-xs">
                <div className="flex justify-between bg-slate-950/60 p-2.5 rounded-lg border border-slate-800">
                  <span className="text-slate-400">Total Duration:</span>
                  <span className="font-mono font-bold text-white">{result.baseline.duration_days} Days</span>
                </div>
                <div className="flex justify-between bg-slate-950/60 p-2.5 rounded-lg border border-slate-800">
                  <span className="text-slate-400">Target Milestones On-Time:</span>
                  <span className="font-mono font-bold text-emerald-400">{result.baseline.milestones_on_time_pct}%</span>
                </div>
              </div>
            </div>

            <div className="rounded-xl border border-rose-500/20 bg-slate-900/50 p-5">
              <h4 className="text-xs font-bold uppercase tracking-wider text-rose-400 border-b border-slate-800 pb-2">
                Simulated Scenario Projection
              </h4>
              <div className="mt-4 space-y-3 text-xs">
                <div className="flex justify-between bg-slate-950/60 p-2.5 rounded-lg border border-slate-800">
                  <span className="text-slate-400">Simulated Duration:</span>
                  <span className="font-mono font-bold text-rose-400">{result.simulated.duration_days.toFixed(1)} Days</span>
                </div>
                <div className="flex justify-between bg-slate-950/60 p-2.5 rounded-lg border border-slate-800">
                  <span className="text-slate-400">Target Milestones On-Time:</span>
                  <span className="font-mono font-bold text-amber-400">{result.simulated.milestones_on_time_pct}%</span>
                </div>
              </div>
            </div>
          </div>

          {/* Activity Float Impact Table */}
          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
            <h4 className="text-sm font-semibold text-white border-b border-slate-800 pb-3">
              Activity Float Consumption & Criticality Shifts
            </h4>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="border-b border-slate-800 bg-slate-950/80 text-[11px] uppercase font-semibold text-slate-400">
                  <tr>
                    <th className="py-2.5 px-3">Activity</th>
                    <th className="py-2.5 px-3">Baseline Float</th>
                    <th className="py-2.5 px-3">Simulated Float</th>
                    <th className="py-2.5 px-3">Impact Outcome</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                  {result.affected_activities.map((item, i) => (
                    <tr key={i} className="hover:bg-slate-900/60">
                      <td className="py-2.5 px-3 font-sans text-white font-medium">{item.activity_name}</td>
                      <td className="py-2.5 px-3 text-slate-400">{item.baseline_float_days}d</td>
                      <td className={`py-2.5 px-3 font-bold ${item.simulated_float_days === 0 ? 'text-rose-400' : 'text-slate-300'}`}>
                        {item.simulated_float_days}d
                      </td>
                      <td className="py-2.5 px-3">
                        <span
                          className={`rounded px-2 py-0.5 text-[10px] font-bold ${
                            item.became_critical
                              ? 'bg-rose-500/20 text-rose-300'
                              : 'bg-amber-500/20 text-amber-300'
                          }`}
                        >
                          {item.impact_status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Recommended Interventions */}
          <div className="rounded-xl border border-emerald-500/20 bg-slate-900/50 p-5">
            <div className="flex items-center gap-2 text-emerald-400 font-semibold text-xs uppercase tracking-wider mb-3">
              <Sparkles className="size-4" />
              <span>Recommended Strategic Mitigations</span>
            </div>
            <ul className="space-y-2 text-xs text-slate-300">
              {result.recommended_mitigations.map((rec, i) => (
                <li key={i} className="flex items-start gap-2">
                  <CheckCircle2 className="size-3.5 text-emerald-400 mt-0.5 shrink-0" />
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}
