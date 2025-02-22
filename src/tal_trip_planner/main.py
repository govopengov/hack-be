#!/usr/bin/env python
import sys
import warnings
import csv
import json

from datetime import datetime

from tal_trip_planner.crew import TalTripPlanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """

    # inputs = {
    #     'topic': 'AI LLMs',
    #     'current_year': str(datetime.now().year),
    #     "source": "Atru",
    #     "destination": "Pune"
    # }

    inputs = []
    outputs = []

    with open('./knowledge/users.csv', encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        inputs = [row for row in csvReader]

    # inputs = {
    #     'topic': 'AI LLMs',
    #     'current_year': str(datetime.now().year),
    #     "source": "Atru",
    #     "destination": "Pune",
    #     "travel_date": "2025-02-28"
    # }

 
    try:
        crew_outputs = TalTripPlanner().crew().kickoff_for_each(inputs=inputs)

        for output in crew_outputs:
            outputs.append(output.json_dict)

        return outputs
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        "source": "Atru",
        "destination": "Pune",
        "travel_date": "2025-02-28"
    }
    try:
        TalTripPlanner().crew().train(n_iterations=1, filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TalTripPlanner().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        TalTripPlanner().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
