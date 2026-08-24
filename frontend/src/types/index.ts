export interface PortfolioSummary {
  total_projects: number
  active_contracts_count: number
  total_contract_value_sar: number
  portfolio_health_score: number
  portfolio_status: string
  critical_risks_count: number
  active_delays_count: number
  monitored_suppliers_count: number
}

export interface HealthDimension {
  score: number
  weight: number
  status: 'nominal' | 'watch' | 'degraded' | 'excellent'
}

export interface EarnedValue {
  pv_sar: number
  ev_sar: number
  ac_sar: number
  cpi: number
  spi: number
  cv_sar: number
  sv_sar: number
}

export interface CausalNode {
  id: string
  label: string
  entity_type: string
  status: string
  details?: Record<string, string>
}

export interface CausalEdge {
  source: string
  target: string
  relationship: string
  confidence: number
  evidence?: string
}

export interface EvidenceItem {
  claim: string
  source_type: string
  source_id?: string
  verified: boolean
  confidence: number
}

export interface CausalChain {
  chain_id: string
  title: string
  root_cause: string
  target_impact: string
  confidence: number
  causal_type: string
  explanation: string
  nodes: CausalNode[]
  edges: CausalEdge[]
  evidence_items: EvidenceItem[]
  affected_milestones: string[]
  time_horizon_days: number
  generated_at: string
}

export interface SupplierBottleneck {
  supplier_id: string
  supplier_name: string
  supplier_code: string
  supplied_projects_count: number
  supplied_materials: string[]
  betweenness_centrality: number
  concentration_risk: string
  lead_time_reliability_pct: number
  alternative_suppliers: Array<{ name: string; readiness: string; lead_time_days: number }>
}

export interface ProjectCard {
  id: string
  name: string
  code: string
  description?: string
  status: string
  start_date?: string
  end_date?: string
  health_score: number
  schedule_variance_days: number
}

export interface OverviewData {
  portfolio_summary: PortfolioSummary
  health_dimensions: Record<string, HealthDimension>
  earned_value: EarnedValue
  primary_causal_chain: CausalChain | null
  causal_chains_count: number
  supplier_bottlenecks: SupplierBottleneck[]
  projects: ProjectCard[]
}

export interface ActivityCPM {
  id: string
  code: string
  name: string
  duration_days: number
  percent_complete: number
  earliest_start: number
  earliest_finish: number
  latest_start: number
  latest_finish: number
  total_float: number
  free_float: number
  is_critical: boolean
  planned_start?: string
  planned_finish?: string
}

export interface CPMSchedule {
  activities: ActivityCPM[]
  critical_path: string[]
  project_duration_days: number
  total_activities: number
  critical_activities_count: number
}

export interface Project360Bundle {
  project: ProjectCard
  health: {
    overall_score: number
    status: string
    dimensions: Record<string, HealthDimension>
    earned_value: EarnedValue
  }
  cpm_schedule: CPMSchedule
  causal_chains: CausalChain[]
  contracts: Array<{
    id: string
    number: string
    title: string
    contract_type: string
    value_sar: number
    currency: string
    status: string
  }>
  financials: {
    total_invoices_sar: number
    total_payments_sar: number
    invoices: Array<{ id: string; number: string; amount_sar: number; date: string; status: string }>
    payments: Array<{ id: string; reference: string; amount_sar: number; date: string; status: string }>
    subcontracts: Array<{ id: string; number: string; title: string; value_sar: number }>
  }
  risks: Array<{
    id: string
    code: string
    title: string
    probability: number
    impact_sar: number
    status: string
  }>
  delays: Array<{
    id: string
    code: string
    title: string
    delay_days: number
    start_date?: string
    status: string
  }>
  milestones: Array<{
    id: string
    code: string
    name: string
    due_at?: string
    status: string
  }>
  engineering_and_quality: {
    rfis: Array<{ id: string; number: string; subject: string; status: string }>
    submittals: Array<{ id: string; number: string; title: string; status: string }>
  }
  documents: Array<{
    id: string
    number: string
    title: string
    document_type: string
    status: string
  }>
}

export interface GraphNode {
  id: string
  raw_id: string
  label: string
  type: string
  code?: string
  status?: string
  value_sar?: number
  category: string
}

export interface GraphEdge {
  id: string
  source: string
  target: string
  label: string
  confidence: number
  is_causal: boolean
}

export interface GraphTopology {
  nodes: GraphNode[]
  edges: GraphEdge[]
  statistics: {
    total_nodes: number
    total_edges: number
    causal_edges_count: number
  }
}

export interface ScenarioSimulationResult {
  scenario_id: string
  project_name: string
  disruption_type: string
  target_entity: string
  simulated_delay_days: number
  baseline: {
    duration_days: number
    cost_sar: number
    milestones_on_time_pct: number
  }
  simulated: {
    duration_days: number
    projected_slip_days: number
    additional_cost_sar: number
    milestones_on_time_pct: number
  }
  variance: {
    duration_delta_days: string
    cost_delta_sar: string
    new_critical_path_items: number
  }
  affected_activities: Array<{
    activity_name: string
    baseline_float_days: number
    simulated_float_days: number
    became_critical: boolean
    impact_status: string
  }>
  recommended_mitigations: string[]
}

export interface EvidenceVault {
  documents: Array<{
    id: string
    number: string
    title: string
    document_type: string
    status: string
  }>
  claims: Array<{
    id: string
    title: string
    description: string
    page_number: number
    confidence: number
    verified_by: string
    verification_status: string
    document_id: string
  }>
}
