from google.adk.agents import LlmAgent,SequentialAgent,Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH,RemoteA2aAgent 
from dotenv import load_dotenv
from .dataInjestionAgent.agent import dataInjestionAgent
from .creditAnalyserAgent.agent import creditAnalyzerAgent   

load_dotenv()

instructions  = """
You are the Root Agent for credit limit increase requests.

Sub-agents:
- Data Ingestion Agent: fetches customer data.
- Credit Analyzer Agent: approves or rejects credit requests.

Workflow:
1. Receive the user's request (e.g., "Increase credit limit for customer 1").
2. If the request does not include a customer_id, stop and ask the user for it.
3. Call the Data Ingestion Agent with the customer_id.
4. Wait for the Data Ingestion Agent to return the customer data.
5. Pass the customer data to the Credit Analyzer Agent.
6. Wait for the analyzer's decision (APPROVE, REJECT, or REVIEW) and reason.
7. Return a final response to the user summarizing the decision and recommendation (if rejected).

Rules:
- Do NOT make any credit decisions yourself.
- Never return a final response until the analyzer agent has been called.
"""

# data_ingestion_agent = RemoteA2aAgent(
#     name="data_ingestion_agent",
#     description=(
#         "Retrieves full customer credit data from the database given a customer_id. "
#         "This agent ONLY fetches and returns structured data — it does NOT perform "
#         "any analysis, decision-making, or credit evaluation."
#     ),
#     agent_card=f"http://localhost:8080{AGENT_CARD_WELL_KNOWN_PATH}",
# )

# credit_analyzer_agent = RemoteA2aAgent(
#     name="credit_analyzer_agent",
#     description=(
#         "Takes structured customer credit data as input and determines whether to "
#         "APPROVE, REJECT, or REVIEW the credit limit increase request. "
#         "Uses deterministic rules to evaluate financial metrics and payment history. "
#         "Does NOT fetch or modify any data."
#     ),
#     agent_card=f"http://localhost:8081{AGENT_CARD_WELL_KNOWN_PATH}",
# )


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