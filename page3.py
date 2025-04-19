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
    df['Year'] = df['sampling_date'].dt.year  
    return df


def display_page3():
    df = load_data()

    # Sidebar filters
    st.sidebar.header("Filters")
    states = st.sidebar.multiselect("Select State", df['State'].dropna().unique(), key="page3_state_select")

    df_filtered = df.copy()
    if states:
        df_filtered = df_filtered[df_filtered['State'].isin(states)]
        
   
    
    st.sidebar.write("🔍 *Filtered Data Shape:*", df_filtered.shape)
    if not df_filtered.empty:
        st.sidebar.write("✅ *Sample Data:*", df_filtered[['State', 'rspm', 'spm']].drop_duplicates())
        
    
    tab3, = st.tabs(["📊 Statewise Trends of SPM & RSPM Emissions Over the Years"])
    
    with tab3:
        if not df_filtered.empty:
            st.subheader("📊 Key Air Quality Statistics")

            pollutants = ['rspm', 'spm']
            metrics = {'Sum': np.sum, 'Avg': np.mean, 'Max': np.max, 'Min': np.min}
            card_colors = ['#87df24', '#659574']

            def format_value(value):
                return f"{value/1000:.1f}K" if value >= 1000 else f"{value:.2f}"

            # Create metric cards  
            for pollutant, color in zip(pollutants, card_colors):
                cols = st.columns(4, gap="medium")
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

        # Donut Charts for RSPM & SPM
        for pollutant, title, colors in zip(
            ["rspm", "spm"], 
            ["🛢️ RSPM Pollution Distribution by State", "🛢️ SPM Pollution Distribution by State"], 
            [['#6A79F7', '#DC5035', '#8B0000', '#FFD700', '#00FA9A'],
             ['#FF7F50', '#4682B4', '#9932CC', '#32CD32', '#FFD700']]
        ):
            st.subheader(title)

            if not df_filtered.empty:
                state_pollutant = df_filtered.groupby("State")[pollutant].sum().reset_index()

                fig, ax = plt.subplots(figsize=(5, 5))
                wedges, texts, autotexts = ax.pie(
                    state_pollutant[pollutant],
                    labels=state_pollutant["State"],
                    autopct='%1.1f%%',
                    startangle=140,
                    colors=colors[:len(state_pollutant)],
                    wedgeprops={'edgecolor': 'black'}
                )

                
                for text in texts + autotexts:
                    text.set_color('white')  # Changed to black for better visibility

                centre_circle = plt.Circle((0, 0), 0.70, fc='black')  # White center for clarity
                fig.gca().add_artist(centre_circle)

                ax.set_title(f"Sum of {pollutant.upper()} by State", color='black')

                st.pyplot(fig)
            st.markdown("<br><hr>", unsafe_allow_html=True)

        # Line Chart for RSPM & SPM Trends Over Years
        st.subheader("📈 RSPM & SPM Trends Over the Years")

        if not df_filtered.empty:
            selected_pollutants = st.multiselect(
                "Select Pollutants:",
                ["rspm", "spm"],
                default=["rspm", "spm"]
            )

            if selected_pollutants:
                
                min_year, max_year = df_filtered["Year"].min(), df_filtered["Year"].max()
                all_years = pd.DataFrame({"Year": np.arange(min_year, max_year + 1)})

                
                filtered_chart_df = df_filtered.groupby("Year", as_index=False)[selected_pollutants].sum()

                
                filtered_chart_df = all_years.merge(filtered_chart_df, on="Year", how="left").fillna(0)

                # Create Line Chart
                fig = px.line(
                    filtered_chart_df,
                    x="Year",
                    y=selected_pollutants,
                    markers=True,
                    title="RSPM & SPM Trends Over the Years"
                )

                
                fig.update_xaxes(range=[min_year, max_year])

                
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
