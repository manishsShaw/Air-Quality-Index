import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
import plotly.express as px


@st.cache_data
def load_data():
    file_path = "Compressed_India_Air_Quality_Data 3.csv"
    df = pd.read_csv(file_path)
    

    df['sampling_date'] = pd.to_datetime(df['sampling_date'], format='%d-%m-%Y', errors='coerce')
    

    df = df.dropna(subset=['sampling_date'])
    
    return df

def display_page1():

    df = load_data()

    st.sidebar.header("Filters")

    states = st.sidebar.multiselect("Select State", df['State'].dropna().unique(), key = "page1_states_select")


    df_filtered = df.copy()
    if states:
        df_filtered = df_filtered[df_filtered['State'].isin(states)]

    # Debugging Output
    st.sidebar.write("🔍 *Filtered Data Shape:*", df_filtered.shape)
    if not df_filtered.empty:
        st.sidebar.write("✅ *Sample Data:*", df_filtered[['State', 'sampling_date', 'agency', 'Area Type', 'location_monitoring_station', 'so2', 'no2', 'rspm', 'spm']].drop_duplicates())


    tab1, = st.tabs(["📊 Overview of Air Quality Index Visualization"])

    # Tab 1: Overview with Metric Cards
    with tab1:
        if not df_filtered.empty:
            st.subheader("📊 Key Air Quality Statistics")

            pollutants = ['so2', 'no2', 'rspm', 'spm']
            metrics = {'Sum': np.sum, 'Avg': np.mean, 'Max': np.max, 'Min': np.min}

            card_colors = ['#2E3B55', '#3A506B', '#5E81AC', '#4C566A']  # Dark theme colors

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

  

        
        
        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        # Clustered Bar Chart: States vs Count of Agencies
        st.subheader("📊 Count of Agencies per State")
        state_agency_count = df_filtered.groupby('State')['agency'].nunique().reset_index()
        state_agency_count = state_agency_count.sort_values(by='agency', ascending=False)

        
        if not states:
            top_states = state_agency_count.head(3)
        else:
            top_states = state_agency_count[state_agency_count['State'].isin(states)]

        fig, ax = plt.subplots(figsize=(10, 5))

        
        plt.style.use("dark_background")
        sns.barplot(x='State', y='agency', data=top_states, palette='Blues_r', ax=ax)

        ax.set_facecolor("#1E1E1E")  # Dark background for the chart
        ax.set_xlabel("State", fontsize=12, color='white')
        ax.set_ylabel("Count of Agencies", fontsize=12, color='white')
        ax.set_title("Top States by Agency Count", fontsize=14, color='white')
        
        ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

       
        def format_y_axis(value, _):
            return f"{value/1000:.1f}K" if value >= 1000 else f"{int(value)}"

        ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_y_axis))
        
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_edgecolor('white')

        
        for p in ax.patches:
            ax.annotate(format_y_axis(p.get_height(), None), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='bottom', fontsize=11, color='white')

        st.pyplot(fig)

        
        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        # Donut Chart: Count of States by Area Type
        st.subheader("\U0001F4CA Distribution of Area Type")
        area_type_counts = df_filtered['Area Type'].value_counts()

        dark_colors = ['#3470a3', '#79abc9', '#ccdbea', '#4C566A']
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(area_type_counts, labels=area_type_counts.index, autopct='%1.1f%%', startangle=140, colors=dark_colors[:len(area_type_counts)], wedgeprops={'edgecolor': 'black'})

        for text in ax.texts:
            text.set_color('white')

        centre_circle = plt.Circle((0, 0), 0.70, fc='black')
        fig.gca().add_artist(centre_circle)
        
        ax.set_title("Distribution of Area Types")
        st.pyplot(fig)

        
        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        # Top 5 Polluted Cities
        st.subheader("🏙️ Top 5 Most Polluted Cities")
        city_pollution = df_filtered.groupby("City")[['so2', 'no2', 'rspm', 'spm']].mean().sum(axis=1).reset_index()
        city_pollution.columns = ["City", "Total Pollution"]
        city_pollution = city_pollution.sort_values(by="Total Pollution", ascending=False).head(5)

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="City", y="Total Pollution", data=city_pollution, palette=["#6A79F7", "#DC5038", "#EA4335", "#7EF964", "#89FE05"], ax=ax)
        ax.set_xlabel("City")
        ax.set_ylabel("Pollution Level")
        ax.set_title("Top 5 Most Polluted Cities")
        st.pyplot(fig)

       
        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        # Yearly Pollution Trend by Area Type
        st.subheader("📆 Pollution Trend by Area Type Over the Years")

        df_filtered['Year'] = df_filtered['sampling_date'].dt.year
        area_trend = df_filtered.groupby(["Year", "Area Type"])[['so2', 'no2', 'rspm', 'spm']].mean().reset_index()
        area_trend["Total Pollution"] = area_trend[['so2', 'no2', 'rspm', 'spm']].sum(axis=1)

        fig = px.line(
            area_trend,
            x="Year",
            y="Total Pollution",
            color="Area Type",
            markers=True,
            template="plotly_dark",
            title="Yearly Pollution Trend by Area Type"
        )

        
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=40),
            xaxis_title="Year",
            yaxis_title="Total Pollution",
            width=None,  
            height=None  
        )

        st.plotly_chart(fig, use_container_width=True)

        
