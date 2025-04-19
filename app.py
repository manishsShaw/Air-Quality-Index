import streamlit as st
from page1 import display_page1
from page2 import display_page2
from page3 import display_page3
from contact_us import display_contact_us
from page4 import display_page4
from home import home
from dashboard import dashboard
import pandas as pd
import smtplib


page_bg = """
<style>
.stApp {
    background: #000026;
    color: white;
}

/* Centering the login box */
.login-container {
    width: 400px;
    margin: auto;
    padding: 20px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.2);
    text-align: center;
}

/* Stylish Input Fields */
input {
    border-radius: 5px !important;
    padding: 10px;
    width: 100%;
    border: 1px solid white;
    background: rgba(255, 255, 255, 0.2);
    color: white;
}

/* Button Styles */
.stButton > button {
    background: #ff4b4b;
    color: white;
    border-radius: 10px;
    padding: 10px, 15px;
    font-size: 18px;
    font-weight: bold;
    width: 35%;
    transition: 0.3s;
}

.stButton > button:hover {
    background: #ff1e1e;
    transform: scale(1.05);
}

/* Sign-up link */
.signup-text {
    color: #ff4b4b;
    font-weight: bold;
    cursor: pointer;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    min-width: 300px !important;  /* Fixed sidebar width */
    max-width: 300px !important;  /* Prevent expansion */
    background-color: #191942;  /* Sidebar background */
}

/* Sidebar Radio Buttons - Horizontal Alignment */
.stRadio label {
    display: inline-flex !important;
    white-space: nowrap !important; /* Prevent text wrapping */
    overflow-x: hidden !important;
}



[data-testid="stSidebar"] .stRadio input:checked + label {
    background-color: #ff4b4b;
    color: white;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False




# SMTP Configuration
smtp_server = "smtp.office365.com"
smtp_port = 587
smtp_user = "support@aptpath.in"
smtp_password = "kjydtmsbmbqtnydk"
sender_email = "support@aptpath.in"
receiver_emails = ["shawmanish361@gmail.com"]

# Function to send email (optional)
def send_email(subject, message, recipient):
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(sender_email, recipient, email_message)
        return True
    except Exception as e:
        return False

# Login or Sign Up
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center;'>📊 Welcome to the AQI Dashboard</h2>", unsafe_allow_html=True)
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left;'>🔐 Login Here: </h3>", unsafe_allow_html=True)

    # Login Section
    email = st.text_input("Email", key="email")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")

    if st.button("Login"):
        if username and password:
            st.session_state.authenticated = True
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Please enter valid credentials")

    st.markdown("<p>Don't have an account? <span class='signup-text'>Sign up now</span></p>", unsafe_allow_html=True)

    # Sign Up Section
    st.markdown("<h2 style='text-align: left;'>🌍Sign Up Here:</h2>", unsafe_allow_html=True)
    
    user_email = st.text_input("Email", key="User_email")
    new_username = st.text_input("New Username", key="new_username")
    new_password = st.text_input("New Password", type="password", key="new_password")

    if st.button("Sign Up"):
        if user_email and new_username and new_password:
            # Sending welcome email (Optional)
            subject = "Welcome to AQI Dashboard"
            message = f"Hello {new_username},\n\nYour account has been successfully created!"
            email_sent = send_email(subject, message, user_email)

            if email_sent:
                st.success("Account created successfully! Please log in. A confirmation email has been sent.")
            else:
                st.success("Account created successfully! Please log in.")
        else:
            st.error("Please fill in all the fields.")

    st.markdown("</div>", unsafe_allow_html=True)

    


else:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()
    
    # Sidebar Navigation
    st.sidebar.title("✨ Navigation")

    page = st.sidebar.radio("", [
        "🏠 Home",
        "📊 Dashboard",
        "📄 Overview of Pollution",
        "📊 City Comparisons",
        "📈 Impacts and Insights",
        "🌍 AQI Status",
        "📞 Contact Us"
    ], horizontal=True)





    @st.cache_data
    def load_air_quality_data():
        try:
            # Update the file path if necessary
            df = pd.read_csv("Compressed_India_Air_Quality_Data 3.csv")
            return df
        except Exception as e:
            st.error(f"Error loading dataset: {e}")
            return None

    air_quality_data = load_air_quality_data()


    def get_chatbot_response(query):
        """
        Searches the loaded air quality dataset for a matching city.
        Returns air quality details if a matching city is found.
        """
        if air_quality_data is None:
            return "Dataset not available at the moment."
        
        query_lower = query.lower()
        

        if "City" not in air_quality_data.columns:
            return "Dataset format error: 'City' column not found."
        
        cities = air_quality_data["City"].dropna().unique()
        for city in cities:
            if city.lower() in query_lower:
                row = air_quality_data[air_quality_data["City"].str.lower() == city.lower()].iloc[0]
                response = (f"In {row['City']}, {row.get('State', 'N/A')}, the AQI is {row.get('AQI', 'N/A')} "
                            f"with the main pollutant being {row.get('Main Pollutant', 'N/A')}.")
                return response
        
        return "I'm sorry, I couldn't find any air quality data matching your query. Please try specifying a valid city name."

    st.sidebar.markdown("---")
    st.sidebar.subheader("💬 Chatbot")
    chat_input = st.sidebar.text_input("Ask me anything about air quality:")

    if st.sidebar.button("Send"):
        if chat_input.strip():
            response = get_chatbot_response(chat_input)
            st.sidebar.write("🤖 " + response)
        else:
            st.sidebar.write("Please enter a question.")

        
    # Developer Info Section
    st.sidebar.markdown("---")
    st.sidebar.subheader("👨‍💻 Developer Info")
    st.sidebar.markdown("**Name:** Manish Shaw")  # Replace with actual name
    st.sidebar.markdown("📧 **Email:** [mshaw9753@gmail.com](mailto:johndoe@example.com)")  # Replace with actual email
    st.sidebar.markdown("🐙 **GitHub:** [github.com/manishsShaw](https://github.com/manishsShaw)")  # Replace with actual GitHub
    st.sidebar.markdown("🔗 **LinkedIn:** [linkedin.com/in/manish-shaw-272172251/](https://www.linkedin.com/in/manish-shaw-272172251/)")  # Replace with actual LinkedIn



    # Page Navigation Logic
    if page == "🏠 Home":
        home()
    elif page == "📊 Dashboard":
        dashboard()
    elif page == "📄 Overview of Pollution":
        display_page1()
    elif page == "📊 City Comparisons":
        display_page2()
    elif page == "📈 Impacts and Insights":
        display_page3()
    elif page == "🌍 AQI Status":
        display_page4()
    elif page == "📞 Contact Us":
        display_contact_us()
