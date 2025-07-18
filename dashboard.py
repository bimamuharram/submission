# Menyiapkan DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


## create_byseason_df untuk menyiapkan byseason_df
def create_byseason_df(df):
    byseason_df = df.groupby(by="season").cnt.mean().reset_index()
    byseason_df.rename(columns={
        "cnt": "avg_count",
    }, inplace=True)

    return byseason_df

## create bymonth_df untuk menyiapkan bymonth_df
def create_bymonth_df(df):
    bymonth_df = df.groupby(by="mnth").cnt.mean().reset_index()
    bymonth_df.rename(columns={
        "cnt": "avg_count",
    }, inplace=True)

    return bymonth_df

## create byday_df untuk menyiapkan byday_df
def create_byday_df(df):
    byday_df = df.groupby(by="weekday").cnt.mean().reset_index()
    byday_df.rename(columns={
        "cnt": "avg_count",
    }, inplace=True)

    return byday_df

## create byhour_df untuk menyiapkan byhour_df
def create_byhour_df(df):
    byhour_df = df.groupby(by="hr").cnt.mean().reset_index()
    byhour_df.rename(columns={
        "cnt": "avg_count",
    }, inplace=True)

    return byhour_df

## create byweather_df untuk menyiapkan byweather_df
def create_byweather_df(df): df.groupby(by="weathersit").cnt.mean().reset_index()

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

byseason_df = create_byseason_df(day_df)
bymonth_df = create_bymonth_df(day_df)
byday_df = create_byday_df(day_df)
byweather_df = create_byweather_df(day_df)
byhour_df = create_byhour_df(hour_df)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header("Proyek Analisis Data: Bike Sharing Dataset Dashboard")

st.subheader("Average Number of Rental Bikes")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Optimal Season", value="Spring")

with col2:
    st.metric(label="Optimal Month", value="Jun to Sep")

with col3:
    st.metric(label="Optimal Day", value="Saturday")

with col4:
    st.metric(label="Optimal Hour", value="Rush Hour")

## Average Number of Rental Bikes by Season

season_dict = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_order = ["Spring", "Summer", "Fall", "Winter"]

byseason_df["season_name"] = byseason_df["season"].map(season_dict)

fig, ax = plt.subplots(figsize=(15, 5))
colors = ["#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3"]
sns.barplot(
    x="season_name",
    y="avg_count",
    data=byseason_df,
    order=season_order,
    palette=colors,
    ax=ax
)

ax.set_title("Average Number of Rental Bikes by Season in 2011 and 2012")
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

## Average Number of Rental Bikes by Month

import calendar

bymonth_df["month_name"] = bymonth_df["mnth"].apply(lambda x: calendar.month_name[x])

fig, ax = plt.subplots(figsize=(15, 5))
plt.plot(
    bymonth_df["month_name"],
    bymonth_df["avg_count"],
    marker="o",
    color="#72BCD4"
)

ax.set_title("Average Number of Rental Bikes by Month in 2011 and 2012")
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

## Average Number of Rental Bikes by Day

import calendar

byday_df["day_name"] = byday_df["weekday"].apply(lambda x: calendar.day_name[x])

fig, ax = plt.subplots(figsize=(15, 5))
plt.plot(
    byday_df["day_name"],
    byday_df["avg_count"],
    marker="o",
    color="#72BCD4"
)

ax.set_title("Average Number of Rental Bikes by Day in 2011 and 2012")
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

## Average Number of Rental Bikes by Hour

fig, ax = plt.subplots(figsize=(15, 5))
plt.plot(
    byhour_df["hr"],
    byhour_df["avg_count"],
    marker="o",
    color="#72BCD4"
)

ax.set_title("Average Number of Rental Bikes by Hour in 2011 and 2012")
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

## Average Number of Rental Bikes by Daily Weather

fig, ax = plt.subplots(figsize=(15, 5))
sns.barplot(
    x="weathersit",
    y="cnt",
    data=day_df,
    palette=["#72BCD4", "#D3D3D3", "#D3D3D3"],
    ci=None,
    ax=ax
)

ax.set_title("Average Number of Rental Bikes by Daily Weather in 2011 and 2012")
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_xticklabels(["Clear", "Mist", "Light Rain"])
st.pyplot(fig)