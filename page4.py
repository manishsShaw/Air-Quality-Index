import streamlit as st
import matplotlib.pyplot as plt

def display_page4():
    def get_aqi_status(value):
        if value <= 50:
            return "Good", "#228B22", "images/good.png", "Air quality is considered satisfactory.", "✅ Enjoy the fresh air!"
        elif value <= 100:
            return "Moderate", "#DAA520", "images/moderate.png", "Air quality is acceptable, but some pollutants may be a concern.", "⚠️ Some pollutants may cause minor health issues."
        elif value <= 150:
            return "Unhealthy for Sensitive Groups", "#FF8C00", "images/unhealthy.png", "Sensitive groups may experience health effects.", "⚠️ Sensitive individuals should reduce prolonged outdoor activities."
        elif value <= 200:
            return "Unhealthy", "#B22222", "images/very-unhealthy.png", "Everyone may begin to experience health effects.", "❗ Consider reducing outdoor exposure."
        else:
            return "Hazardous", "#4B0082", "images/hazardous.png", "Health warnings of emergency conditions.", "🚨 Stay indoors and wear a mask if necessary."

    st.title("🌍 AQI Current Status")

    
    aqi = st.number_input("Enter AQI Value Manually", min_value=0, step=1, key="aqi_input")

    status, color, image_path, description, warning_message = get_aqi_status(aqi)

    
    st.markdown(f'<style>body {{ background-color: {color}; color: white; }}</style>', unsafe_allow_html=True)
    st.subheader(f"Status: {status}")
    st.write(f"**Health Effects:** {description}")

    
    try:
        st.image(image_path, caption=status, use_container_width=True)

    except FileNotFoundError:
        st.error("Image not found. Please check the file path.")

    st.warning(warning_message)

    # AQI Bar Chart Section
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader("📊 AQI Levels Bar Chart")

    categories = ["Good", "Moderate", "Unhealthy", "Very-Unhealthy", "Hazardous"]
    values = [50, 100, 150, 200, 300]
    colors = ["#228B22", "#DAA520", "#FF8C00", "#B22222", "#4B0082"]

    fig, ax = plt.subplots(facecolor="#222222")
    ax.bar(categories, values, color=colors)

    ax.set_facecolor("#222222")
    ax.spines["bottom"].set_color("white")
    ax.spines["left"].set_color("white")
    ax.tick_params(axis='x', colors='white', rotation=15)
    ax.tick_params(axis='y', colors='white')
    ax.title.set_color("white")
    ax.set_ylabel("AQI Threshold", color="white")

    st.pyplot(fig)  
