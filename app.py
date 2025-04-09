import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page configuration
st.set_page_config(layout="wide", page_title="Malaysia Census Dashboard")

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

# Year filter (global)
year = st.selectbox("Year", [2020, 2021, 2022, 2023])

# Section 1: Summary metrics in a row
st.subheader("Summary")
col1, col2, col3, col4 = st.columns(4)

metric_icons = {
    "Blok Penghitungan": "🏙️",
    "Unit Bangunan": "🏢",
    "Tempat Kediaman": "🏘️",
    "Pertubuhan Perniagaan": "🏪"
}

with col1:
    st.markdown(f"### {metric_icons['Blok Penghitungan']} {summary_metrics['Blok Penghitungan']:,}")
    st.markdown("**Blok Penghitungan**")
    
with col2:
    st.markdown(f"### {metric_icons['Unit Bangunan']} {summary_metrics['Unit Bangunan']:,}")
    st.markdown("**Unit Bangunan**")
    
with col3:
    st.markdown(f"### {metric_icons['Tempat Kediaman']} {summary_metrics['Tempat Kediaman']:,}")
    st.markdown("**Tempat Kediaman**")
    
with col4:
    st.markdown(f"### {metric_icons['Pertubuhan Perniagaan']} {summary_metrics['Pertubuhan Perniagaan']:,}")
    st.markdown("**Pertubuhan Perniagaan**")

st.markdown("---")

# Section 2: Map view
st.subheader("Map View")

# Create a horizontal radio button for different metrics
metric_options = ["Blok Penghitungan", "Unit Bangunan", "Tempat Kediaman", "Pertubuhan Perniagaan"]
selected_metric = st.radio("Select Metric", metric_options, horizontal=True)

# Display map (simplified for this example)
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
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Section 3: Graph view
st.subheader("Graph View")

# Create two columns for graphs
graph_col1, graph_col2 = st.columns([3, 1])

with graph_col1:
    # Bar chart showing census blocks by state
    selected_graph_metric = st.radio(
        "Select metric for graph",
        ["Blok Penghitungan", "Unit Bangunan", "Tempat Kediaman", "Pertubuhan Perniagaan"],
        horizontal=True
    )
    
    # Create bar chart
    fig = px.bar(
        x=states,
        y=census_blocks,
        labels={"x": "State", "y": selected_graph_metric},
        title=f"{selected_graph_metric} by State ({year})"
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with graph_col2:
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
    
    st.caption(f"30 BP Split out of 10,000 BP for {selected_state} in Year {year}")

# Small footer with copyright info
st.markdown("---")
st.caption("© 2024 Jabatan Perangkaan Malaysia Hakcipta Terpelihara")
