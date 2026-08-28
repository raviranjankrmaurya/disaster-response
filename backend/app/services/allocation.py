"""
Logistics / Allocation engine — route/road-accessibility aware.

Maximizes severity-weighted, route-practicality-weighted coverage of
zone demand, subject to depot stock and zone demand constraints.
Uses OR-Tools CP-SAT.
"""

from ortools.sat.python import cp_model

SEVERITY_WEIGHT = {"critical": 4, "high": 3, "moderate": 2, "low": 1}
MAX_DISTANCE_KM_FOR_FULL_WEIGHT = 50
DISTANCE_PENALTY_PER_100KM = 1


def _route_weight_multiplier(depot, route):
    if depot.get("road_accessible") is False:
        return 1
    if route is None or route.get("distance_km") is None:
        return 10
    distance_km = route["distance_km"]
    if distance_km <= MAX_DISTANCE_KM_FOR_FULL_WEIGHT:
        return 10
    penalty = int((distance_km - MAX_DISTANCE_KM_FOR_FULL_WEIGHT) / 100) * DISTANCE_PENALTY_PER_100KM
    return max(10 - penalty, 2)


def allocate_resources(depots_stock, zones_demand, routes=None):
    if not depots_stock or not zones_demand:
        return []
    routes = routes or {}

    model = cp_model.CpModel()

    allocation_vars = {}
    for d in depots_stock:
        for z in zones_demand:
            allocation_vars[(d["depot_id"], z["zone_id"])] = model.NewIntVar(
                0, min(d["quantity_available"], z["demand"]) or 0,
                f"alloc_{d['depot_id']}_{z['zone_id']}"
            )

    for d in depots_stock:
        model.Add(
            sum(allocation_vars[(d["depot_id"], z["zone_id"])] for z in zones_demand)
            <= d["quantity_available"]
        )

    for z in zones_demand:
        model.Add(
            sum(allocation_vars[(d["depot_id"], z["zone_id"])] for d in depots_stock)
            <= z["demand"]
        )

    objective_terms = []
    for d in depots_stock:
        for z in zones_demand:
            severity_weight = SEVERITY_WEIGHT.get(z["severity"], 1)
            route = routes.get((d["depot_id"], z["zone_id"]))
            route_weight = _route_weight_multiplier(d, route)
            combined_weight = severity_weight * route_weight
            objective_terms.append(combined_weight * allocation_vars[(d["depot_id"], z["zone_id"])])
    model.Maximize(sum(objective_terms))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5.0
    status = solver.Solve(model)

    allocations = []
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for d in depots_stock:
            for z in zones_demand:
                qty = solver.Value(allocation_vars[(d["depot_id"], z["zone_id"])])
                if qty > 0:
                    route = routes.get((d["depot_id"], z["zone_id"]), {})
                    allocations.append({
                        "depot_id": d["depot_id"],
                        "depot_name": d["depot_name"],
                        "zone_id": z["zone_id"],
                        "zone_name": z["zone_name"],
                        "quantity_allocated": qty,
                        "distance_km": route.get("distance_km"),
                        "duration_min": route.get("duration_min"),
                        "route_source": route.get("source"),
                    })
    return allocations
