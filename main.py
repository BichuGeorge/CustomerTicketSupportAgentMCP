import streamlit as st
from tools.sheet_connector import (
    append_processed_ticket,
    fetch_new_tickets,
    update_ticket
)
from tools.classify_ticket import classify_ticket
from tools.generate_reply import generate_reply
from tools.gmail_sender import send_email_smtp
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="AI Ticket Manager",
    layout="centered",
)

st.title("AI Ticket Manager")
st.markdown("Manage your support tickets with AI assistance.")

tickets = fetch_new_tickets() # Finding pending tickets

if not tickets:
    st.success("No new tickets found. All tickets are processed.")
else:
    for i, ticket in enumerate(tickets, start=1):
        if ticket['Sentiment'] and ticket['AutoReply']:
            continue
        with st.expander(f" Ticket #{i} from {ticket['Name']} ({ticket['Email']})"):
            st.markdown("**: Message:**")
            st.info(ticket['Message'])
            if st.button(f"Analyze & Respond Ticket #{i}"):
                with st.spinner("Running AI classification reply generation..."):
                    classification = classify_ticket(ticket['Message'])
                    reply = generate_reply(ticket['Message'])

                st.success("AI analysis complete!")
                st.markdown("**: Sentiment:** " + classification['sentiment'])
                st.markdown("**: Issue Type:** " + classification['issue_type'])
                st.markdown("**: Suggested Reply:** ")
                st.text_area(
                    "AI Generated Reply",
                    reply,
                    height=150,
                    disabled=True
                )
                update_ticket(
                    row_number=i+1,
                    sentiment=classification['sentiment'],
                    issue_type=classification['issue_type'],
                    reply=reply
                )
                append_processed_ticket(
                    ticket = ticket,
                    sentiment=classification['sentiment'],
                    issue_type=classification['issue_type'],
                    reply=reply
                )

                with st.spinner("Sending Email Reply..."):
                    success = send_email_smtp(
                        to=ticket['Email'],
                        subject=f"Support Ticket #{i} Response",
                        body=reply
                    )
                    if success:
                        st.success(f"Email sent successfully")
                    else:
                        st.error(f"Failed to send email")
                    
                    st.info("Ticket processed and email sent successfully!")
