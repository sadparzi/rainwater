# app/compute.py

# This module contains the computational logic for:
# - Calculating rainwater harvesting potential
# - Recommending recharge structures
# - Estimating costs and benefits
# - Suggesting structure dimensions

import math


def calculate_potential(user_input, rainfall_mm: float) -> float:
    """
    Calculates the total rooftop rainwater harvesting potential
    based on rainfall and site parameters.

    Args:
        user_input: InputData object containing roof area and open space.
        rainfall_mm: Annual rainfall in millimeters.

    Returns:
        float: Estimated runoff potential in liters.
    """
    # Typical runoff and infiltration coefficients
    runoff_coeff = 0.8          # ~80% of rainfall on roofs can be collected
    infiltration_factor = 0.3   # ~30% for open spaces

    # Contributions
    roof_contribution = rainfall_mm * user_input.roof_area * runoff_coeff
    open_space_contribution = rainfall_mm * user_input.open_space * infiltration_factor

    # Total potential runoff
    total_runoff = roof_contribution + open_space_contribution
    return round(total_runoff, 2)


def recommend_structure(user_input, potential: float) -> str:
    """
    Suggests an appropriate recharge structure
    based on runoff potential and available space.

    Args:
        user_input: InputData with open_space value.
        potential: Total potential runoff (liters).

    Returns:
        str: Recommended structure type.
    """
    if potential < 50000:
        return "Modular Tank (compact)" if user_input.open_space < 20 else "Recharge Pit (small)"
    elif 50000 <= potential <= 200000:
        return "Recharge Trench (medium)" if user_input.open_space >= 50 else "Recharge Pit (large, reinforced)"
    else:
        return "Recharge Shaft with Trench" if user_input.open_space >= 100 else "Deep Bore Recharge Shaft"


def cost_estimation(potential: float, structure: str) -> tuple[float, str]:
    """
    Estimates the cost of implementing a recharge structure
    and categorizes its benefit-to-cost ratio.

    Args:
        potential: Harvesting potential (liters).
        structure: Recommended structure type.

    Returns:
        tuple: (estimated total cost, benefit label)
    """
    base_costs = {
        "Recharge Pit (small)": 20000,
        "Recharge Pit (large, reinforced)": 40000,
        "Recharge Trench (medium)": 60000,
        "Recharge Shaft": 100000,
        "Deep Bore Recharge Shaft": 150000,
        "Recharge Shaft with Trench": 180000,
        "Modular Tank (compact)": 25000,
    }

    base_cost = base_costs.get(structure, 30000)

    # Scale cost depending on potential (every 50,000L adds ~10,000 INR)
    extra_cost = (int(potential) // 50000) * 10000
    total_cost = base_cost + extra_cost

    # Benefit-to-cost analysis
    benefit_ratio = round(potential / total_cost, 2) if total_cost > 0 else 0
    if benefit_ratio > 5:
        benefit_label = "High benefit"
    elif benefit_ratio > 2:
        benefit_label = "Moderate cost-benefit"
    else:
        benefit_label = "Low benefit"

    return round(total_cost, 2), benefit_label


def calculate_structure_dimensions(structure: str, potential: float) -> str:
    """
    Suggests approximate dimensions or number of structures
    required based on design norms.

    Args:
        structure: Recommended structure type.
        potential: Harvesting potential (liters).

    Returns:
        str: Human-readable design guideline.
    """
    if "Pit" in structure:
        pits_needed = math.ceil(potential / 2500) if potential > 0 else 0
        return f"1.2m × 1.2m × 2m each, {pits_needed} pits"
    elif "Trench" in structure:
        sections_needed = math.ceil(potential / 15000) if potential > 0 else 0
        return f"1m width × 1.5m depth × 10m length, {sections_needed} trench sections"
    elif "Shaft" in structure:
        shafts_needed = math.ceil(potential / 50000) if potential > 0 else 0
        return f"2m diameter × 10m depth, {shafts_needed} shafts"
    elif "Modular" in structure:
        volume_m3 = math.ceil(potential / 1000) if potential > 0 else 0
        return f"{volume_m3} m³ modular tank system"
    else:
        return "Standard design as per site conditions"
    