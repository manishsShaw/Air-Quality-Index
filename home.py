import streamlit as st

def home():
      
    
        st.title("📄Overview")
        

        st.image("images/page 1.png", use_container_width=True)


        st.markdown("""
            <h2 style='text-align: center; color: #2E86C1;'>🌍 Air Quality Index (AQI) Visualization Dashboard</h2>
            <p style='font-size: 18px; text-align: justify;'>
                Welcome to the <b>Air Quality Index (AQI) Visualization Dashboard</b> – a powerful tool designed to help you monitor and analyze air pollution levels across different regions. 
                This dashboard provides real-time insights into air quality, helping users make informed decisions for a healthier environment. 🌱
            </p>

            <h3 style='color: #D35400;'>📊 Key Features</h3>

            <h4 style='color: #33C3FF;'>1️⃣ Air Quality Index Summary</h4>
            <p style='font-size: 18px;'>
                - Displays <b>average pollutant levels</b>, including:  
                🏭 <b>SO₂</b> (Sulfur Dioxide), 🌫️ <b>NO₂</b> (Nitrogen Dioxide), 💨 <b>SPM</b> (Suspended Particulate Matter), 🌪 <b>RSPM</b> (Respirable Suspended Particulate Matter).  
                - Shows the <b>number of monitoring agencies</b> in each state.  
                - Provides a <b>state-wise breakdown</b> of pollution levels.  
            </p>

            <h4 style='color: #33C3FF;'>2️⃣ Count of Agencies by State</h4>
            <p style='font-size: 18px;'>
                - A <b>bar chart</b> illustrating the <b>number of air monitoring agencies</b> per state.  
                - Helps users compare <b>monitoring coverage</b> across different regions.  
            </p>

            <h4 style='color: #33C3FF;'>3️⃣ Area Type Distribution</h4>
            <p style='font-size: 18px;'>
                - A <b>pie chart</b> displaying pollution data by <b>area type</b>: <br> 
                🏭 <b>Industrial Areas</b>,<br> 🏡 <b>Residential Areas</b>,<br> 🏥 <b>Sensitive Areas</b>,<br> 🌆 <b>Mixed Zones</b>.  
            </p>

            <h4 style='color: #33C3FF;'>4️⃣ SO₂ and NO₂ Overview Dashboard</h4>
            <p style='font-size: 18px;'>
                - Provides a <b>state-wise breakdown</b> of <b>SO₂ and NO₂ levels</b>.  
                - A <b>time-series graph</b> tracking the changes in <b>average SO₂ and NO₂ concentrations</b> over time.  
                - Focus on <b>specific regions</b> such as Andhra Pradesh, Telangana, and Maharashtra.  
            </p>

            <h4 style='color: #33C3FF;'>5️⃣ Interactive Map</h4>
            <p style='font-size: 18px;'>
                - A <b>geospatial visualization</b> of pollution levels across various locations.  
                - Highlights specific <b>cities and districts</b> where pollution levels are measured.  
                - Allows users to explore <b>regional air quality trends</b> with a dynamic interface.  
            </p>

            <h3 style='color: #D35400;'>💡 Additional Features</h3>

            <h4 style='color: #33C3FF;'>🤖 AI Chatbot Assistance</h4>
            <p style='font-size: 18px;'>
                - Need help navigating the dashboard? Ask our <b>AI-powered chatbot</b> for instant answers!  
                - Get quick insights on air pollution data and real-time AQI updates.  
            </p>

            <h4 style='color: #33C3FF;'>🎯 Quick Quiz</h4>
            <p style='font-size: 18px;'>
                - Test your knowledge about air pollution with our interactive <b>Quick Quiz</b>!  
                - Fun and engaging questions designed to raise awareness about environmental issues.  
            </p>

            <h4 style='color: #33C3FF;'>📝 Feedback Section</h4>
            <p style='font-size: 18px;'>
                - Share your thoughts! Let us know how we can improve your experience.  
                - Provide feedback on dashboard usability, data accuracy, and visualization enhancements.  
            </p>

            <h4 style='color: #33C3FF;'>📞 Contact Us</h4>
            <p style='font-size: 18px;'>
                - Have questions or suggestions? Reach out to us!  
                - <b>Email:</b> mshaw9753@gmail.com  
                - <b>Phone:</b> +918777714024  
            </p>

            <h3 style='color: #33C3FF;'>🛠️ Technology Stack</h3>
            <p style='font-size: 18px;'>
                🚀 <b>Power BI</b> for interactive visualizations.  
                ☁ <b>Microsoft Azure</b> for cloud-based data processing.  
                🗺 <b>TomTom & Microsoft Maps</b> for geospatial analysis.  
                🤖 <b>AI Chatbot</b> for instant assistance.  
            </p>

            <h3 style='color: #33C3FF;'>📌 Conclusion</h3>
            <p style='font-size: 18px; text-align: justify;'>
                The homepage serves as a <b>central dashboard</b> for assessing <b>air quality trends</b> and <b>regional pollution levels</b>.
                With an intuitive interface, users can explore key <b>pollution indicators</b>, compare data across states, and make informed decisions.
                Our interactive tools, AI chatbot, and real-time analytics ensure a seamless experience in understanding environmental data.  
            </p>
        """, unsafe_allow_html=True)