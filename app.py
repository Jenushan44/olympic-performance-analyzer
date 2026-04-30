import streamlit as st 
import pandas as pd 
import altair as alt
import plotly.express as px
from utils.country_mappings import noc_to_iso
import numpy as np

olympics_df = pd.read_csv("data/processed/olympics_cleaned.csv")
top_country_medals_df = pd.read_csv("data/processed/top_country_medals.csv")
top_country_medal_points_df = pd.read_csv("data/processed/top_country_medal_points.csv")
medal_trends_df = pd.read_csv("data/processed/medal_trends.csv")
country_top_sport_df = pd.read_csv("data/processed/country_top_sport.csv")
specialized_countries_df = pd.read_csv("data/processed/specialized_countries.csv")
noc_regions_df = pd.read_csv("data/raw/noc_regions.csv")

st.set_page_config(
  page_title = "Olympic Performance Analyzer", 
  layout = "wide",
)

st.markdown("""<style> .block-container {max-width: 1250px; margin: auto; padding-top: 2rem}; </style>""", unsafe_allow_html =True)

st.title("Olympic Performance Analyzer")
st.write("Olympic medal trends, country performance and sport specialization using historical athlete and medal data.")
st.sidebar.title("Filters")

st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Medal Records", len(olympics_df),border = True)
col2.metric("Countries", olympics_df['NOC'].unique().size, border = True)
col3.metric("Sports", olympics_df['Sport'].unique().size, border = True )
col4.metric("Year Range", f"{olympics_df['Year'].min()} - {olympics_df['Year'].max()}", border = True)

map_df = noc_regions_df[["NOC", "region"]].drop_duplicates()
map_df = map_df.merge(top_country_medals_df, on="NOC", how="left")
map_df = map_df.merge(top_country_medal_points_df, on="NOC", how= "left")

map_df = map_df.rename(columns={"region": "Country", "0": "Total Medals", "Medal_Points": "Medal Points"})
map_df["Total Medals"] = map_df["Total Medals"].fillna(0)
map_df["Medal Points"] = map_df["Medal Points"].fillna(0)


map_df["Map_Code"] = map_df["NOC"].replace(noc_to_iso)
map_df = map_df.dropna(subset=["Map_Code"])

map_df = map_df.groupby("Map_Code", as_index=False).agg({"Country":"first", "NOC": "first", "Total Medals": "sum", "Medal Points": "sum"})

map_df["Map_Medals"] = np.log1p(map_df["Total Medals"])
map_df["Medal Intensity"] = (map_df["Map_Medals"] / map_df["Map_Medals"].max()) * 10

map_fig = px.choropleth(map_df, locations = "Map_Code", locationmode="ISO-3", color = "Medal Intensity", hover_data=  ["Country", "NOC", "Total Medals", "Medal Points"], projection = "equirectangular", color_continuous_scale="Blues", range_color=(0, 10))
map_fig.update_layout(height=550, paper_bgcolor = "#0e1117", plot_bgcolor = "#0e1117", font = dict(color="white"), margin = dict(l=0, r = 0, t=0, b=0))
map_fig.update_geos(showland = True, landcolor = "gray", showcountries = True, countrycolor = "white", showocean= True, oceancolor = "#0e1117", bgcolor = "#0e1117", showframe = True, projection_scale = 1)
map_fig.update_coloraxes(colorbar_title = "", colorbar_tickvals = ["0", "2", "4", "6", "8","10"], colorbar_thickness=18, colorbar_len = 0.7, colorbar_y = 0.5, colorbar_ticklabelposition = "outside", colorbar_ticklabeloverflow = "allow")

st.plotly_chart(map_fig, use_container_width=True, config = {"displayModeBar": False, "scrollZoom": False})

st.markdown("<h2 style = 'text-align: center;' >Olympic Medal Rankings</h2>", unsafe_allow_html=True)
st.markdown("<p style = 'text-align: center; font-style: italic; font-size: 1rem; margin-top: -0.4rem; margin-bottom: 1.4rem;'>Compare Olympic performance by total medal count, weighted medal points and medal heavy sports.</p>", unsafe_allow_html=True)

top_medals_chart_df = top_country_medals_df.sort_values(by="0", ascending=False).head(10)
top_medal_points_chart_df = top_country_medal_points_df.sort_values(by="Medal_Points", ascending = False).head(10)

country_medal_rank_col1, country_medal_rank_col2 = st.columns(2)

with country_medal_rank_col1:
  st.markdown("<h4 style = 'text-align: center;'>Top 10 Countries by Total Medals</h4>", unsafe_allow_html=True)
  top_medal_chart = alt.Chart(top_medals_chart_df).mark_bar().encode(x = alt.X("0", title = "Number of Medals"), y = alt.Y("NOC", sort = None, title = "Country (NOC)"))
  st.altair_chart(top_medal_chart, use_container_width= True)

with country_medal_rank_col2:
  st.markdown("<h4 style = 'text-align: center;'>Top 10 Countries by Medal Points</h4>", unsafe_allow_html=True)
  top_medal_points_chart = alt.Chart(top_medal_points_chart_df).mark_bar().encode(x = alt.X("Medal_Points", title="Medal Points"), y = alt.Y("NOC", sort = None, title="Country (NOC)"))
  st.altair_chart(top_medal_points_chart, use_container_width=True)

st.markdown("<h4 style = 'text-align: center;'>Top 10 Sports by Medals</h4>", unsafe_allow_html=True)

top_sports_df = olympics_df.groupby('Sport')['Medal'].size().sort_values(ascending=False).head(10).reset_index(name="Medal_Count")
top_sports_chart = alt.Chart(top_sports_df).mark_bar().encode(x= alt.X("Medal_Count", title="Number of Medals"), y= alt.Y("Sport", sort=None, title="Sport"))
st.altair_chart(top_sports_chart, use_container_width=True)

st.markdown("<h2 style = 'text-align: center;' >Medal Trends Over Time</h2>", unsafe_allow_html=True)
st.markdown("<p style = 'text-align: center; font-style: italic; font-size: 1rem; margin-top: -0.4rem; margin-bottom: 1.4rem;'>Track Olympic medal counts over time, with recent changes showing the split between Summer and Winter Games.</p>", unsafe_allow_html=True)
medal_trends_chart = alt.Chart(medal_trends_df).mark_line().encode(x= alt.X("Year", sort=None), y = alt.Y("Number of Medals"))
st.altair_chart(medal_trends_chart, use_container_width=True)

st.markdown("<h2 style = 'text-align: center;'>Sport Specialization Rankings</h2>", unsafe_allow_html=True)
st.markdown("<p style = 'text-align: center; font-style: italic; font-size: 1rem; margin-top: -0.4rem; margin-bottom: 1.4rem;'>The specialization score shows what share of a country’s medals came from its strongest sport. Countries with less than 10 total medals were filtered out.</p>", unsafe_allow_html=True)

specialization_table_df = specialized_countries_df.copy()
specialization_table_df["Specialization_Score"] = specialization_table_df["Specialization_Score"].round(2)
specialization_table_df = specialization_table_df.rename(columns={"NOC": "Country (NOC)","Sport_Medal_Count": "Sport Medal Count", "Total_Country_Medals": "Total Country Medals", "Specialization_Score": "Specialization Score"})
st.dataframe(specialization_table_df, use_container_width = True, hide_index = True)