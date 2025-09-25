# app/app.py

# Load environment variables (like API keys) from a .env file
from dotenv import load_dotenv
load_dotenv()

# Import Flask framework for building the backend API
from flask import Flask, request, jsonify

# Import the service function that performs the RTRWH assessment
# The try/except ensures imports work both inside the "app" package and standalone
try:
    from .services import assess_rtrwh
except Exception:
    from services import assess_rtrwh

# Initialize the Flask application
app = Flask(__name__)


# Define API endpoint `/assess` that accepts POST requests
@app.route("/assess", methods=["POST"])
def assess():
    """
    API endpoint to assess Rooftop Rainwater Harvesting (RTRWH).
    Expects a JSON payload with user input data.

    Example Input JSON:
    {
        "name": "John",
        "location": "Delhi",
        "latitude": 28.6,
        "longitude": 77.2,
        "dwellers": 5,
        "roof_area": 100,
        "open_space": 50,
        "gw_depth": 10,
        "rainfall_mm": 800
    }
    """
    # Extract JSON data from the request
    data = request.get_json()
    if not data:
        # Return error if input is missing or invalid
        return jsonify({"error": "Invalid JSON input"}), 400

    try:
        # Call the core service function to compute assessment
        result = assess_rtrwh(data)
        return jsonify(result)  # Return results as JSON
    except Exception as e:
        # Handle unexpected errors gracefully
        return jsonify({"error": str(e)}), 500


# Run the Flask app only if this script is executed directly
if __name__ == "__main__":
    # Host 0.0.0.0 makes it accessible on LAN (not just localhost)
    # Port 5000 is the default
    # Debug=True enables auto-reload and detailed error pages
    app.run(host="0.0.0.0", port=5000, debug=True)
