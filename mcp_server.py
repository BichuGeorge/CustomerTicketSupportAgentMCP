from fastmcp import FastMCP
from tools.sheet_connector import (
    append_processed_ticket,
    fetch_new_tickets,
    update_ticket
)
from tools.classify_ticket import classify_ticket
from tools.generate_reply import generate_reply
from tools.gmail_sender import send_email_smtp
import os
os.environ["DANGEROUSLY_OMIT_AUTH"] = "true"
mcp = FastMCP("AI Powered Customer Support Ticket Management System" )

@mcp.tool(
    name="resolve_ticket",
    description="Resolve a customer support ticket by classifying the issue, generating a reply, and sending an email response."
)
def resolve_ticket(name, email, message):
    try:
        classification = classify_ticket(message)
        sentiment = classification['sentiment']
        issue_type = classification['issue_type']
        reply = generate_reply(message)
        fake_ticket = {
            'Name': name,
            'Email': email,
            'IssueType': issue_type,
            'Message': message
        }
        append_processed_ticket(
            ticket=fake_ticket,
            sentiment=sentiment,
            issue_type=issue_type,
            reply=reply
        )
        mail_result = send_email_smtp(
            to_email=email,
            subject=f"Support Ticket Update: {issue_type} Issue",
            body=reply
        )
        return {
            "status": "success",
            "email_message": mail_result.get("message", "Email sent successfully"),
            "email_status": mail_result.get("status"),
            "sentiment": sentiment,
            "issue_type": issue_type,
            "reply": reply
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
if __name__ == "__main__":
    mcp.run()
