import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def dashboard():
 
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = 0
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'quiz_feedback' not in st.session_state:
        st.session_state.quiz_feedback = ""
    if 'selected_answer' not in st.session_state:
        st.session_state.selected_answer = None
    
    # Quiz Data
    quiz_data = [
        ("What is the primary pollutant responsible for acid rain?",
         ["Carbon Dioxide (CO₂)", "Sulfur Dioxide (SO₂)", "Methane (CH₄)", "Ozone (O₃)"],
         "Sulfur Dioxide (SO₂)"),
        ("Which gas is the major contributor to global warming?",
         ["Oxygen (O₂)", "Carbon Dioxide (CO₂)", "Nitrogen (N₂)", "Helium (He)"],
         "Carbon Dioxide (CO₂)"),
        ("What is the main cause of ozone layer depletion?",
         ["Carbon Monoxide (CO)", "Chlorofluorocarbons (CFCs)", "Sulfur Dioxide (SO₂)", "Methane (CH₄)"],
         "Chlorofluorocarbons (CFCs)"),
        ("Which renewable energy source is most widely used?",
         ["Solar Energy", "Wind Energy", "Hydropower", "Geothermal Energy"],
         "Hydropower"),
        ("What is the leading cause of deforestation?",
         ["Urban Expansion", "Logging", "Agriculture", "Mining"],
         "Agriculture"),
        ("Which sector is the largest consumer of freshwater?",
         ["Industry", "Agriculture", "Household", "Energy Production"],
         "Agriculture"),
        ("What is the primary source of marine pollution?",
         ["Oil Spills", "Plastic Waste", "Chemical Waste", "Sewage"],
         "Plastic Waste"),
        ("Which country emits the most carbon dioxide?",
         ["USA", "China", "India", "Russia"],
         "China"),
        ("What is the main component of smog?",
         ["Nitrogen Dioxide (NO₂)", "Ozone (O₃)", "Sulfur Dioxide (SO₂)", "Carbon Monoxide (CO)"],
         "Ozone (O₃)"),
        ("Which energy source produces the least greenhouse gases?",
         ["Coal", "Natural Gas", "Nuclear", "Oil"],
         "Nuclear")
    ]
    
    # Power BI Dashboard Embed
    st.subheader("📊 Power BI Dashboard")
    power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiOWRkYmI2NTktMjg2NC00N2VhLThmYzUtMjBjZDRkOGQzNWUxIiwidCI6ImJiYzNmZmNkLTczZjQtNDczMC1hZjk4LTVjODQxZDNkODljYyJ9&pageName=14d5b4335b1421fb0a39"
    st.markdown(f'<iframe width="800" height="600" src="{power_bi_url}" frameborder="0" allowFullScreen></iframe>', unsafe_allow_html=True)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    
    # Quiz Section
    st.title("🧠 Quick Quiz")
    if not st.session_state.quiz_completed:
        question, options, correct_answer = quiz_data[st.session_state.quiz_index]
        answer = st.radio(question, options, index=None, key=f"quiz_{st.session_state.quiz_index}")
        
        if st.button("Submit Answer"):
            if answer:
                if answer == correct_answer:
                    st.session_state.quiz_feedback = "✅ Correct!"
                else:
                    st.session_state.quiz_feedback = f"❌ Incorrect. The correct answer is {correct_answer}."
                
                if st.session_state.quiz_index < len(quiz_data) - 1:
                    st.session_state.quiz_index += 1
                else:
                    st.session_state.quiz_completed = True
                st.rerun()
        
        st.write(st.session_state.quiz_feedback)
    else:
        st.success("🎉 You have completed the quiz!")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    

    st.markdown("""
    <style>
    div[data-baseweb="slider"] > div:nth-child(1) > div:nth-child(2) {
        height: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    

    st.title("📝 Feedback")
    rating = st.slider("Rate your experience:", min_value=1, max_value=5, value=1)
    feedback = st.text_area("Share your feedback:")
    
    # SMTP Credentials for Feedback Emails
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    smtp_user = "support@aptpath.in"
    smtp_password = "kjydtmsbmbqtnydk"  
    sender_email = "support@aptpath.in"
    receiver_emails = ["shawmanish361@gmail.com"]  
    

    def send_email(subject, body, receiver_email):
        try:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            return True
        except Exception as e:
            st.error(f"Email failed: {e}")
            return False
    

    if st.button("Submit Feedback", key="feedback_btn"):
        if feedback.strip():
            subject = f"Feedback from User - Rating: {rating}"
            body = f"Rating: {rating}\n\nFeedback:\n{feedback}"
            email_sent = True
            for receiver in receiver_emails:
                if not send_email(subject, body, receiver):
                    email_sent = False
                    break
            if email_sent:
                st.success(f"Thank you for your feedback! You rated us {rating} ⭐.")
            else:
                st.error("Failed to send feedback email. Please try again later.")
        else:
            st.error("Please enter some feedback before submitting.")


