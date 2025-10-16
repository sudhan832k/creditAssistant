from google.adk.agents import LlmAgent,Agent
from dotenv import load_dotenv
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

load_dotenv()

instructions = """
You are the Credit Analyzer Agent.

Rules:
- Receive customer data from the root agent.
- Use the decision tool to determine APPROVE, REJECT, or REVIEW.
- If REJECT, provide a short, actionable recommendation; otherwise leave it empty.
- Return exactly this JSON structure to the root agent:

{
  "decision": "APPROVE" | "REJECT" | "REVIEW",
  "reason": "<reason from decision tool>",
  "recommendation": "<short actionable recommendation if REJECT; otherwise empty>"
}

- Do NOT guess missing fields.
- Do NOT make user-facing replies yourself.


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