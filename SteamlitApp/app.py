import  streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import seaborn as sns
import altair as alt
import matplotlib.pyplot as plt
from shapely.geometry import Point
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Function to load the dataset
@st.cache_data  # Cache the function to enhance performance
def load_data():
    # Define the file path
    file_path = 'global_youtube_data_2023.csv'
    
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)

    # Drop irrelevant columns
    df = df[['Title', 'subscribers', 'video views', 'uploads', 'channel_type', 'created_year', 'lowest_monthly_earnings', 'highest_monthly_earnings', 'Country', 'Longitude', 'Latitude']]

    # Convert high numbers to more readable numbers
    df['subscribers_mio'] = df['subscribers'] / 1000000
    df['video_views_mio'] = df['video views'] / 1000000
    df['lowest_monthly_earnings_1000'] = df['lowest_monthly_earnings'] / 1000
    df['highest_monthly_earnings_1000'] = df['highest_monthly_earnings'] / 1000

    # Create bins for number of subscribers
    bin_edges = [0, 14, 18, 22, 26, 30, 300]
    bin_labels = ['< 14', '14-17.9', '18-21.9', '22-25.9', '26-29.9', '> 30']
    df['subscriberGroup_mio'] = pd.cut(df['subscribers_mio'], bins=bin_edges, labels=bin_labels, right=False)

    # Handling missing values
    median_year = df['created_year'].median()
    df['created_year'].fillna(median_year, inplace=True)

    type_mode = df['channel_type'].mode()[0]
    df['channel_type'].fillna(type_mode, inplace=True)

    country_mode = df['Country'].mode()[0]
    df['Country'].fillna(country_mode, inplace=True)

    longitude_mode = df['Longitude'].mode()[0]
    df['Longitude'].fillna(longitude_mode, inplace=True)

    latitude_mode = df['Latitude'].mode()[0]
    df['Latitude'].fillna(latitude_mode, inplace=True)

    return df

# Load the data using the defined function
df_full = load_data()

# Tile
st.title("Youtube Dashboard")

# Sidebar with filters
st.sidebar.header("Filters 📊")

# Apply filters to the dataset
df = df_full

# Introduction
st.markdown("""
            Welcome to the HR Attrition Dashboard. In the backdrop of rising employee turnovers, HR departments are stressing the significance of predicting and understanding employee departures. Through the lens of data analytics, this dashboard unveils the deeper causes of employee churn and proposes strategies to boost employee retention.
""")
with st.expander("📊 **Objective**"):
                 st.markdown("""
At the heart of this dashboard is the mission to visually decode data, equipping HR experts with insights to tackle these queries:
- Which company factions face a greater likelihood of employee exits?
- What might be pushing these individuals to part ways?
- Observing the discerned trends, what incentives might hold the key to decreasing the attrition rate?
"""
)
                             
# Selection box for analysis                                         
analysis_option = st.selectbox(
    "Select Analysis 📈",
    ["Top 10 biggest Youtubers by number of subscribers", 
     "Monthly earnings by number of subscribers",
     "Map of location of Youtubers",
     "Option 4", 
     "Option 5"]
)

# Content of page base on selection
if analysis_option == 'Top 10 biggest Youtubers by number of subscribers':
    st.subheader(analysis_option)

    temp = df.sort_values('subscribers', ascending=False)[:10]
    temp = temp[['subscribers_mio', 'Title', 'channel_type', 'video_views_mio', 'created_year', 'Country']]
    temp['video_views_mio'] = temp['video_views_mio'].round(0)
    temp['subscribers_mio'] = temp['subscribers_mio'].round(2)
    temp['created_year'] = temp['created_year'].astype(int)
    temp['created_year'] = temp['created_year'].astype(str)
    temp = temp.rename(columns={'Title': 'Youtuber', 
                                'channel_type': 'Type',
                                'subscribers_mio': 'Subscribers (mio)', 
                                'video_views_mio': 'Views (mio)', 
                                'created_year': 'Created year'})
    st.dataframe(temp, hide_index=True)

elif analysis_option == "Map of location of Youtubers":
    st.subheader(analysis_option)

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))
    gdf.crs = "EPSG:4326"
    gdf = gdf.to_crs("EPSG:4326")
    m = folium.Map(location=[47.6062, -122.3321], zoom_start=3, tiles="CartoDB positron")

    # Create a marker cluster
    marker_cluster = MarkerCluster().add_to(m)

    # Loop through each youtuber and add it as a circle on the map within the marker cluster
    for _, row in gdf.iterrows():
        # Creating a pop-up message with some key information about the incident
        popup_content = f"""
        Youtuber: {row['Title']}<br>
        Subscribers: {row['subscribers_mio']} million<br>
        Country: {row['Country']}<br>
        Highest monthly earnings: {row['highest_monthly_earnings']}<br>
        Lowest monthly earnings: {row['lowest_monthly_earnings']}<br>
        """
        popup = folium.Popup(popup_content, max_width=300)
                
        folium.Circle(
                location=[row['Latitude'], row['Longitude']],
                radius=15,
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.4,
                popup=popup
                ).add_to(marker_cluster)

    st_folium(m)

elif analysis_option == 'Monthly earnings by number of subscribers': 
    st.subheader(analysis_option) 

    # Boxplots for monthly earnings by number of subscribers
    fig, ax = plt.subplots(1, 2, figsize=(15, 7))

    # Lowest monthly earning by Subscribers
    sns.boxplot(x="subscriberGroup_mio", y="lowest_monthly_earnings_1000", data=df, ax=ax[1], palette='Set2')
    ax[1].set_title('Lowest monthly earnings by Subscribers')
    ax[1].set_xlabel('Subscribers, millions')
    ax[1].set_ylabel('Lowest monthly earnings, thousands')
    
    # Highest monthly earning by Subscribers
    sns.boxplot(x="subscriberGroup_mio", y="highest_monthly_earnings_1000", data=df, ax=ax[0], palette='Set2')
    ax[0].set_title('Highest monthly earnings by Subscribers')
    ax[0].set_xlabel('Subscribers, millions')
    ax[0].set_ylabel('Highest monthly earnings, thousands')
    
    plt.tight_layout()
    st.pyplot(fig)

elif analysis_option == 'Option 4': 
    st.subheader("Some chart")
    # Bar chart for channel type distribution
    chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('channel_type:N', title='Channel Type'),
    y=alt.Y('count():Q', title='Count'),
    color='channel_type:N').properties(
          title='Channel Type Distribution (Bar Chart)'
          )

    st.altair_chart(chart, use_container_width=True)

elif analysis_option == 'Option 5': 
    st.subheader("Some other chart")
    # Pie chart for channel type distribution
    chart = alt.Chart(df).mark_arc().encode(
    color='channel_type:N',
    theta='count:Q',
    tooltip=['channel_type:N', 'count:Q']).properties(
         title='Channel Type Distribution (Pie Chart)'
         )

    st.altair_chart(chart, use_container_width=True)

else: 
    st.subheader("I'm not done yet")




