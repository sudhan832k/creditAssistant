from google.adk.agents import LlmAgent,SequentialAgent,Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH,RemoteA2aAgent 
from dotenv import load_dotenv
from .dataInjestionAgent.agent import dataInjestionAgent
from .creditAnalyserAgent.agent import creditAnalyzerAgent   

load_dotenv()

instructions  = """
You are the Root Agent for credit limit increase requests. 
- First, check if the user's request includes a customer_id. If not, ask the user for it. 
- If customer_id is present, call the Data Ingestion Agent to fetch customer data. 
- Wait for the Data Ingestion Agent to return the data. 
- Then call the Credit Analyzer Agent with the customer data. 
- Wait for the analyzer's decision. 
- Return only the final decision and recommendation to the user. 
Do NOT make any credit decisions yourself. Do NOT return data from sub-agents directly.

Sub-agents:
- DataIngestionAgent: fetches customer data.
- CreditAnalyzerAgent: approves or rejects credit requests.
"""

data_ingestion_agent = RemoteA2aAgent(
    name="dataIngestionAgent",
    description=(
        "You are a sub-agent. Fetch customer data using the provided customer_id. "
        "Always return the result to the Root Agent. "
        "Do NOT analyze, summarize, or make any credit decisions."
    ),
    agent_card=f"http://localhost:8080{AGENT_CARD_WELL_KNOWN_PATH}",
)

credit_analyzer_agent = RemoteA2aAgent(
    name="creditAnalyzerAgent",
    description=(
        "You are a sub-agent. Receive customer data from the Root Agent and determine "
        "APPROVE, REJECT, or REVIEW for the credit limit increase request. "
        "Return the result to the Root Agent. "
        "If REJECT, provide a short actionable recommendation. "
        "Do NOT fetch data or interact with any database directly."
    ),
    agent_card=f"http://localhost:8081{AGENT_CARD_WELL_KNOWN_PATH}",
)


# root_agent = SequentialAgent(
#     name="CreditRouterAgent",
#     sub_agents=[data_ingestion_agent, credit_analyzer_agent],
#     description=(
#         "A sequential workflow agent that handles credit limit increase requests end-to-end. "
#         "It executes sub-agents in the following order: "
#         "1) Data Ingestion Agent: fetches and structures full customer data based on the provided customer ID, "
#         "2) Credit Analyzer Agent: analyzes the fetched customer data and provides a credit decision "
#         "(APPROVE, REJECT, or REVIEW) along with a reason. "
#         "Each step depends on the output of the previous sub-agent. "
#         "The Router Agent itself does not make any credit decisions; it only coordinates the workflow "
#         "and returns the final result to the user."
#     )
# )

root_agent = Agent(
    model="gemini-2.5-flash",
    name="Credit_Assistant",
    instruction=instructions,
    sub_agents=[dataInjestionAgent,creditAnalyzerAgent]
    #sub_agents=[data_ingestion_agent,credit_analyzer_agent]
)