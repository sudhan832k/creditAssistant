from google.adk.agents import LlmAgent,Agent
from dotenv import load_dotenv
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

load_dotenv()

instructions = """
You are the Credit Analyzer Agent.

Your job:
- Receive customer data from the Root Agent.
- Call the necessary decision tool to determine APPROVE, REJECT, or REVIEW.
- If REJECT, provide a short actionable recommendation for the customer.
- Return the result to the Root Agent in JSON format:

{
  "decision": "APPROVE" | "REJECT" | "REVIEW",
  "reason": "<reason from decision tool>",
  "recommendation": "<short recommendation if REJECT, else empty>"
}

Rules:
- Do NOT make guesses about missing data.
- Only provide the recommendation if the decision is REJECT; otherwise leave it empty.

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