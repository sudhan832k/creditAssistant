from fastmcp.server import FastMCP

mcp = FastMCP("MCP_Server_two")

@mcp.tool(
    name="evaluate_credit_request",
    description="Evaluate a credit limit increase request using deterministic rules."
)
def evaluate_credit_request(customer):
    """
    Evaluate a credit limit increase request using deterministic rules.
   
    Input: dictionary with keys:
        customer_id, customer_name, current_credit_limit, payment_terms,
        credit_limit_increase_requested, total_sales_12mo, current_receivables,
        current_receivable_status, payment_history, disputes, credit_rating


    Output: dictionary with fields:
        decision: "APPROVE" | "REJECT" | "REVIEW"
        reason: short string explaining why
    """
    # Extract relevant fields safely
    print("Evaluating customer:", customer)
    limit = float(customer.get("current_credit_limit", 0))
    req_increase = float(customer.get("credit_limit_increase_requested", 0))
    total_sales = float(customer.get("total_sales_12mo", 0))
    receivables = float(customer.get("current_receivables", 0))
    status = str(customer.get("current_receivable_status", "")).strip()
    history = str(customer.get("payment_history", "")).lower()
    disputes = int(customer.get("disputes", 0))
    rating = str(customer.get("credit_rating", "")).upper().strip()
    terms = str(customer.get("payment_terms", "")).strip()


    # Helper: detect on-time % in text (if any)
    import re
    match = re.search(r'(\d{2,3})\s*%.*on[- ]?time', history)
    on_time_pct = int(match.group(1)) if match else 0


    # ----- RULE 1: AUTO REJECT -----
    if status in ["60-90d", "90+d overdue"]:
        return {
            "decision": "REJECT",
            "reason": "Receivables overdue ({}).".format(status)
        }


    if rating in ["C", "C+", "C-", "D", "D-"]:
        return {
            "decision": "REJECT",
            "reason": f"Low credit rating ({rating})."
        }


    if disputes >= 3:
        return {
            "decision": "REJECT",
            "reason": f"High number of disputes ({disputes})."
        }


    if on_time_pct < 85:
        return {
            "decision": "REJECT",
            "reason": f"Poor payment history ({on_time_pct}% on-time)."
        }


    # ----- RULE 2: MANUAL REVIEW -----
    # Percentage requested increase
    requested_pct = (req_increase / limit * 100) if limit else 0
    receivable_ratio = (receivables / total_sales) if total_sales else 0


    if requested_pct > 50:
        return {
            "decision": "REVIEW",
            "reason": f"Requested increase {requested_pct:.1f}% > 50% of current limit."
        }


    if receivable_ratio > 0.25:
        return {
            "decision": "REVIEW",
            "reason": f"Receivables are {receivable_ratio*100:.1f}% of total sales (high exposure)."
        }


    if terms in ["Net 60", "Net 90"]:
        return {
            "decision": "REVIEW",
            "reason": f"Long payment terms ({terms}) require manual assessment."
        }


    if rating in ["B", "B-"]:
        return {
            "decision": "REVIEW",
            "reason": f"Mid-tier credit rating ({rating})."
        }


    # ----- RULE 3: AUTO APPROVE -----
    if (rating in ["A+", "A", "A-"]
        and status == "Current"
        and disputes == 0
        and on_time_pct >= 95
        and req_increase <= 0.3 * limit
        and receivable_ratio <= 0.15):
        return {
            "decision": "APPROVE",
            "reason": "Meets all auto-approval conditions (A-rating, current receivables, low risk)."
        }


    # ----- DEFAULT -----
    return {
        "decision": "REVIEW",
        "reason": "No clear rule triggered; defaulting to manual review."
    }


mcp.run(
    transport="sse",
    host="127.0.0.1",
    port=8091
)