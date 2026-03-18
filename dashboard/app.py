# ================================
# 📊 Tech Layoff Intelligence Dashboard
# ================================

# ----------- IMPORTS -----------
import streamlit as st
import pandas as pd
import plotly.express as px

# ----------- PAGE CONFIG -----------
st.set_page_config(page_title="Tech Layoff Dashboard", layout="wide")

# ----------- CUSTOM STYLING -----------
st.markdown("""
<style>
div[data-baseweb="select"] > div {
    border-color: #4CAF50 !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #4CAF50 !important;
    box-shadow: 0 0 0 1px #4CAF50 !important;
}
</style>
""", unsafe_allow_html=True)

# ----------- TITLE -----------
st.title("Tech Layoff Intelligence Dashboard")

st.markdown("""
Analyze global tech layoffs across industries, countries, and time.

Use filters to explore trends and insights.
""")

# ----------- LOAD DATA -----------
df = pd.read_csv("data/processed/layoffs_cleaned.csv")

# ----------- SIDEBAR FILTERS -----------
st.sidebar.header("🔍 Filters")

# Year filter
selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df['year'].dropna().unique())
)

# Country filter
selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df['country'].dropna().unique())
)

# Apply filters
filtered_df = df[df['year'] == selected_year]

if selected_country != "All":
    filtered_df = filtered_df[filtered_df['country'] == selected_country]

# ----------- HEADER INFO -----------
st.subheader(f"Data for Year: {selected_year} | Country: {selected_country}")

# ================================
# 📊 KPI METRICS
# ================================

total_layoffs = filtered_df['total_laid_off'].sum()
total_companies = filtered_df['company'].nunique()

col1, col2 = st.columns(2)

col1.metric("Total Layoffs", f"{int(total_layoffs):,}")
col2.metric("Total Companies", total_companies)

st.markdown("---")

# ================================
# 📊 INDUSTRY ANALYSIS
# ================================

st.subheader("Industry Analysis")

industry = (
    filtered_df
    .groupby('industry')['total_laid_off']
    .sum()
    .reset_index()
    .sort_values(by='total_laid_off', ascending=False)
    .head(10)
)

fig1 = px.bar(
    industry,
    x='industry',
    y='total_laid_off',
    title="Top Industries by Layoffs",
    color='total_laid_off',
    color_continuous_scale='Blues'
)

fig1.update_layout(
    xaxis_tickangle=-45,
    template='plotly_dark'
)

# ================================
# 📉 TIME SERIES ANALYSIS
# ================================

monthly = (
    filtered_df
    .groupby(['year', 'month'])['total_laid_off']
    .sum()
    .reset_index()
)

monthly['date'] = pd.to_datetime(monthly[['year', 'month']].assign(day=1))

fig2 = px.line(
    monthly,
    x='date',
    y='total_laid_off',
    title="Layoffs Over Time",
    markers=True
)

fig2.update_layout(template='plotly_dark')

# ================================
# 🌍 COUNTRY ANALYSIS (NEW)
# ================================

country_data = (
    filtered_df
    .groupby('country')['total_laid_off']
    .sum()
    .reset_index()
    .sort_values(by='total_laid_off', ascending=False)
    .head(10)
)

fig3 = px.bar(
    country_data,
    x='country',
    y='total_laid_off',
    title="Top Countries by Layoffs",
    color='total_laid_off',
    color_continuous_scale='Reds'
)

fig3.update_layout(
    xaxis_tickangle=-45,
    template='plotly_dark'
)

# ================================
# 🏢 STAGE ANALYSIS (NEW)
# ================================

stage_data = (
    filtered_df
    .groupby('stage')['percentage_laid_off']
    .mean()
    .reset_index()
    .sort_values(by='percentage_laid_off', ascending=False)
)

fig4 = px.bar(
    stage_data,
    x='stage',
    y='percentage_laid_off',
    title="Avg Layoff % by Company Stage",
    color='percentage_laid_off',
    color_continuous_scale='Purples'
)

fig4.update_layout(
    xaxis_tickangle=-45,
    template='plotly_dark'
)

# ================================
# 📊 DISPLAY SECTION
# ================================

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

# Row 2
col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.plotly_chart(fig4, use_container_width=True)