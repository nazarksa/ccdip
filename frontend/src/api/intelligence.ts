import { apiRequest } from './client'
import type {
  EvidenceVault,
  GraphTopology,
  OverviewData,
  Project360Bundle,
  ScenarioSimulationResult,
  SupplierBottleneck,
} from '../types'

export async function fetchPortfolioOverview(): Promise<OverviewData> {
  return apiRequest<OverviewData>('/api/v1/intelligence/overview')
}

export async function fetchProject360(projectId: string): Promise<Project360Bundle> {
  return apiRequest<Project360Bundle>(`/api/v1/intelligence/projects/${projectId}/360`)
}

export async function fetchGraphTopology(): Promise<GraphTopology> {
  return apiRequest<GraphTopology>('/api/v1/intelligence/graph/topology')
}

export async function simulateScenario(params: {
  disruption_type: string
  target_entity_name: string
  simulated_delay_days: number
}): Promise<ScenarioSimulationResult> {
  return apiRequest<ScenarioSimulationResult>('/api/v1/intelligence/scenarios/simulate', {
    method: 'POST',
    body: JSON.stringify(params),
  })
}

export async function fetchSupplierBottlenecks(): Promise<SupplierBottleneck[]> {
  return apiRequest<SupplierBottleneck[]>('/api/v1/intelligence/supply-chain/bottlenecks')
}

export async function fetchEvidenceVault(): Promise<EvidenceVault> {
  return apiRequest<EvidenceVault>('/api/v1/intelligence/evidence/vault')
}
