import { useQuery } from '@tanstack/react-query'
import {
  CheckCircle2,
  FileCheck,
  FileText,
  Search,
} from 'lucide-react'
import { useState } from 'react'
import { fetchEvidenceVault } from '../api/intelligence'

export function EvidenceVaultPage() {
  const [searchTerm, setSearchTerm] = useState('')

  const { data, isLoading, error } = useQuery({
    queryKey: ['evidence-vault'],
    queryFn: fetchEvidenceVault,
  })

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="size-8 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
          <p className="text-xs text-slate-400">Retrieving verified evidence claims and audit citations...</p>
        </div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="rounded-xl border border-rose-900/50 bg-rose-950/20 p-6 text-rose-300">
        <p className="font-semibold text-sm">Failed to load evidence vault</p>
        <p className="mt-1 text-xs text-rose-400">{(error as Error)?.message}</p>
      </div>
    )
  }

  const { documents, claims } = data
  const filteredClaims = claims.filter(
    (c) =>
      !searchTerm ||
      c.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.description.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col justify-between gap-4 border-b border-slate-800 pb-4 sm:flex-row sm:items-center">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-emerald-400">
            <FileCheck className="size-4" />
            <span>Audit & Evidence Citation Vault</span>
          </div>
          <h1 className="text-xl font-bold text-white sm:text-2xl mt-0.5">
            Verified Claims & Document Provenance
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Every causal claim and risk propagation is backed by an audited document citation.
          </p>
        </div>

        <div className="relative">
          <Search className="absolute left-2.5 top-2.5 size-3.5 text-slate-400" />
          <input
            type="text"
            placeholder="Search claims or citations..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="rounded-lg border border-slate-800 bg-slate-900/80 pl-8 pr-3 py-1.5 text-xs text-white placeholder:text-slate-500 focus:border-emerald-500 focus:outline-none"
          />
        </div>
      </div>

      {/* Claims List Grid */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-white">Verified Causal Claims ({filteredClaims.length})</h3>
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {filteredClaims.map((claim) => (
            <div
              key={claim.id}
              className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur shadow-md flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="rounded bg-emerald-500/20 px-2 py-0.5 font-mono text-[10px] font-bold text-emerald-400">
                    Page {claim.page_number} Citation
                  </span>
                  <span className="flex items-center gap-1 text-[11px] text-emerald-400 font-semibold">
                    <CheckCircle2 className="size-3.5" />
                    <span>{claim.verification_status}</span>
                  </span>
                </div>
                <h4 className="mt-2 text-sm font-bold text-white">{claim.title}</h4>
                <p className="mt-1.5 text-xs text-slate-300 leading-relaxed bg-slate-950/60 p-3 rounded-lg border border-slate-800/80">
                  &ldquo;{claim.description}&rdquo;
                </p>
              </div>

              <div className="mt-4 border-t border-slate-800/80 pt-3 flex items-center justify-between text-[11px] text-slate-400">
                <span>Verified by: <b className="text-slate-200">{claim.verified_by}</b></span>
                <span className="font-mono text-emerald-400">{(claim.confidence * 100).toFixed(0)}% Confidence</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Governed Source Documents */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
        <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-3">
          Governed Source Documents Repository
        </h3>
        <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className="flex items-center justify-between rounded-lg bg-slate-950/60 p-3.5 border border-slate-800"
            >
              <div className="flex items-center gap-3">
                <FileText className="size-4 text-emerald-400" />
                <div>
                  <span className="font-mono text-[10px] text-slate-500">[{doc.number}]</span>
                  <p className="text-xs font-semibold text-white">{doc.title}</p>
                </div>
              </div>
              <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] capitalize text-slate-300 font-medium">
                {doc.document_type}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
