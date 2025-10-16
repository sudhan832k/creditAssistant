from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from a2a.types import AgentCard
from starlette.applications import Starlette
from starlette.routing import Mount

# Define sub-agents
agent1 = LlmAgent(model="gemini-2.5-flash", name="data_ingestion_agent", instruction="Fetch customer data.")
agent2 = LlmAgent(model="gemini-2.5-flash", name="credit_validation_agent", instruction="Validate customer credit.")
agent3 = LlmAgent(model="gemini-2.5-flash", name="approval_decision_agent", instruction="Approve or reject credit request.")

# Define agent cards
card1 = AgentCard(
    name="data_ingestion_agent",
    url="http://localhost:8080/a2a/data_ingestion_agent",
    description="Handles customer data fetching.",
    version="1.0.0",
        capabilities={"fetch_customer_data": "Retrieve customer info from DB"},  # ✅ REQUIRED
    skills=[],  # ✅ REQUIRED
    defaultInputModes=["application/json"],
    defaultOutputModes=["application/json"]
)

card2 = AgentCard(
    name="credit_validation_agent",
    url="http://localhost:8080/a2a/credit_validation_agent",
    description="Handles credit score validation.",
    version="1.0.0",
        capabilities={"fetch_customer_data": "Retrieve customer info from DB"},  # ✅ REQUIRED
    skills=[],  # ✅ REQUIRED
    defaultInputModes=["application/json"],
    defaultOutputModes=["application/json"]
)

card3 = AgentCard(
    name="approval_decision_agent",
    url="http://localhost:8080/a2a/approval_decision_agent",
    description="Handles final approval decision.",
    version="1.0.0",
        capabilities={"fetch_customer_data": "Retrieve customer info from DB"},  # ✅ REQUIRED
    skills=[],  # ✅ REQUIRED
    defaultInputModes=["application/json"],
    defaultOutputModes=["application/json"]
)

# Create individual A2A apps (but don’t serve them yet)
a2a_1 = to_a2a(agent1, agent_card=card1)
a2a_2 = to_a2a(agent2, agent_card=card2)
a2a_3 = to_a2a(agent3, agent_card=card3)

# Merge all apps into one
main_app = Starlette(routes=[
    Mount("/a2a/data_ingestion_agent", app=a2a_1),
    Mount("/a2a/credit_validation_agent", app=a2a_2),
    Mount("/a2a/approval_decision_agent", app=a2a_3),
])

