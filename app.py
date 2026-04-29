import streamlit as st 
import pandas as pd 
import altair as alt
from vega_datasets import data
import plotly.express as px

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

map_df = pd.merge(top_country_medals_df, top_country_medal_points_df, on="NOC")
map_df = map_df.rename(columns={"0": "Total Medals", "Medal_Points": "Medal Points"})

map_df["Map_Code"] = map_df["NOC"]

noc_to_iso = {
  "GER": "DEU",
  "SUI": "CHE",
  "NED": "NLD",
  "DEN": "DNK",
  "POR": "PRT",
  "MAS": "MYS",
  "INA": "IDN",
  "IRI": "IRN",
  "KSA": "SAU",
  "KUW": "KWT",
  "ALG": "DZA",
  "RSA": "ZAF",
  "CRO": "HRV",
  "SLO": "SVN",
  "GRE": "GRC",
  "BUL": "BGR",
  "LAT": "LVA",
  "URS": "RUS",
  "EUN": "RUS",
  "ROC": "RUS",
  "GDR": "DEU",
  "FRG": "DEU",
  "TCH": "CZE",
  "YUG": "SRB",
  "SCG": "SRB",
  "BOH": "CZE",
  "ANZ": "AUS",
  "CHI": "CHL",
  "BAH": "BHS",
  "BAR": "BRB",
  "BER": "BMU",
  "BOT": "BWA",
  "BRN": "BHR",
  "CRC": "CRI",
  "ESA": "SLV",
  "HAI": "HTI",
  "LIB": "LBN",
  "MGL": "MNG",
  "NGR": "NGA",
  "NIG": "NER",
  "PUR": "PRI",
  "SRI": "LKA",
  "TAN": "TZA",
  "UAE": "ARE",
  "VIE": "VNM",
  "ZAM": "ZMB",
  "ZIM": "ZWE",
}

map_df["Map_Code"] = map_df["Map_Code"].replace(noc_to_iso)

map_fig = px.choropleth(map_df, locations = "Map_Code", color = "Total Medals", hover_data=  ["NOC", "Total Medals", "Medal Points"], projection = "equirectangular", color_continuous_scale=["#2f2f2f", "#d9d9d9"])
map_fig.update_layout(height=600, paper_bgcolor = "#0e1117", plot_bgcolor = "#0e1117", font = dict(color="white"))
map_fig.update_geos(showland = True, landcolor = "gray", showcountries = True, countrycolor = "white", showocean= True, oceancolor = "#0e1117", bgcolor = "#0e1117")

st.plotly_chart(map_fig, use_container_width=True, config = {"displayModeBar": False})

st.subheader("Country Medal Rankings")

top_medals_chart_df = top_country_medals_df.sort_values(by="0", ascending=False).head(10)
top_medal_points_chart_df = top_country_medal_points_df.sort_values(by="Medal_Points", ascending = False).head(10)

st.write("Top Countries by Total Medals")
top_medal_chart = alt.Chart(top_medals_chart_df).mark_bar().encode(x = alt.X("NOC", sort = None, title = "Country (NOC)"), y = alt.Y("0", title = "Number of Medals"))
st.altair_chart(top_medal_chart, use_container_width= True)

st.write("Top Countries by Medal Points")
top_medal_points_chart = alt.Chart(top_medal_points_chart_df).mark_bar().encode(x = alt.X("NOC", sort = None, title="Country (NOC)"), y = alt.Y("Medal_Points", title="Medal Points"))
st.altair_chart(top_medal_points_chart, use_container_width=True)

st.subheader("Top Sports by Medals")

top_sports_df = olympics_df.groupby('Sport')['Medal'].size().sort_values(ascending=False).head(10).reset_index(name="Medal_Count")
top_sports_chart = alt.Chart(top_sports_df).mark_bar().encode(x= alt.X("Sport", sort=None, title="Sport"), y= alt.Y("Medal_Count", title="Number of Medals"))
st.altair_chart(top_sports_chart, use_container_width=True)

st.subheader("Medal Trends Over Time")
medal_trends_chart = alt.Chart(medal_trends_df).mark_line().encode(x= alt.X("Year", sort=None), y = alt.Y("Number of Medals"))
st.altair_chart(medal_trends_chart, use_container_width=True)

st.subheader("Sport Specialization")
st.write("The specialization score shows what share of a country’s medals came from its strongest sport. Countries with less than 10 total medals were filtered out.")
st.write(specialized_countries_df)