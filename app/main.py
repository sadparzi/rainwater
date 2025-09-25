# app/main.py

# This file defines the FastAPI application and its routes.
# It is the main entry point when running the backend server with FastAPI.
# The API provides an endpoint to assess rooftop rainwater harvesting feasibility.

from fastapi import FastAPI
from pydantic import BaseModel
from app.services import assess_rtrwh  # Import the core assessment function

# Initialize the FastAPI app with a title
app = FastAPI(title="RTRWH & Artificial Recharge Assessment")


class InputData(BaseModel):
    """
    Defines the expected structure of the input JSON request.
    Pydantic automatically validates and converts types.
    Default values are provided where applicable.
    """
    # Name of the user or household (optional)
    name: str | None = None
    # Location (city/town/village) – can be used to fetch rainfall if lat/lon not provided
    location: str | None = None
    # Latitude of the property
    latitude: float | None = 0.0
    # Longitude of the property
    longitude: float | None = 0.0
    # Number of dwellers (default: 1 person)
    dwellers: int | None = 1
    # Roof area in square meters
    roof_area: float | None = 0.0
    # Open space available for recharge structures in square meters
    open_space: float | None = 0.0
    # Annual rainfall in millimeters (optional – can be auto-fetched via API)
    rainfall_mm: float | None = None
    # Depth to groundwater table in meters
    gw_depth: float | None = 0.0


@app.post("/assess")
async def assess(data: InputData):
    """
    API endpoint: POST /assess
    Accepts user input in JSON format, validates with InputData model,
    and passes data to the assessment service.
    Returns a JSON response with assessment results.
    """
    # Convert input data (Pydantic model) into dictionary for processing
    result = assess_rtrwh(data.dict())

    # Return dummy_id for now (can be replaced with database ID if integrated)
    return {"id": "dummy_id", "result": result}
