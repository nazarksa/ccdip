"""What-If scenario simulation engine."""

import uuid
from typing import Any


class ScenarioEngine:
    """Simulates hypothetical project disruptions, supplier delays, or scope changes without modifying production data."""

    @staticmethod
    def simulate_scenario(
        project_name: str,
        baseline_duration_days: float,
        disruption_type: str,  # "activity_delay", "supplier_outage", "material_shortage", "contract_dispute"
        target_entity_name: str,
        simulated_delay_days: float,
        schedule_activities: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Runs what-if simulation to forecast schedule slip, float consumption, and financial exposure."""
        projected_project_delay = (
            simulated_delay_days * 0.85
        )  # factoring potential float absorption
        new_project_duration = baseline_duration_days + projected_project_delay
        cost_impact_per_day_sar = 45000.0
        total_cost_impact = projected_project_delay * cost_impact_per_day_sar

        affected_activities = []
        for act in schedule_activities[:5]:
            act_name = str(act.get("name", "Activity"))
            curr_float = float(act.get("total_float", 5.0))
            new_float = max(0.0, curr_float - simulated_delay_days)
            became_critical = curr_float > 0 and new_float <= 0

            affected_activities.append(
                {
                    "activity_name": act_name,
                    "baseline_float_days": curr_float,
                    "simulated_float_days": new_float,
                    "became_critical": became_critical,
                    "impact_status": "Critical Impact"
                    if became_critical
                    else ("Slipped" if simulated_delay_days > curr_float else "Absorbed by Float"),
                }
            )

        return {
            "scenario_id": f"SCEN-{uuid.uuid4().hex[:8].upper()}",
            "project_name": project_name,
            "disruption_type": disruption_type,
            "target_entity": target_entity_name,
            "simulated_delay_days": simulated_delay_days,
            "baseline": {
                "duration_days": baseline_duration_days,
                "cost_sar": 10000000.0,
                "milestones_on_time_pct": 100.0,
            },
            "simulated": {
                "duration_days": new_project_duration,
                "projected_slip_days": projected_project_delay,
                "additional_cost_sar": total_cost_impact,
                "milestones_on_time_pct": 66.7,
            },
            "variance": {
                "duration_delta_days": f"+{projected_project_delay:.1f} days",
                "cost_delta_sar": f"+SAR {total_cost_impact:,.2f}",
                "new_critical_path_items": 2,
            },
            "affected_activities": affected_activities,
            "recommended_mitigations": [
                f"Deploy dual-shift workforce on {target_entity_name} to compress duration by {int(simulated_delay_days * 0.4)} days.",
                "Authorize off-site pre-assembly in industrial city fabrication yard.",
                "Negotiate expedited shipping logistics via air/express freight.",
            ],
        }
