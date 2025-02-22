from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from .output_schemas.route_identifier_output import RouteIdentifierOutput

@CrewBase
class TalTripPlanner():
    """TalTripPlanner CrewAI implementation"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    csv_source = CSVKnowledgeSource(file_paths=["users.csv"])

    @agent
    def route_identifier(self) -> Agent:
        return Agent(
            config=self.agents_config['route_identifier'],
            verbose=True,
            knowledge_sources=[self.csv_source]
        )

    @agent
    def cost_calculator(self) -> Agent:
        return Agent(config=self.agents_config['cost_calculator'])

    @agent
    def comfort_assessor(self) -> Agent:
        return Agent(config=self.agents_config['comfort_assessor'])

    @agent
    def policy_enforcer(self) -> Agent:
        return Agent(config=self.agents_config['policy_enforcer'])

    @task
    def route_identification_task(self) -> Task:
        return Task(
            config=self.tasks_config['route_identification_task'],
            output_json=RouteIdentifierOutput
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Auto-created by @agent decorator
            tasks=self.tasks,    # Auto-created by @task decorator
            process=Process.sequential,
            memory=False,
            respect_context_window=True,
            verbose=True,
        )