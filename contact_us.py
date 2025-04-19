import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re 


SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USER = "support@aptpath.in"
SMTP_PASSWORD = "kjydtmsbmbqtnydk"  
SENDER_EMAIL = "support@aptpath.in"
RECEIVER_EMAIL = "shawmanish361@gmail.com"  

def is_valid_email(email):
    """Check if the email is valid using regex."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def send_email(subject, body, receiver_email):
    """Function to send an email."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())

        return True  
    except Exception as e:
        st.error(f"❌ Email failed: {e}")  
        return False  

def display_contact_us():


    # Frequently Asked Questions 
    st.subheader("❓ Frequently Asked Questions")
    
    faqs = {
        "🌍 What is this platform about?": "This platform provides real-time insights into air quality and pollution levels using interactive data visualizations.",
        "📊 How do I navigate the dashboard?": "Use the sidebar to access different sections of the dashboard, including live data, historical trends, and analysis reports.",
        "📥 Can I download reports?": "Currently, report downloads are not supported, but we are working on adding this feature soon.",
        "📩 How do I contact support?": "You can reach out to us by filling out the contact form below, and our team will respond as soon as possible.",
        "⏳ Is the data updated in real-time?": "Yes, our platform fetches real-time air quality data from reliable sources and updates it periodically.",
        "📱 Can I access this platform on mobile devices?": "Yes, our platform is mobile-friendly and can be accessed on any device with an internet connection."
    }

    for question, answer in faqs.items():
        with st.expander(question):
            st.write(answer)

    st.markdown("<br><hr>", unsafe_allow_html=True)  # Adds a separator line

    #Contact Form
    st.subheader("📩 Get in Touch")

    name = st.text_input("Your Name", placeholder="Enter your full name")
    email = st.text_input("Your Email", placeholder="Enter your email address")
    message = st.text_area("Your Message", placeholder="Type your message here...")

    if st.button("✉️ Send Message"):
        if not name.strip():
            st.warning("⚠️ Please enter your name.")
        elif not is_valid_email(email):
            st.warning("⚠️ Please enter a valid email address.")
        elif not message.strip():
            st.warning("⚠️ Your message cannot be empty.")
        else:
            subject = f"New Message from {name}"
            body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            if send_email(subject, body, RECEIVER_EMAIL):  
                st.success("✅ Message sent successfully!")
            else:
                st.error("❌ Failed to send message. Please try again later.")



