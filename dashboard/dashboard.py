import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by="hr").agg({
        "registered": "sum",
        "casual": "sum",
        "cnt": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    
    return daily_rent_df

def create_hour_group_df(df):
    hour_group_df = df.groupby(by="hr_group").cnt.sum()
    hour_group_df = hour_group_df.reset_index()

    return hour_group_df

def create_total_season_df(df):
    total_season_df = df.groupby(by="season").agg({
        "cnt": "sum"
    })
    return total_season_df

# Load cleaned data
data_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]

for column in datetime_columns:
  data_df[column] = pd.to_datetime(data_df[column])

# Filter data
min_date = data_df["dteday"].min()
max_date = data_df["dteday"].max()
 
with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = data_df[(data_df["dteday"] >= str(start_date)) & 
                (data_df["dteday"] <= str(end_date))]

st.header('Bike Sharing Dashboard')
st.subheader('Hourly rent')

daily_rent_df = create_daily_rent_df(main_df)
hour_group_df = create_hour_group_df(main_df)
total_season_df = create_total_season_df(main_df)

col1, col2, col3 = st.columns(3)

with col1:
    total_casual = daily_rent_df.casual.sum()
    st.metric("Total casual", value=total_casual)

with col2:
    total_registered = daily_rent_df.registered.sum()
    st.metric("Total registered", value=total_registered)

with col3:
    total_rent = daily_rent_df.cnt.sum()
    st.metric("Total rent", value=total_rent)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df["hr"],
    daily_rent_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xticks(daily_rent_df["hr"])
ax.set_xlabel("Hour", fontsize=20, labelpad=10)
 
st.pyplot(fig)

st.subheader('Number of Rent')
colors = ['#FF9999', '#72BCD4', '#FFD700']  
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(
    y="cnt", 
    x="hr_group",
    data=hour_group_df,
    ax=ax[0],
    palette=colors
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hour Group", fontsize=30, labelpad=10)
ax[0].set_title("By Hour Group", loc="center", fontsize=50)
ax[0].tick_params(axis='x', labelsize=35)
ax[0].tick_params(axis='y', labelsize=30)

handles = [
    plt.Line2D([0], [0], color=colors[0], lw=10, label='Midday (11 AM - 5 PM)'),
    plt.Line2D([0], [0], color=colors[1], lw=10, label='Morning (3 AM - 10 AM)'),
    plt.Line2D([0], [0], color=colors[2], lw=10, label='Night (6 PM - 2 AM)')
]
ax[0].legend(handles=handles, loc='upper right', fontsize=20)

sns.barplot(x="season", y="cnt", data=total_season_df, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Season", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("By Season", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)


st.pyplot(fig)