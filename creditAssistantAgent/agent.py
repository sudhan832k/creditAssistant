from google.adk.agents import LlmAgent,SequentialAgent,Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH,RemoteA2aAgent 
from dotenv import load_dotenv
from .dataInjestionAgent.agent import dataInjestionAgent
from .creditAnalyserAgent.agent import creditAnalyzerAgent   

load_dotenv()

instructions  = """
You are the root agent. Your job is to route user queries through sub-agents step by step:

Sub-agents:
- data ingestion agent: retrieves customer data
- credit analyzer agent: approves or rejects credit limit increase

Workflow:
1. When a user request arrives, check for `customer_id`. If missing, respond: "Customer ID is required."
2. If `customer_id` is present, call the data ingestion agent with that ID.
3. Do NOT make any credit decisions yourself.
4. After receiving the response from the data ingestion agent, call the credit analyzer agent with that data.
5. Only after receiving the response from the analyzer, return a final user-facing message.
6. Never call any sub-agent more than once per request.
7. Do NOT include internal reasoning or database details in the user-facing reply.
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