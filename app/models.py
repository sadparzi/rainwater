# app/models.py
class UserInput:
    def __init__(self, name, location, latitude, longitude, dwellers, roof_area, open_space, gw_depth):
        self.name = name
        self.location = location
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.dwellers = int(dwellers)
        self.roof_area = float(roof_area)
        self.open_space = float(open_space)
        self.gw_depth = float(gw_depth)

class AssessmentResult:
    def __init__(self, feasibility, runoff_capacity, recommended_structure, estimated_cost, benefit_ratio, gw_depth):
        self.feasibility = feasibility
        self.runoff_capacity = runoff_capacity
        self.recommended_structure = recommended_structure
        self.estimated_cost = estimated_cost
        self.benefit_ratio = benefit_ratio
        self.gw_depth = gw_depth

# app/models.py

# This file defines the core data models (blueprints) used across the application.
# These classes represent structured data passed between the frontend, backend, and services.


class UserInput:
    """
    Represents the user-provided input data for rainwater harvesting assessment.
    All fields are validated and converted to appropriate types (float/int).
    """
    def __init__(self, name, location, latitude, longitude, dwellers, roof_area, open_space, gw_depth):
        # Name of the user or household
        self.name = name
        # City/town/village name (used to fetch rainfall if coordinates are not provided)
        self.location = location
        # Latitude of the property (converted to float)
        self.latitude = float(latitude)
        # Longitude of the property (converted to float)
        self.longitude = float(longitude)
        # Number of people living in the household (used to calculate water demand)
        self.dwellers = int(dwellers)
        # Roof catchment area in square meters
        self.roof_area = float(roof_area)
        # Open space available for recharge pits/trenches in square meters
        self.open_space = float(open_space)
        # Groundwater depth (distance from surface to water table) in meters
        self.gw_depth = float(gw_depth)


class AssessmentResult:
    """
    Represents the output of the assessment with calculated results.
    Stores feasibility, potential capacity, recommended structure, cost, and groundwater info.
    """
    def __init__(self, feasibility, runoff_capacity, recommended_structure, estimated_cost, benefit_ratio, gw_depth):
        # Whether the project is feasible or not ("Feasible" / "Not Feasible")
        self.feasibility = feasibility
        # Potential water that can be harvested (liters)
        self.runoff_capacity = runoff_capacity
        # Recommended rainwater harvesting structure (pit, trench, recharge well, etc.)
        self.recommended_structure = recommended_structure
        # Estimated cost in INR
        self.estimated_cost = estimated_cost
        # Benefit-to-cost ratio (High / Medium / Low benefit)
        self.benefit_ratio = benefit_ratio
        # Depth to groundwater table in meters
        self.gw_depth = gw_depth

    def to_dict(self):
        """
        Convert the object into a dictionary (used when returning JSON response).
        """
        return {
            "feasibility": self.feasibility,
            "runoff_capacity": self.runoff_capacity,
            "recommended_structure": self.recommended_structure,
            "estimated_cost": self.estimated_cost,
            "benefit_ratio": self.benefit_ratio,
            # Clearly labeled groundwater depth with unit in meters
            "depth_to_groundwater_m": self.gw_depth
        }
    def to_dict(self):
        return {
            "feasibility": self.feasibility,
            "runoff_capacity": self.runoff_capacity,
            "recommended_structure": self.recommended_structure,
            "estimated_cost": self.estimated_cost,
            "benefit_ratio": self.benefit_ratio,
            "depth_to_groundwater_m": self.gw_depth
        }
