import streamlit as st
from tools.sheet_connector import append_ticket_to_sheet

st.set_page_config(
    page_title="Submit a Support Ticket Ticket",
    page_icon=":ticket:"
)
st.title("Submit a Support Ticket")
st.markdown("We're here to help! Please fill out the form below to submit your support ticket.")
# Form for submitting a support ticket
with st.form(key='ticket_form'):
    name = st.text_input("Your Name", placeholder="Enter your name")
    email = st.text_input("Your Email", placeholder="Enter your email")
    issue_type = st.selectbox(
        "Issue Type",
        options=["Billing", "Technical", "Login Issue", "Other"],
        index=0
    )
    message = st.text_area(
        "Message",
        placeholder="Describe your issue or question in detail",
        height=150
    )
    submitted = st.form_submit_button("Submit Ticket")
    if submitted:
        if not name or not email or not message:
            st.error("Please fill out all fields.")
        else:
            # Append the ticket to the Google Sheet
            append_ticket_to_sheet(name, email, issue_type, message)
            st.success("Your ticket has been submitted successfully! We will get back to you shortly.")