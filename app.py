import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="IPL Player Analytics", layout="wide")
st.title("🏏 IPL Player Performance Analytics & Auction Value Predictor")
st.markdown("Explore player performance stats and predicted auction values from real IPL ball-by-ball data.")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("ipl_player_stats_final.csv")

player_stats = load_data()

# Sidebar filter
st.sidebar.header("Filters")
min_innings = st.sidebar.slider("Minimum innings played", 0, 50, 10)

filtered = player_stats[player_stats['innings_played'] >= min_innings]

# Top section: key metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Players", len(filtered))
col2.metric("Avg Performance Score", round(filtered['performance_score'].mean(), 1))
col3.metric("Avg Predicted Value (lakhs)", round(filtered['predicted_value'].mean(), 1))

# Top 10 players chart
st.subheader("Top 10 Players by Performance Score")
top10 = filtered.sort_values('performance_score', ascending=False).head(10)
st.bar_chart(top10.set_index('player')['performance_score'])

# Undervalued players table
st.subheader("Most Undervalued Players (High Performance-to-Value Ratio)")
undervalued = filtered.sort_values('value_ratio', ascending=False).head(10)
st.dataframe(undervalued[['player', 'performance_score', 'predicted_value', 'value_ratio']])

# Player search/comparison
st.subheader("🔍 Player Comparison Tool")
selected_players = st.multiselect("Select players to compare", filtered['player'].unique())
if selected_players:
    comparison = filtered[filtered['player'].isin(selected_players)]
    st.dataframe(comparison[['player', 'total_runs', 'strike_rate', 'wickets', 'economy_rate', 'performance_score']])
