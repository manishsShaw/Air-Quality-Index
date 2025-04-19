import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


@st.cache_data
def load_data():
    file_path = "Compressed_India_Air_Quality_Data 3.csv"
    df = pd.read_csv(file_path)
    df['sampling_date'] = pd.to_datetime(df['sampling_date'], format='%d-%m-%Y', errors='coerce')
    df['Year'] = df['sampling_date'].dt.year  # Extract Year
    return df


def display_page2():
    df = load_data()

    
    st.sidebar.header("Filters")
    states = st.sidebar.multiselect("Select State", df['State'].dropna().unique(), key="page2_state_select")

    df_filtered = df.copy()
    if states:
        df_filtered = df_filtered[df_filtered['State'].isin(states)]
        
   
    st.sidebar.write("🔍 *Filtered Data Shape:*", df_filtered.shape)
    if not df_filtered.empty:
        st.sidebar.write("✅ *Sample Data:*", df_filtered[['State', 'so2', 'no2']].drop_duplicates())

    
    tab2, = st.tabs(["📊 Statewise Trends of SO₂ & NO₂ Emissions Over the Years"])
    
    with tab2:
        # Key Air Quality Statistics
        if not df_filtered.empty:
            st.subheader("📊 Key Air Quality Statistics")

            pollutants = ['so2', 'no2']
            metrics = {'Sum': np.sum, 'Avg': np.mean, 'Max': np.max, 'Min': np.min}

            card_colors = ['#4971ff','#595985']  # Dark theme colors

            def format_value(value):
                return f"{value/1000:.1f}K" if value >= 1000 else f"{value:.2f}"

            # Create metric cards  
            for pollutant, color in zip(pollutants, card_colors):
                cols = st.columns(4, gap="medium")  # Added space between cards
                for i, (metric_name, func) in enumerate(metrics.items()):
                    value = func(df_filtered[pollutant].dropna())
                    with cols[i]:
                        st.markdown(
                            f"""
                            <div style="background-color: {color}; padding: 20px; border-radius: 10px; text-align: center; 
                            color: white; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.6); min-height: 100px; display: flex; flex-direction: column; justify-content: center;">
                                <h3 style="margin:0; font-size: 22px;">{format_value(value)}</h3>
                                <p style="margin:0; font-weight: bold; font-size: 14px;">{metric_name} of {pollutant.upper()}</p>
                            </div>
                            """, unsafe_allow_html=True
                        )

        
        st.markdown("<br><hr>", unsafe_allow_html=True)

        # Donut Chart: Sum of NO₂ by State
        st.subheader("🛢️ NO₂ Pollution Distribution by State")

        if not df_filtered.empty:
            state_no2 = df_filtered.groupby("State")["no2"].sum().reset_index()

            dark_colors = ['#6A79F7', '#DC5035', '#8B0000', '#FFD700', '#00FA9A']

            fig, ax = plt.subplots(figsize=(4, 4))
            wedges, texts, autotexts = ax.pie(
                state_no2["no2"],
                labels=state_no2["State"],
                autopct='%1.1f%%',
                startangle=140,
                colors=dark_colors[:len(state_no2)],  # Use colors based on available data
                wedgeprops={'edgecolor': 'black'}
            )

            for text in texts + autotexts:
                text.set_color('white')

            centre_circle = plt.Circle((0, 0), 0.70, fc='black')
            fig.gca().add_artist(centre_circle)

            ax.set_title("Sum of NO₂ by State", color='white')

            st.pyplot(fig)

        
        st.markdown("<br><hr>", unsafe_allow_html=True)

        # Donut Chart for SO₂
        st.subheader("🛢️ SO₂ Pollution Distribution by State")

        if not df_filtered.empty:
            state_so2 = df_filtered.groupby("State")["so2"].sum().reset_index()

            dark_colors = ['#FF7F50', '#4682B4', '#9932CC', '#32CD32', '#FFD700']

            fig, ax = plt.subplots(figsize=(4, 4))
            wedges, texts, autotexts = ax.pie(
                state_so2["so2"],
                labels=state_so2["State"],
                autopct='%1.1f%%',
                startangle=140,
                colors=dark_colors[:len(state_so2)],  
                wedgeprops={'edgecolor': 'black'}
            )

            for text in texts + autotexts:
                text.set_color('white')

            centre_circle = plt.Circle((0, 0), 0.70, fc='black')
            fig.gca().add_artist(centre_circle)

            ax.set_title("Sum of SO₂ by State", color='white')

            st.pyplot(fig)

        
        st.markdown("<br><hr>", unsafe_allow_html=True)
        

        # Line Chart for SO₂ & NO₂ Trends Over Years
        st.subheader("📈 SO₂ & NO₂ Trends Over the Years")

        if not df_filtered.empty:
            
            selected_pollutants = st.multiselect(
                "Select Pollutants:",
                ["so2", "no2"],
                default=["so2", "no2"]
            )

            
            if selected_pollutants:
                filtered_chart_df = df_filtered.groupby("Year")[selected_pollutants].sum().reset_index()

                # Create Line Chart
                fig = px.line(
                    filtered_chart_df,
                    x="Year",
                    y=selected_pollutants,
                    markers=True,
                    title="SO₂ & NO₂ Trends Over the Years"
                )

                # Apply Dark Theme
                fig.update_layout(
                    template="plotly_dark",
                    margin=dict(l=20, r=20, t=40, b=20),
                    xaxis_title="Year",
                    yaxis_title="Level"
                )

                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Please select at least one pollutant to display the line chart.")
        else:
            st.warning("No data available for the selected state(s).")

