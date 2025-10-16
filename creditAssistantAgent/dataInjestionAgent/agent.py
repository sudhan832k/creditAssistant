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

Your job:
- Use the provided customer_id to fetch customer data.
- Call the necessary tool `get_customer_by_id(customer_id)` to get data.
- Return the tool's output back to the Root Agent.
- Do NOT make any credit decisions.
- Do NOT summarize or alter the data.
- Do NOT stop the workflow; the Root Agent will handle the next steps.
"""
dataInjestionAgent = LlmAgent(
    model="gemini-2.5-flash",
    name="Data_Ingestion_Agent",
    instruction=instructions,
    tools=[McpToolset(connection_params=mcp_connection)]
)

a2a_app = to_a2a(dataInjestionAgent, port=8080)