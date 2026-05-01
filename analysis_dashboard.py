import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import re
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="EV Trends Analysis & Forecasting System",
    page_icon="📈",
    layout="wide"
)

# Premium Styling
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    h1, h2, h3 { color: #58a6ff; font-family: 'Segoe UI', sans-serif; }
    .sidebar-header { text-align: center; color: #58a6ff; font-size: 20px; font-weight: bold; margin-bottom: 20px; border-bottom: 2px solid #58a6ff; }
    .report-box { background-color: #1c2128; padding: 15px; border-radius: 10px; border-left: 5px solid #58a6ff; color: #adbac7; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_name = "Electric_Vehicle_Population_Data.csv"
    possible_paths = [file_name, f"ev-data-analysis-main/{file_name}"]
    path = next((p for p in possible_paths if os.path.exists(p)), None)
    if not path:
        st.error("❌ Dataset not found.")
        st.stop()
    df = pd.read_csv(path, low_memory=False)
    
    def extract_coords(loc):
        try:
            if pd.isna(loc): return None, None
            vals = re.findall(r"[-+]?\d*\.\d+|\d+", str(loc))
            if len(vals) >= 2: return float(vals[1]), float(vals[0])
        except: pass
        return None, None

    if 'Vehicle Location' in df.columns:
        coords = df['Vehicle Location'].apply(extract_coords)
        df['latitude'] = [c[0] for c in coords]
        df['longitude'] = [c[1] for c in coords]
    return df

def main():
    st.title("📈 EV Trends Analysis & Forecasting System")
    df = load_data()

    # --- SIDEBAR FILTERS ---
    st.sidebar.markdown('<div class="sidebar-header">EV TRENDS SYSTEM</div>', unsafe_allow_html=True)
    with st.sidebar:
        st.header("🔍 Trend Filters")
        selected_counties = st.multiselect("Region", sorted(df['County'].dropna().unique()))
        selected_makes = st.multiselect("Manufacturer", sorted(df['Make'].unique()))
        ev_type = st.radio("EV Technology", ["All"] + list(df['Electric Vehicle Type'].unique()))

    # Apply Filters
    f_df = df.copy()
    if selected_counties: f_df = f_df[f_df['County'].isin(selected_counties)]
    if selected_makes: f_df = f_df[f_df['Make'].isin(selected_makes)]
    if ev_type != "All": f_df = f_df[f_df['Electric Vehicle Type'] == ev_type]

    # --- TABS ---
    t1, t2, t3, t4 = st.tabs(["📊 Performance & Forecasting", "🌍 Geo Analysis", "📈 Growth Trends", "📄 Explorer"])

    with t1:
        # Metrics Header
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Current Population", f"{len(f_df):,}")
        m2.metric("Avg Range", f"{f_df['Electric Range'].mean():.1f} mi")
        m3.metric("Dominant Make", f_df['Make'].mode()[0] if not f_df.empty else "N/A")
        m4.metric("Model Variety", f"{f_df['Model'].nunique()}")

        st.divider()

        # 1. RANGE FORECASTING (UPGRADED)
        st.subheader("🔮 2030 Performance Forecast")
        range_trend = f_df.groupby('Model Year')['Electric Range'].mean().reset_index()
        range_trend = range_trend[range_trend['Model Year'] > 2010]
        if len(range_trend) > 2:
            z = np.polyfit(range_trend['Model Year'], range_trend['Electric Range'], 1)
            p = np.poly1d(z)
            fy = np.array([2024, 2025, 2026, 2027, 2028, 2029, 2030])
            fr = p(fy)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=range_trend['Model Year'], y=range_trend['Electric Range'], name='Historical Range', line=dict(color='#58a6ff', width=4)))
            fig.add_trace(go.Scatter(x=fy, y=fr, name='2030 Forecast', line=dict(color='#00ff88', dash='dash', width=3)))
            fig.update_layout(template="plotly_dark", title="Avg Electric Range Projection")
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # 2. BRAND PERFORMANCE MATRIX (NEW)
        st.subheader("📊 Manufacturer Performance Matrix")
        c1, c2 = st.columns(2)
        with c1:
            top_perf = f_df.groupby('Make')['Electric Range'].mean().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(top_perf, x='Electric Range', y='Make', orientation='h', color='Electric Range', 
                         template="plotly_dark", title="Top 10 Tech Leaders (Avg Range)")
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            diversity = f_df.groupby('Make')['Model'].nunique().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(diversity, x='Model', y='Make', orientation='h', color='Model',
                         template="plotly_dark", title="Innovation Index (Model Variety)")
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # 3. PERFORMANCE DENSITY (NEW)
        st.subheader("🎯 Tech Maturity Density")
        fig = px.density_contour(f_df, x="Model Year", y="Electric Range", color="Electric Vehicle Type",
                                 template="plotly_dark", title="Range Evolution Density Map")
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        st.subheader("🌍 Advanced Geographic Analysis")
        map_mode = st.radio("Map Style", ["🔥 Heatmap", "📍 Points", "📊 Bubbles"], horizontal=True)
        map_df = f_df.dropna(subset=['latitude', 'longitude'])
        if not map_df.empty:
            if map_mode == "🔥 Heatmap":
                fig = px.density_mapbox(map_df, lat='latitude', lon='longitude', radius=10, zoom=6, mapbox_style="carto-darkmatter", template="plotly_dark")
            elif map_mode == "📍 Points":
                fig = px.scatter_mapbox(map_df.sample(min(len(map_df), 3000)), lat='latitude', lon='longitude', color="Make", zoom=6, mapbox_style="carto-darkmatter", template="plotly_dark")
            else:
                county_geo = map_df.groupby(['County', 'latitude', 'longitude']).size().reset_index(name='Count')
                fig = px.scatter_mapbox(county_geo, lat='latitude', lon='longitude', size='Count', color='Count', zoom=6, mapbox_style="carto-darkmatter", template="plotly_dark")
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=600)
            st.plotly_chart(fig, use_container_width=True)
            
        st.divider()

        # Regional Insights
        c3, c4 = st.columns(2)
        with c3:
            st.subheader("🏙️ Top 10 EV Cities")
            top_cities = f_df['City'].value_counts().head(10).reset_index()
            # Handle column name change in newer pandas
            city_col = top_cities.columns[0]
            val_col = top_cities.columns[1]
            fig = px.bar(top_cities, x=val_col, y=city_col, orientation='h', color=val_col, 
                         template="plotly_dark", title="City-wise Vehicle Density")
            st.plotly_chart(fig, use_container_width=True)
            
        with c4:
            st.subheader("🏛️ Legislative District Stats")
            if 'Legislative District' in f_df.columns:
                leg_dist = f_df['Legislative District'].value_counts().head(10).reset_index()
                dist_col = leg_dist.columns[0]
                cnt_col = leg_dist.columns[1]
                fig = px.pie(leg_dist, values=cnt_col, names=dist_col, hole=0.5,
                             template="plotly_dark", title="Top 10 Districts")
                st.plotly_chart(fig, use_container_width=True)

    with t3:
        st.subheader("📈 Adoption Growth Trends")
        c5, c6 = st.columns(2)
        with c5:
            # S-Curve
            top_5_makes = f_df['Make'].value_counts().head(5).index
            s_curve = f_df[f_df['Make'].isin(top_5_makes)].groupby(['Model Year', 'Make']).size().groupby(level=1).cumsum().reset_index(name='Total')
            fig = px.line(s_curve, x='Model Year', y='Total', color='Make', template="plotly_dark", title="Cumulative Adoption S-Curve")
            st.plotly_chart(fig, use_container_width=True)
            
        with c6:
            # YoY Growth
            yoy = f_df.groupby('Model Year').size().reset_index(name='Count')
            yoy['Growth %'] = yoy['Count'].pct_change() * 100
            fig = px.bar(yoy[yoy['Model Year'] > 2010], x='Model Year', y='Growth %', color='Growth %', 
                         template="plotly_dark", title="Market Velocity (YoY %)")
            st.plotly_chart(fig, use_container_width=True)
            
        st.divider()
        
        # Fleet Era
        st.subheader("📊 Fleet Maturity Composition")
        f_df['Era'] = pd.cut(f_df['Model Year'], bins=[1990, 2015, 2020, 2025], labels=['Early', 'Mass Market', 'Modern Pro'])
        era_df = f_df['Era'].value_counts().reset_index()
        era_df.columns = ['Era', 'Count']
        fig = px.pie(era_df, names='Era', values='Count', hole=0.5, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with t4:
        st.subheader("📄 Data Quality & Explorer")
        # Missing Data
        missing = f_df.isnull().sum().reset_index()
        missing.columns = ['Column', 'Missing']
        st.table(missing[missing['Missing'] > 0])
        
        st.divider()
        st.dataframe(f_df.head(1000), use_container_width=True)
        
        csv = f_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Filtered Data", data=csv, file_name='ev_data.csv', mime='text/csv')

if __name__ == "__main__":
    main()
