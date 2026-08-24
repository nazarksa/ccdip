import { createBrowserRouter } from 'react-router-dom'

import { AppShell } from '../layouts/AppShell'
import { EvidenceVaultPage } from '../pages/EvidenceVaultPage'
import { ExecutivePage } from '../pages/ExecutivePage'
import { FoundationPage } from '../pages/FoundationPage'
import { GraphExplorerPage } from '../pages/GraphExplorerPage'
import { Project360Page } from '../pages/Project360Page'
import { ScenarioSimulatorPage } from '../pages/ScenarioSimulatorPage'
import { ScheduleIntelligencePage } from '../pages/ScheduleIntelligencePage'
import { SupplyChainPage } from '../pages/SupplyChainPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppShell />,
    children: [
      { index: true, element: <ExecutivePage /> },
      { path: 'project-360', element: <Project360Page /> },
      { path: 'graph-explorer', element: <GraphExplorerPage /> },
      { path: 'schedule', element: <ScheduleIntelligencePage /> },
      { path: 'scenarios', element: <ScenarioSimulatorPage /> },
      { path: 'supply-chain', element: <SupplyChainPage /> },
      { path: 'evidence', element: <EvidenceVaultPage /> },
      { path: 'foundation', element: <FoundationPage /> },
    ],
  },
])
