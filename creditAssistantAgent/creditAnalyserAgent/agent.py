from google.adk.agents import LlmAgent,Agent
from dotenv import load_dotenv
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

load_dotenv()

instructions = """
You are the Credit Analyzer Agent. 
- Receive customer data from the Root Agent. 
- Determine whether to APPROVE, REJECT, or REVIEW the credit limit increase request using the decision tool. 
- If REJECT, provide a short actionable recommendation. 
- Return only the JSON result to the Root Agent in this format:
{
  "decision": "APPROVE" | "REJECT" | "REVIEW",
  "reason": "<reason from decision tool>",
  "recommendation": "<short actionable recommendation if REJECT, else empty>"
}
- Do NOT fetch data or interact with any database. 
- Do NOT send any response directly to the user.

"""
mcp_connection = SseConnectionParams(
    url="http://127.0.0.1:8091/sse"
)

creditAnalyzerAgent = Agent(
    model="gemini-2.5-flash",
    name="credit_analyzer_agent",
    instruction=instructions,
    tools=[McpToolset(connection_params=mcp_connection)]
)
a2a_app = to_a2a(creditAnalyzerAgent, port=8081)