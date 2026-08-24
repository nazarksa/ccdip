"""Critical Path Method (CPM) and schedule intelligence engine."""

import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any


@dataclass
class ActivityNode:
    id: uuid.UUID
    name: str
    code: str
    planned_start: datetime | None
    planned_finish: datetime | None
    actual_start: datetime | None
    actual_finish: datetime | None
    duration_days: float
    percent_complete: float
    is_milestone: bool = False
    earliest_start: float = 0.0
    earliest_finish: float = 0.0
    latest_start: float = 0.0
    latest_finish: float = 0.0
    total_float: float = 0.0
    free_float: float = 0.0
    is_critical: bool = False


class ScheduleEngine:
    """Deterministic schedule calculation engine implementing CPM and topological sorting."""

    @staticmethod
    def calculate_cpm(
        activities: list[dict[str, Any]],
        dependencies: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Calculates CPM metrics: ES, EF, LS, LF, Total Float, Free Float, and Critical Path."""
        if not activities:
            return {"activities": [], "critical_path": [], "project_duration_days": 0.0}

        node_map: dict[str, ActivityNode] = {}
        for act in activities:
            raw_id = str(act["id"])
            act_id_val = uuid.UUID(raw_id)
            start = act.get("planned_start")
            finish = act.get("planned_finish")

            duration = 5.0
            if start and finish:
                if isinstance(start, str):
                    start = datetime.fromisoformat(start.replace("Z", "+00:00"))
                if isinstance(finish, str):
                    finish = datetime.fromisoformat(finish.replace("Z", "+00:00"))
                delta = (finish - start).total_seconds() / 86400.0
                duration = max(1.0, round(delta, 1))

            pct = float(act.get("percent_complete") or 0.0)
            if isinstance(act.get("percent_complete"), Decimal):
                pct = float(act["percent_complete"])

            node_map[raw_id] = ActivityNode(
                id=act_id_val,
                name=str(act.get("name", "")),
                code=str(act.get("code", "")),
                planned_start=start,
                planned_finish=finish,
                actual_start=act.get("actual_start"),
                actual_finish=act.get("actual_finish"),
                duration_days=duration,
                percent_complete=pct,
            )

        preds: dict[str, list[tuple[str, float]]] = {k: [] for k in node_map}
        succs: dict[str, list[tuple[str, float]]] = {k: [] for k in node_map}
        in_degree: dict[str, int] = {k: 0 for k in node_map}

        for dep in dependencies:
            p_id = str(dep.get("predecessor_id"))
            s_id = str(dep.get("successor_id"))
            lag = float(dep.get("lag_days") or 0.0)
            if p_id in node_map and s_id in node_map:
                preds[s_id].append((p_id, lag))
                succs[p_id].append((s_id, lag))
                in_degree[s_id] += 1

        queue = [k for k, deg in in_degree.items() if deg == 0]
        topo_order: list[str] = []

        while queue:
            curr = queue.pop(0)
            topo_order.append(curr)
            for succ_key, _ in succs[curr]:
                in_degree[succ_key] -= 1
                if in_degree[succ_key] == 0:
                    queue.append(succ_key)

        if len(topo_order) < len(node_map):
            for k in node_map:
                if k not in topo_order:
                    topo_order.append(k)

        # Forward Pass
        for key in topo_order:
            node = node_map[key]
            max_es = 0.0
            for pred_id, lag in preds[key]:
                pred_node = node_map[pred_id]
                max_es = max(max_es, pred_node.earliest_finish + lag)
            node.earliest_start = max_es
            node.earliest_finish = max_es + node.duration_days

        project_duration = max((n.earliest_finish for n in node_map.values()), default=0.0)

        # Backward Pass
        for key in reversed(topo_order):
            node = node_map[key]
            if not succs[key]:
                node.latest_finish = project_duration
            else:
                min_lf = float("inf")
                for succ_id, lag in succs[key]:
                    succ_node = node_map[succ_id]
                    min_lf = min(min_lf, succ_node.latest_start - lag)
                node.latest_finish = min_lf if min_lf != float("inf") else project_duration

            node.latest_start = node.latest_finish - node.duration_days
            node.total_float = max(0.0, round(node.latest_start - node.earliest_start, 1))

            if not succs[key]:
                node.free_float = node.total_float
            else:
                min_succ_es = min(
                    (node_map[succ_id].earliest_start - lag for succ_id, lag in succs[key]),
                    default=node.earliest_finish,
                )
                node.free_float = max(0.0, round(min_succ_es - node.earliest_finish, 1))

            node.is_critical = node.total_float <= 0.001

        critical_path = [k for k in topo_order if node_map[k].is_critical]

        result_activities = [
            {
                "id": str(n.id),
                "code": n.code,
                "name": n.name,
                "duration_days": n.duration_days,
                "percent_complete": n.percent_complete,
                "earliest_start": n.earliest_start,
                "earliest_finish": n.earliest_finish,
                "latest_start": n.latest_start,
                "latest_finish": n.latest_finish,
                "total_float": n.total_float,
                "free_float": n.free_float,
                "is_critical": n.is_critical,
                "planned_start": n.planned_start.isoformat() if n.planned_start else None,
                "planned_finish": n.planned_finish.isoformat() if n.planned_finish else None,
            }
            for n in node_map.values()
        ]

        return {
            "activities": result_activities,
            "critical_path": critical_path,
            "project_duration_days": project_duration,
            "total_activities": len(result_activities),
            "critical_activities_count": len(critical_path),
        }
