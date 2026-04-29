import streamlit as st 
import pandas as pd 
import altair as alt

olympics_df = pd.read_csv("data/processed/olympics_cleaned.csv")
top_country_medals_df = pd.read_csv("data/processed/top_country_medals.csv")
top_country_medal_points_df = pd.read_csv("data/processed/top_country_medal_points.csv")
medal_trends_df = pd.read_csv("data/processed/medal_trends.csv")
country_top_sport_df = pd.read_csv("data/processed/country_top_sport.csv")
specialized_countries_df = pd.read_csv("data/processed/specialized_countries.csv")

st.set_page_config(
  page_title = "Olympic Performance Analyzer", 
  layout = "wide",
)

st.title("Olympic Performance Analyzer")
st.write("Olympic medal trends, country performance and sport specialization using historical athlete and medal data.")
st.sidebar.title("Filters")

st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Medal Records", len(olympics_df),border = True)
col2.metric("Countries", olympics_df['NOC'].unique().size, border = True)
col3.metric("Sports", olympics_df['Sport'].unique().size, border = True )
col4.metric("Year Range", f"{olympics_df['Year'].min()} - {olympics_df['Year'].max()}", border = True)


st.subheader("Country Medal Rankings")

top_medals_chart_df = top_country_medals_df.sort_values(by="0", ascending=False).head(10)
top_medal_points_chart_df = top_country_medal_points_df.sort_values(by="Medal_Points", ascending = False).head(10)


st.write("Top Countries by Total Medals")
top_medal_chart = alt.Chart(top_medals_chart_df).mark_bar().encode(x = alt.X("NOC", sort = None, title = "Country (NOC)"), y = alt.Y("0", title = "Number of Medals"))
st.altair_chart(top_medal_chart, use_container_width= True)

st.write("Top Countries by Medal Points")
top_medal_points_chart = alt.Chart(top_medal_points_chart_df).mark_bar().encode(x = alt.X("NOC", sort = None, title="Country (NOC)"), y = alt.Y("Medal_Points", title="Medal Points"))
st.altair_chart(top_medal_points_chart, use_container_width=True)

st.write("Medal Trends Over Time")
st.write("Sport Specialization")