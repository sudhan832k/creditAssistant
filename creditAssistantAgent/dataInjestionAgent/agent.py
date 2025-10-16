from fastapi import FastAPI
from google.adk.agents import LlmAgent,Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
from dotenv import load_dotenv
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from a2a.types import AgentCard

load_dotenv()

# MCP server connection
mcp_connection = SseConnectionParams(
    url="http://127.0.0.1:8090/sse"
)
instructions = """
You are the Data Ingestion Agent.

Rules:
- Always call the tool `get_customer_by_id(customer_id)` to fetch customer data.
- Do NOT analyze, summarize, or make any decisions.
- Return exactly the JSON output from the tool to the root agent.
- Never send user-facing messages or explanations.
- The root agent will handle the next steps.
"""
dataInjestionAgent = LlmAgent(
    model="gemini-2.5-flash",
    name="Data_Ingestion_Agent",
    instruction=instructions,
    tools=[McpToolset(connection_params=mcp_connection)]
)

a2a_app = to_a2a(dataInjestionAgent, port=8080)