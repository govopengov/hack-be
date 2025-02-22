from flask import Flask, jsonify, request
from tal_trip_planner.travel_graph import travel_app  # ✅ Fix: Remove TravelState import

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/travel-planner', methods=['POST'])
def run_travel_planner():
    try:
        user_input = request.json

        # Check for missing required fields
        required_fields = ["source", "destination", "travel_date"]
        missing_fields = [field for field in required_fields if field not in user_input]

        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # ✅ Fix: Ensure correct initial state format
        initial_state = {"user_input": user_input}

        final_state = travel_app.invoke(initial_state)

        return jsonify(final_state.get("result", {}))  # ✅ Ensure result exists
    except Exception as e:
        return jsonify({"error": str(e)}), 500