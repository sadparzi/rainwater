# app/services.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file (like API keys)
load_dotenv()

# Import necessary functions and models
# The try/except ensures that imports work both inside "app" package and standalone
try:
    from .compute import calculate_potential, recommend_structure, cost_estimation, calculate_structure_dimensions
    from .models import UserInput, AssessmentResult
except Exception:
    from compute import calculate_potential, recommend_structure, cost_estimation, calculate_structure_dimensions
    from models import UserInput, AssessmentResult

# Load API key for OpenWeather (used for fetching rainfall data)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_rainfall(lat=None, lon=None, location=None):
    """
    Fetch rainfall data from OpenWeather API if possible.
    Falls back to a default value (1000 mm/year) if data is missing/unavailable.

    Parameters:
        lat (float): Latitude of the location
        lon (float): Longitude of the location
        location (str): City/region name

    Returns:
        float: Estimated yearly rainfall in millimeters
    """
    try:
        # Build API URL depending on available parameters
        if lat and lon and OPENWEATHER_API_KEY:
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        elif location and OPENWEATHER_API_KEY:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}"
        else:
            return 1000.0  # Default fallback rainfall (mm/year)

        # Make API request
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return 1000.0

        # Parse rainfall data
        data = response.json()
        rainfall_mm = 0
        if "rain" in data:
            # Some APIs provide rainfall in last 1h or 3h
            rainfall_mm = data["rain"].get("1h", data["rain"].get("3h", 0))

        # If no rainfall reported, fallback to default
        if rainfall_mm == 0:
            return 1000.0

        # Convert hourly rainfall to annual estimate (mm)
        return round(rainfall_mm * 24 * 365, 2)

    except Exception:
        # If any error, fallback to default
        return 1000.0


def assess_rtrwh(data):
    """
    Main service function to assess Rooftop Rainwater Harvesting (RTRWH) feasibility.

    Parameters:
        data (dict): Input data from user (roof size, dwellers, location, etc.)

    Returns:
        dict: Assessment results including feasibility, cost, demand coverage, and structure recommendation.
    """

    # Wrap input data into UserInput model
    user_input = UserInput(
        name=data.get("name"),
        location=data.get("location"),
        latitude=float(data.get("latitude", 0)),
        longitude=float(data.get("longitude", 0)),
        dwellers=int(data.get("dwellers", 1)),
        roof_area=float(data.get("roof_area", 0)),
        open_space=float(data.get("open_space", 0)),
        gw_depth=float(data.get("gw_depth", 0))  # depth to groundwater (meters)
    )

    # Get rainfall input: either from user or API
    rainfall = data.get("rainfall_mm")
    if rainfall is None:
        rainfall = get_rainfall(lat=user_input.latitude, lon=user_input.longitude, location=user_input.location)
    try:
        rainfall = float(rainfall)
    except:
        rainfall = 1000.0

    # Calculate water harvesting potential (liters/year)
    potential = calculate_potential(user_input, rainfall)

    # Recommend suitable harvesting structure (e.g., recharge pit, trench)
    structure = recommend_structure(user_input, potential)

    # Estimate structure dimensions based on structure type and potential
    dimensions = calculate_structure_dimensions(structure, potential)

    # Estimate cost and benefit ratio
    cost, benefit = cost_estimation(potential, structure)

    # Calculate household yearly water demand (135 liters/person/day × dwellers × 365 days)
    yearly_demand = user_input.dwellers * 135 * 365

    # Calculate percentage of demand that can be met
    coverage_percent = round((potential / yearly_demand) * 100, 2) if yearly_demand > 0 else 0

    # Generate demand status based on coverage percentage
    if coverage_percent >= 100:
        demand_status = f"Fully sufficient ({coverage_percent}%)"
    elif coverage_percent >= 70:
        demand_status = f"Adequate ({coverage_percent}%)"
    elif coverage_percent >= 30:
        demand_status = f"Partial ({coverage_percent}%)"
    else:
        demand_status = f"Minimal ({coverage_percent}%)"

    # Create result object with all details
    result = AssessmentResult(
        feasibility="Feasible" if potential > 0 else "Not Feasible",
        runoff_capacity=potential,
        recommended_structure=structure,
        estimated_cost=cost,
        benefit_ratio=benefit,
        gw_depth=user_input.gw_depth  # depth to groundwater table (in meters)
    ).to_dict()

    # Add extra details to result dictionary
    result.update({
        "yearly_demand_liters": yearly_demand,   # yearly water requirement (liters/year)
        "coverage_percentage": coverage_percent, # % of demand covered
        "demand_met_status": demand_status,      # textual description
        "structure_dimensions": dimensions,      # dimensions of suggested structure
        "rainfall_used_mm": rainfall             # rainfall considered (mm/year)
    })

    return result
