import { useQuery } from '@tanstack/react-query'
import {
  Network,
  Search,
  ZoomIn,
  ZoomOut,
} from 'lucide-react'
import { useMemo, useState } from 'react'
import { fetchGraphTopology } from '../api/intelligence'

export function GraphExplorerPage() {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>('supplier-1')
  const [filterCategory, setFilterCategory] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState<string>('')
  const [zoomLevel, setZoomLevel] = useState<number>(1.0)

  const { data, isLoading, error } = useQuery({
    queryKey: ['graph-topology'],
    queryFn: fetchGraphTopology,
  })

  // Filter nodes & edges
  const filteredNodes = useMemo(() => {
    if (!data) return []
    return data.nodes.filter((node) => {
      const matchCat = filterCategory === 'all' || node.category === filterCategory || node.type.toLowerCase() === filterCategory.toLowerCase()
      const matchSearch = !searchQuery || node.label.toLowerCase().includes(searchQuery.toLowerCase()) || (node.code && node.code.toLowerCase().includes(searchQuery.toLowerCase()))
      return matchCat && matchSearch
    })
  }, [data, filterCategory, searchQuery])

  const filteredNodeIds = useMemo(() => new Set(filteredNodes.map((n) => n.id)), [filteredNodes])

  const filteredEdges = useMemo(() => {
    if (!data) return []
    return data.edges.filter((e) => filteredNodeIds.has(e.source) && filteredNodeIds.has(e.target))
  }, [data, filteredNodeIds])

  // Selected node details
  const selectedNode = useMemo(() => {
    if (!data || !selectedNodeId) return data?.nodes[0] ?? null
    return data.nodes.find((n) => n.id === selectedNodeId) ?? data.nodes[0]
  }, [data, selectedNodeId])

  // Upstream & Downstream relations for selected node
  const upstreamEdges = useMemo(() => {
    if (!data || !selectedNode) return []
    return data.edges.filter((e) => e.target === selectedNode.id)
  }, [data, selectedNode])

  const downstreamEdges = useMemo(() => {
    if (!data || !selectedNode) return []
    return data.edges.filter((e) => e.source === selectedNode.id)
  }, [data, selectedNode])

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="size-8 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
          <p className="text-xs text-slate-400">Loading graph topology and causal links...</p>
        </div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="rounded-xl border border-rose-900/50 bg-rose-950/20 p-6 text-rose-300">
        <p className="font-semibold text-sm">Failed to load graph topology</p>
        <p className="mt-1 text-xs text-rose-400">{(error as Error)?.message}</p>
      </div>
    )
  }

  // Node color mapper
  const getNodeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'project':
        return 'border-emerald-500 bg-emerald-950/60 text-emerald-300'
      case 'supplier':
        return 'border-amber-500 bg-amber-950/60 text-amber-300'
      case 'material':
        return 'border-cyan-500 bg-cyan-950/60 text-cyan-300'
      case 'activity':
        return 'border-blue-500 bg-blue-950/60 text-blue-300'
      case 'milestone':
        return 'border-purple-500 bg-purple-950/60 text-purple-300'
      case 'delay':
      case 'risk':
        return 'border-rose-500 bg-rose-950/60 text-rose-300'
      case 'contract':
      case 'invoice':
        return 'border-emerald-400 bg-emerald-950/40 text-emerald-200'
      default:
        return 'border-slate-700 bg-slate-900 text-slate-300'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header & Controls Bar */}
      <div className="flex flex-col justify-between gap-4 border-b border-slate-800 pb-4 lg:flex-row lg:items-center">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-emerald-400">
            <Network className="size-4" />
            <span>Interactive Graph & Causal Explorer</span>
          </div>
          <h1 className="text-xl font-bold text-white sm:text-2xl mt-0.5">Enterprise Dependency Topology</h1>
        </div>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 size-3.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search nodes or codes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="rounded-lg border border-slate-800 bg-slate-900/80 pl-8 pr-3 py-1.5 text-xs text-white placeholder:text-slate-500 focus:border-emerald-500 focus:outline-none"
            />
          </div>

          <div className="flex items-center gap-1 rounded-lg border border-slate-800 bg-slate-900/80 p-1 text-xs">
            {['all', 'schedule', 'supply_chain', 'controls', 'commercial'].map((cat) => (
              <button
                key={cat}
                onClick={() => setFilterCategory(cat)}
                className={`rounded px-2.5 py-1 text-[11px] font-medium capitalize transition ${
                  filterCategory === cat
                    ? 'bg-emerald-500/20 text-emerald-300 font-semibold'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {cat.replace('_', ' ')}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-1 rounded-lg border border-slate-800 bg-slate-900/80 p-1 text-xs">
            <button
              onClick={() => setZoomLevel((z) => Math.max(0.6, z - 0.1))}
              className="p-1 text-slate-400 hover:text-white"
              title="Zoom out"
            >
              <ZoomOut className="size-3.5" />
            </button>
            <span className="px-1 text-[10px] font-mono text-slate-300">{(zoomLevel * 100).toFixed(0)}%</span>
            <button
              onClick={() => setZoomLevel((z) => Math.min(1.6, z + 0.1))}
              className="p-1 text-slate-400 hover:text-white"
              title="Zoom in"
            >
              <ZoomIn className="size-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Canvas & Detail Sidebar Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Visual Graph Layout Grid / Canvas */}
        <div className="relative min-h-[500px] rounded-2xl border border-slate-800 bg-slate-950 p-6 overflow-hidden lg:col-span-2 shadow-inner">
          <div className="absolute top-4 left-4 z-10 flex items-center gap-2 rounded-full bg-slate-900/80 border border-slate-800 px-3 py-1 text-[11px] text-slate-400 backdrop-blur">
            <span>{filteredNodes.length} Entities</span>
            <span>&bull;</span>
            <span>{filteredEdges.length} Directed Relationships</span>
          </div>

          {/* Interactive Node Cards Matrix */}
          <div
            className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-12 transition-transform duration-200"
            style={{ transform: `scale(${zoomLevel})`, transformOrigin: 'top left' }}
          >
            {filteredNodes.map((node) => {
              const isSelected = selectedNode?.id === node.id
              const colorClass = getNodeColor(node.type)

              return (
                <div
                  key={node.id}
                  onClick={() => setSelectedNodeId(node.id)}
                  className={`cursor-pointer rounded-xl border p-4 transition shadow-md ${colorClass} ${
                    isSelected ? 'ring-2 ring-emerald-400 scale-[1.02]' : 'hover:border-slate-600'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono font-bold uppercase tracking-wider opacity-80">
                      {node.type}
                    </span>
                    {node.code && <span className="font-mono text-[10px] opacity-70">[{node.code}]</span>}
                  </div>
                  <h4 className="mt-1 text-xs font-bold leading-snug">{node.label}</h4>
                  {node.value_sar && (
                    <span className="mt-2 block font-mono text-[11px] font-semibold opacity-90">
                      SAR {node.value_sar.toLocaleString()}
                    </span>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {/* Selected Entity & Causal Inspector */}
        <div className="space-y-6">
          {selectedNode ? (
            <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div>
                  <span className="text-[10px] font-mono uppercase font-bold text-emerald-400">
                    Selected Entity
                  </span>
                  <h3 className="text-sm font-bold text-white mt-0.5">{selectedNode.label}</h3>
                </div>
                <span className="rounded bg-slate-800 px-2 py-0.5 font-mono text-[10px] text-slate-300">
                  {selectedNode.type}
                </span>
              </div>

              {/* Upstream Root Causes */}
              <div className="mt-4 space-y-2">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block">
                  Upstream Predecessors / Causes ({upstreamEdges.length})
                </span>
                {upstreamEdges.length === 0 ? (
                  <p className="text-[11px] text-slate-500 italic">Root entity (No upstream dependencies)</p>
                ) : (
                  upstreamEdges.map((e) => (
                    <div
                      key={e.id}
                      onClick={() => setSelectedNodeId(e.source)}
                      className="cursor-pointer flex items-center justify-between rounded-lg bg-slate-950/80 p-2.5 border border-slate-800 hover:border-slate-700 transition text-xs"
                    >
                      <div>
                        <span className="text-[10px] font-mono text-emerald-400 block">{e.label}</span>
                        <span className="font-medium text-white">{e.source.replace(/^[a-z]+-/, '')}</span>
                      </div>
                      <span className="text-[10px] font-mono text-slate-400">{(e.confidence * 100).toFixed(0)}% Conf.</span>
                    </div>
                  ))
                )}
              </div>

              {/* Downstream Propagations */}
              <div className="mt-5 space-y-2 border-t border-slate-800 pt-4">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block">
                  Downstream Successors / Impacts ({downstreamEdges.length})
                </span>
                {downstreamEdges.length === 0 ? (
                  <p className="text-[11px] text-slate-500 italic">Terminal entity (End of branch)</p>
                ) : (
                  downstreamEdges.map((e) => (
                    <div
                      key={e.id}
                      onClick={() => setSelectedNodeId(e.target)}
                      className="cursor-pointer flex items-center justify-between rounded-lg bg-slate-950/80 p-2.5 border border-slate-800 hover:border-slate-700 transition text-xs"
                    >
                      <div>
                        <span className="text-[10px] font-mono text-amber-400 block">{e.label}</span>
                        <span className="font-medium text-white">{e.target.replace(/^[a-z]+-/, '')}</span>
                      </div>
                      <span className="text-[10px] font-mono text-slate-400">{(e.confidence * 100).toFixed(0)}% Conf.</span>
                    </div>
                  ))
                )}
              </div>
            </div>
          ) : (
            <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-6 text-center text-xs text-slate-400">
              Select any graph node to inspect causal evidence and upstream/downstream paths.
            </div>
          )}

          {/* Graph Legend */}
          <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4 text-xs">
            <span className="font-semibold text-slate-300 block mb-2">Ontology Legend</span>
            <div className="grid grid-cols-2 gap-2 text-[11px]">
              <div className="flex items-center gap-1.5"><span className="size-2.5 rounded bg-emerald-500" /> Project / Contract</div>
              <div className="flex items-center gap-1.5"><span className="size-2.5 rounded bg-amber-500" /> Supplier</div>
              <div className="flex items-center gap-1.5"><span className="size-2.5 rounded bg-cyan-500" /> Material</div>
              <div className="flex items-center gap-1.5"><span className="size-2.5 rounded bg-blue-500" /> Activity / Milestone</div>
              <div className="flex items-center gap-1.5"><span className="size-2.5 rounded bg-rose-500" /> Risk / Delay Event</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
