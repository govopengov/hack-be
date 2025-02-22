import csv
from langgraph.graph import StateGraph
from tal_trip_planner.crew import TalTripPlanner

# Load CSV knowledge base
def load_csv_data(file_path):
    """Loads travel data from CSV."""
    try:
        with open(file_path, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            return [row for row in csvReader]
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []

# Define LangGraph State
class TravelState:
    def __init__(self, user_input):
        self.user_input = user_input
        self.result = {}

# Initialize CrewAI instance
crew_ai = TalTripPlanner().crew()

# Define LangGraph nodes that call CrewAI agents
def route_identifier(state: dict):
    """Finds the best travel route using CrewAI."""
    inputs = state.get("user_input", "")
    if not inputs:
        state["result"] = {"error": "Invalid user input."}
        return state

    crew_outputs = crew_ai.kickoff_for_each(inputs=[inputs])
    if crew_outputs:
        state["result"] = crew_outputs[0].json_dict or {}
    else:
        state["result"] = {"error": "CrewAI did not return a result."}
    
    return state

def cost_calculator(state: dict):
    """Calculates estimated cost using CrewAI."""
    if "error" in state.get("result", {}):
        return state

    inputs = {"route": state["result"]}
    crew_outputs = crew_ai.kickoff_for_each(inputs=[inputs])
    if crew_outputs:
        state["result"]["estimated_cost"] = crew_outputs[0].json_dict.get("estimated_cost", "N/A")
    
    return state

def comfort_assessor(state: dict):
    """Assesses travel comfort using CrewAI."""
    if "error" in state.get("result", {}):
        return state

    inputs = {"route": state["result"]}
    crew_outputs = crew_ai.kickoff_for_each(inputs=[inputs])
    if crew_outputs:
        state["result"]["comfort_score"] = crew_outputs[0].json_dict.get("comfort_score", "N/A")
    
    return state

def policy_enforcer(state: dict):
    """Ensures travel policy compliance using CrewAI."""
    if "error" in state.get("result", {}):
        return state

    inputs = {"route": state["result"]}
    crew_outputs = crew_ai.kickoff_for_each(inputs=[inputs])
    if crew_outputs:
        state["result"]["policy_compliant"] = crew_outputs[0].json_dict.get("policy_compliant", True)
    
    return state

# Build the LangGraph workflow
travel_workflow = StateGraph(dict)  # ✅ Uses dict as state

# Add nodes to the graph
travel_workflow.add_node("route_identifier", route_identifier)
travel_workflow.add_node("cost_calculator", cost_calculator)
travel_workflow.add_node("comfort_assessor", comfort_assessor)
travel_workflow.add_node("policy_enforcer", policy_enforcer)

# Set the entry point for LangGraph
travel_workflow.set_entry_point("route_identifier")

# Define execution flow
travel_workflow.add_edge("route_identifier", "cost_calculator")
travel_workflow.add_edge("cost_calculator", "comfort_assessor")
travel_workflow.add_edge("comfort_assessor", "policy_enforcer")

# Compile the LangGraph workflow
travel_app = travel_workflow.compile()
