# Menyiapkan DataFrame
import pandas as pd
import streamlit as st
import plotly.express as px
import calendar

## create_byseason_df untuk menyiapkan byseason_df
def create_byseason_df(df):
    byseason_df = df.groupby(by="season").cnt.mean().reset_index()
    byseason_df.rename(columns={"cnt": "avg_count"}, inplace=True)
    return byseason_df

## create bymonth_df untuk menyiapkan bymonth_df
def create_bymonth_df(df):
    bymonth_df = df.groupby(by="mnth").cnt.mean().reset_index()
    bymonth_df.rename(columns={"cnt": "avg_count"}, inplace=True)
    return bymonth_df

## create byday_df untuk menyiapkan byday_df
def create_byday_df(df):
    byday_df = df.groupby(by="weekday").cnt.mean().reset_index()
    byday_df.rename(columns={"cnt": "avg_count"}, inplace=True)
    return byday_df

## create byhour_df untuk menyiapkan byhour_df
def create_byhour_df(df):
    byhour_df = df.groupby(by="hr").cnt.mean().reset_index()
    byhour_df.rename(columns={"cnt": "avg_count"}, inplace=True)
    return byhour_df

## create byweather_df untuk menyiapkan byweather_df
def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit").cnt.mean().reset_index()
    byweather_df.rename(columns={"cnt": "avg_count"}, inplace=True)
    return byweather_df

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Membuat Komponen Filter
year_option = st.sidebar.radio(
    "Select Year:",
    options=["All", 2011, 2012],
    index=0
)

year_map = {2011: 0, 2012: 1}

if year_option == "All":
    filtered_day_df = day_df
    filtered_hour_df = hour_df
else:
    selected_yr = year_map[year_option]
    filtered_day_df = day_df[day_df["yr"] == selected_yr]
    filtered_hour_df = hour_df[hour_df["yr"] == selected_yr]

byseason_df = create_byseason_df(filtered_day_df)
bymonth_df = create_bymonth_df(filtered_day_df)
byday_df = create_byday_df(filtered_day_df)
byweather_df = create_byweather_df(filtered_day_df)
byhour_df = create_byhour_df(filtered_hour_df)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header("Proyek Analisis Data: Bike Sharing Dataset Dashboard")

if year_option == "All":
    subheader_text = "Optimal Time of Rental Bikes in 2011 & 2012"
else:
    subheader_text = f"Optimal Time of Rental Bikes in {year_option}"

st.subheader(subheader_text)

col1, col2, col3, col4 = st.columns(4)

optimal_season = byseason_df.loc[byseason_df["avg_count"].idxmax(), "season"]
optimal_month = bymonth_df.loc[bymonth_df["avg_count"].idxmax(), "mnth"]
optimal_day = byday_df.loc[byday_df["avg_count"].idxmax(), "weekday"]
optimal_hour = byhour_df.loc[byhour_df["avg_count"].idxmax(), "hr"]

season_dict = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
month_dict = {i: calendar.month_abbr[i] for i in range(1, 13)}
day_dict = {i: calendar.day_name[i] for i in range(7)}

hour_label = f"{optimal_hour:2d}:00"

with col1:
    st.metric(label="Optimal Season", value=season_dict[optimal_season])
with col2:
    st.metric(label="Optimal Month", value=month_dict[optimal_month])
with col3:
    st.metric(label="Optimal Day", value=day_dict[optimal_day])
with col4:
    st.metric(label="Optimal Hour", value=hour_label)

year_label = " & ".join([str(y) for y in [2011, 2012]] if year_option == "All" else [str(year_option)])

## Average Number of Rental Bikes by Season
byseason_df["season_name"] = byseason_df["season"].map(season_dict)
max_val = byseason_df["avg_count"].max()
byseason_df["color"] = byseason_df["avg_count"].apply(lambda x: "#72BCD4" if x == max_val else "#D3D3D3")
fig_season = px.bar(
    byseason_df,
    x="season_name",
    y="avg_count",
    color="color",
    color_discrete_map="identity",
    title=f"Average Number of Rental Bikes by Season in {year_label}",
    labels={"season_name": "Season", "avg_count": "Average Number of Rental Bikes"},
    hover_data={"avg_count": ":,.0f"},
    category_orders={"season_name": ["Spring", "Summer", "Fall", "Winter"]}
)
fig_season.update_layout(showlegend=False)
st.plotly_chart(fig_season, use_container_width=True)

## Average Number of Rental Bikes by Month
bymonth_df["month_name"] = bymonth_df["mnth"].apply(lambda x: calendar.month_name[x])
fig_month = px.line(
    bymonth_df,
    x="month_name",
    y="avg_count",
    markers=True,
    title=f"Average Number of Rental Bikes by Month in {year_label}",
    labels={"month_name": "Month", "avg_count": "Average Number of Rental Bikes"}
)
st.plotly_chart(fig_month, use_container_width=True)

## Average Number of Rental Bikes by Day
byday_df["day_name"] = byday_df["weekday"].apply(lambda x: calendar.day_name[x])
fig_day = px.line(
    byday_df,
    x="day_name",
    y="avg_count",
    markers=True,
    title=f"Average Number of Rental Bikes by Day in {year_label}",
    labels={"day_name": "Day", "avg_count": "Average Number of Rental Bikes"}
)
st.plotly_chart(fig_day, use_container_width=True)

## Average Number of Rental Bikes by Hour
fig_hour = px.line(
    byhour_df,
    x="hr",
    y="avg_count",
    markers=True,
    title=f"Average Number of Rental Bikes by Hour in {year_label}",
    labels={"hr": "Hour", "avg_count": "Average Number of Rental Bikes"}
)
st.plotly_chart(fig_hour, use_container_width=True)

st.subheader(f"Daily Weather Influence on Rental Bikes in {year_label}")

## Average Number of Rental Bikes by Daily Weather
weather_labels = {1: "Clear", 2: "Mist", 3: "Light Rain"}
byweather_df["weather_label"] = byweather_df["weathersit"].map(weather_labels)
max_weather = byweather_df["avg_count"].max()
byweather_df["color"] = byweather_df["avg_count"].apply(lambda x: "#72BCD4" if x == max_weather else "#D3D3D3")
fig_weather = px.bar(
    byweather_df,
    x="weather_label",
    y="avg_count",
    color="color",
    color_discrete_map="identity",
    title=f"Average Number of Rental Bikes by Daily Weather in {year_label}",
    labels={"weather_label": "Weather", "avg_count": "Average Number of Rental Bikes"},
    hover_data={"avg_count": ":,.0f"}
)
fig_weather.update_layout(showlegend=False)
st.plotly_chart(fig_weather, use_container_width=True)

## Average Temperature, Humidity, and Windspeed by Daily Weather
df_weather_summary = filtered_day_df.copy()
df_weather_summary = df_weather_summary.groupby("weathersit").agg({
    "temp": lambda x: round(x.mean() * 41, 1),
    "atemp": lambda x: round(x.mean() * 50, 1),
    "hum": lambda x: round(x.mean() * 100, 1),
    "windspeed": lambda x: round(x.mean() * 67, 1),
}).reset_index()
df_weather_summary["weather_label"] = df_weather_summary["weathersit"].map(weather_labels)
df_weather_summary = df_weather_summary[["weather_label", "temp", "atemp", "hum", "windspeed"]]
df_weather_summary.columns = ["Weather", "Avg Temp (°C)", "Avg Feeling Temp (°C)", "Avg Humidity (%)", "Avg Wind Speed (km/h)"]

st.caption(f"Average Temperature, Humidity, and Windspeed by Daily Weather in {year_label}")
st.dataframe(df_weather_summary, use_container_width=True, hide_index=True)
