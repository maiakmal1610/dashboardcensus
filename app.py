import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page configuration
st.set_page_config(layout="wide", page_title="Landing Page HQ")

# Create sample data for Malaysian states
states = ['Selangor', 'W.P. Kuala Lumpur', 'Pulau Pinang', 'Johor', 'Pahang', 
          'Kelantan', 'Sarawak', 'Terengganu', 'Sabah', 'W.P. Putrajaya', 
          'Kedah', 'Perlis', 'W.P. Labuan']

# Create sample data for census blocks by state
census_blocks = [380, 320, 240, 240, 310, 350, 290, 290, 310, 270, 350, 370, 290]

# Create dummy data for the map
# In a real app, you'd use actual geospatial data
map_data = pd.DataFrame({
    'state': states,
    'census_blocks': census_blocks,
    'lat': [3.0738, 3.1390, 5.4141, 1.4927, 3.8126, 6.1254, 1.5533, 5.3302, 5.9804, 2.9264, 6.1184, 6.4432, 5.2831],
    'lon': [101.5183, 101.6869, 100.3288, 103.7414, 102.3398, 102.2382, 110.1592, 103.1408, 116.0735, 101.6964, 100.3685, 100.1982, 115.2308]
})

# Summary data
summary_metrics = {
    "Blok Penghitungan": 100000,
    "Unit Bangunan": 400000,
    "Tempat Kediaman": 2000000,
    "Pertubuhan Perniagaan": 20000
}

# Display title
st.title("Malaysia Census Dashboard")

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["Summary", "Map View", "Graph View"])

with tab1:
    # Summary metrics in a 2x2 grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Blok Penghitungan", f"{summary_metrics['Blok Penghitungan']:,}")
        st.metric("Tempat Kediaman", f"{summary_metrics['Tempat Kediaman']:,}")
    
    with col2:
        st.metric("Unit Bangunan", f"{summary_metrics['Unit Bangunan']:,}")
        st.metric("Pertubuhan Perniagaan", f"{summary_metrics['Pertubuhan Perniagaan']:,}")

with tab2:
    # Map view
    st.subheader("Map View")
    
    # Create a selectbox for different metrics
    metric_options = ["Blok Penghitungan", "Unit Bangunan", "Tempat Kediaman", "Pertubuhan Perniagaan"]
    selected_metric = st.selectbox("Select Metric", metric_options)
    
    # Year filter
    year = st.selectbox("Year", [2020, 2021, 2022, 2023])
    
    # Display map (simplified for this example)
    # In a real application, you would use actual map data for Malaysia
    fig = px.scatter_mapbox(
        map_data,
        lat="lat",
        lon="lon",
        size="census_blocks",
        color="census_blocks",
        hover_name="state",
        zoom=5,
        mapbox_style="carto-positron",
        title=f"Malaysia Census Data ({selected_metric})"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Graph view
    st.subheader("Graph View")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Bar chart showing census blocks by state
        selected_tab = st.radio(
            "Select metric",
            ["Blok Penghitungan", "Unit Bangunan", "Tempat Kediaman", "Pertubuhan Perniagaan"],
            horizontal=True
        )
        
        year_filter = st.select_slider("Year", options=[2020, 2021, 2022, 2023])
        
        # Create bar chart
        fig = px.bar(
            x=states,
            y=census_blocks,
            labels={"x": "State", "y": selected_tab},
            title=f"{selected_tab} by State ({year_filter})"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Donut chart for BP Split
        st.subheader("BP Split")
        
        # Create options for the donut chart
        state_options = ["Johor", "All States"]
        selected_state = st.selectbox("Select State", state_options)
        
        # Create donut chart
        fig = go.Figure(go.Pie(
            labels=["BP Split", ""],
            values=[30, 9970],
            hole=0.7,
            marker_colors=['#5edbca', '#e8f4f8']
        ))
        
        # Add annotation in the center
        fig.update_layout(
            annotations=[dict(text="0.003%", x=0.5, y=0.5, font_size=20, showarrow=False)],
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption(f"30 BP Split out of 10,000 BP for Johor in Year 2020")

# Small footer with copyright info
st.markdown("---")
st.caption("© 2024 Jabatan Perangkaan Malaysia Hakcipta Terpelihara")
