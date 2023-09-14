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
import random
from PIL import Image

# Function to load the dataset
@st.cache_data  # Cache the function to enhance performance
def load_data():
    # Define the file path
    file_path = path + 'global_youtube_data_2023.csv'
    
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)

    # Drop irrelevant columns
    df = df[['Title', 'subscribers', 'video views', 'uploads', 'channel_type', 'created_year', 'lowest_monthly_earnings', 'highest_monthly_earnings', 'Country', 'Longitude', 'Latitude']]

    # Convert high numbers to more readable numbers
    df['subscribers_M'] = df['subscribers'] / 1000000
    df['video_views_M'] = df['video views'] / 1000000
    df['lowest_monthly_earnings_1000'] = df['lowest_monthly_earnings'] / 1000
    df['highest_monthly_earnings_1000'] = df['highest_monthly_earnings'] / 1000

    # Create bins for number of subscribers
    bin_edges = [0, 14, 18, 22, 26, 30, 300]
    bin_labels = ['< 14', '14-17.9', '18-21.9', '22-25.9', '26-29.9', '> 30']
    df['subscriberGroup_M'] = pd.cut(df['subscribers_M'], bins=bin_edges, labels=bin_labels, right=False)

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

path = 'https://raw.githubusercontent.com/imads20/DashApps/main/YoutubersStreamlit/'

# Load the data using the defined function
df_full = load_data()

# Tile
st.title("YouTube Superstar Insights: Unleash the Data Dynamite! ✨💫🌟")

# Horizontal line - uff, look at that orange
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)

# Sidebar with filters
st.sidebar.header("Filters 📊")

# Sidebar filter: Country
selected_country = st.sidebar.multiselect("Select Country 🌏", df_full['Country'].unique().tolist(), default=None)
if not selected_country:
    selected_country = df_full['Country'].unique().tolist()

df = df_full[df_full['Country'].isin(selected_country)]

# Sidebar filter: Channel type
selected_type = st.sidebar.multiselect("Select Channel Type 📺", df_full['channel_type'].unique().tolist(), default=None)
if not selected_type:
    selected_type = df_full['channel_type'].unique().tolist()

df = df[df['channel_type'].isin(selected_type)]

# Sidebar filter: Subscriber range
min_subscribers = int(df_full['subscribers_M'].min())
max_subscribers = int(df_full['subscribers_M'].max())
subscriber_range = st.sidebar.slider("Select Subscriber Range (M) 💰", min_subscribers, max_subscribers, (min_subscribers, max_subscribers))
df = df[(df['subscribers_M'] >= subscriber_range[0]) & (df['subscribers_M'] <= subscriber_range[1])]

#Easter egg ;)
if st.button("Click me for a surprise! 🎊"):
    st.balloons()
    image = Image.open(path + "balloon.png")
    st.image(image, use_column_width=0.75)


# Introduction
st.markdown("""
            Welcome to the enchanting world of YouTube stardom, where this dazzling dataset unveils the juicy statistics of the biggest YouTube superstars. Picture it as the VIP backstage pass to the YouTube universe, where you can peek behind the curtain at the masterminds of online content.
            
            We've got the top dogs of YouTube in this dataset, complete with their subscriber counts, video views, upload frequencies, country of origin, and even their earnings. It's like having a secret decoder for YouTube success!
            
            So, whether you're a budding content creator seeking inspiration, a data wizard looking to decode the magic behind viral videos, or just someone fascinated by the ever-evolving world of online content, you're in for a wild ride. Dive headfirst into the YouTube cosmos, and let the data adventures begin!
""")
                             
jokes = ["Why did the data scientist go broke? Because he used up all his cache! 💸",
         "Parallel lines have so much in common... It's a shame they'll never meet. 📏",
         "Why did the scarecrow become a successful data scientist? Because he was outstanding in his field! 🌾",
         "Data scientists never sleep; they just enter a 'null' state. 😴",
         "Data science is all about turning 'hard data' into 'heartfelt' insights. 💖",
         "Why did the dashboard get an award? Because it had the 'metrics' for success! 🏆"
         "Why was the data analyst always calm under pressure? Because they knew how to 'plot' their way out of any situation! 📈",
         "Why did the dashboard win the race? Because it had the fastest data visualization! 🚀",
         "What did the dashboard say after winning the data competition? 'I'm on the data highway to success!' 🛣️",
         "Why did the dashboard get an award? Because it knew how to 'chart' a course to victory! 📊",
         "How did the dashboard become a champion? It had a 'winning formula' plotted in its data! 📈",
         "Why did the dashboard always come out on top? Because it had the 'data-savvy' to be a winner! 🥇"]
joke_memes = ['fun1.png', 
              'fun2.png', 
              'fun3.png', 
              'fun4.png', 
              'fun5.png', 
              'fun6.png']
if st.button("🥁 Time for a cheeky pun 🥁"):
    selected = random.choice(jokes)
    st.markdown(f'<p style="color: #FF1493;">{selected}</p>', unsafe_allow_html=True)
    
    image_name = random.choice(joke_memes)
    image = Image.open(path + image_name)
    st.image(image, use_column_width=0.75)


# Horizontal line - Feeling green-tastic today!
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #00FF00, #000000);">',
    unsafe_allow_html=True
)

# Overview of data
st.subheader("Top 10 Youtubers by Number of Subscribers 🥇")

temp = df.sort_values('subscribers', ascending=False)[:10]
temp = temp[['subscribers_M', 'Title', 'channel_type', 'video_views_M', 'created_year', 'Country']]
temp['video_views_M'] = temp['video_views_M'].round(0)
temp['subscribers_M'] = temp['subscribers_M'].round(2)
temp['created_year'] = temp['created_year'].astype(int)
temp['created_year'] = temp['created_year'].astype(str)
temp = temp.rename(columns={'Title': 'Youtuber', 
                            'channel_type': 'Type',
                            'subscribers_M': 'Subscribers (M)', 
                            'video_views_M': 'Views (M)', 
                            'created_year': 'Created year'})
st.dataframe(temp, hide_index=True)

with st.expander("Throwback to 2018: PewDiePie vs. T-Series"):
    image = Image.open(path + "pewLost.png")
    st.image(image, use_column_width=0.75)

# Horizontal line - You are looking blue-tiful!
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #0000FF, #000000);">',
    unsafe_allow_html=True
)

# Analysis
st.subheader("🚀 Let's Dive into Youtuber Metrics! 🎥")
                             
# Selection box for analysis                                         
analysis_option = st.selectbox(
    "Select Analysis 📈",
    ["Monthly earnings by number of subscribers",
     "Map of location of Youtubers",
     "Bar chart of channel type distribution", 
     "Pie chart of channel type distribution", 
     "Relationship between Number of Uploads and Views",
     ]
)

st.markdown(f'<h4 style="color: #333; font-weight: bold;">{analysis_option}</h4>', unsafe_allow_html=True)

# Content of page base on selection
if analysis_option == "Map of location of Youtubers":
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
        Subscribers: {row['subscribers_M']} million<br>
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
    # KDE distribution of monthly earnings compared to number of subscribers
    temp = df.rename(columns={'subscriberGroup_M': 'Subscribers (M)'})
    fig, ax = plt.subplots(1, 2, figsize=(15, 7))

    # Plot KDE distribution for lowest monthly earnings by Subscribers
    sns.kdeplot(data=temp, 
                x="lowest_monthly_earnings_1000", 
                hue="Subscribers (M)", 
                palette='Set2', 
                ax=ax[1])
    ax[1].set_title('KDE Distribution of Lowest Monthly Earnings by Subscribers')
    ax[1].set_xlabel('Lowest Monthly Earnings, thousands')
    ax[1].set_ylabel('Density')

    # Plot KDE distribution for highest monthly earnings by Subscribers
    sns.kdeplot(data=temp, 
                x="highest_monthly_earnings_1000", 
                hue="Subscribers (M)", 
                palette='Set2', 
                ax=ax[0])
    ax[0].set_title('KDE Distribution of Highest Monthly Earnings by Subscribers')
    ax[0].set_xlabel('Highest Monthly Earnings, thousands')
    ax[0].set_ylabel('Density')

    # Display the KDE plots in Streamlit
    st.pyplot(fig)

elif analysis_option == 'Bar chart of channel type distribution': 
    # Bar chart for channel type distribution
    temp = df.rename(columns={'channel_type': 'Channel Type'})
    chart = alt.Chart(temp).mark_bar().encode(
    x=alt.X('Channel Type:N', title='Channel Type'),
    y=alt.Y('count():Q', title='Count'),
    color='Channel Type:N'
    ).properties(
         title='Channel Type Distribution (Bar Chart)'
         )

    st.altair_chart(chart, use_container_width=True)

elif analysis_option == 'Pie chart of channel type distribution': 
    # Pie chart for channel type distribution
    temp = df[['channel_type']].value_counts().reset_index()
    temp = temp.rename(columns={'channel_type': 'Channel Type'})

    chart = alt.Chart(temp).mark_arc().encode(
        theta='count:Q',
        color='Channel Type:N',
        tooltip=['Channel Type', 'count']
    ).properties(
        title='Channel Type Distribution',
        width=300,
        height=300
    ).project('identity')

    st.altair_chart(chart, use_container_width=True)

elif analysis_option == 'Relationship between Number of Uploads and Views':
      fig, ax = plt.subplots()
      ax.scatter(df['uploads'], df['video views'], alpha=0.5)
      ax.set_xlabel('Number of Uploads')
      ax.set_ylabel('Number of Views')
      ax.set_title('Uploads vs. Views')
      
      st.pyplot(fig)

# Horizontal line - nice hot pink, huh?
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FF0066 20%, #000000 80%);">',
    unsafe_allow_html=True
)

# Random quotes to get us through it all (:
quotes = ["Data science: Where we spend 80% of our time cleaning data and the other 20% complaining about it 🙃", 
          "Data science is easy; it's like riding a bike. Except the bike is on fire, you're on fire, everything is on fire, and you're in hell 🥵", 
          "Data scientists make great detectives; we can find correlations between anything...except a social life 🙃",
          "Machine learning: Because 'I don't know what I'm doing' is just a fancy term for 'innovation 🤓'",
          "Data science is like magic, but instead of pulling a rabbit out of a hat, you pull insights out of a dataset 🪄",
          "In data science, we don't make mistakes; we have 'learning experiences' that help us improve skills 🚀",
          "Data scientists don't age; they just get replaced by newer models 😉",
          "Data scientists: Making sense of data one 'WTF?' at a time 🥵",
          "Data science is 90% data, 10% science, and 100% complaining about data quality 🫠",
          "If a data scientist solves a problem in a forest and no one is around to hear, did they even use Python? 🐍",]
if st.button("End the week with a data-tastic smile! 😎"):
    selected = random.choice(quotes)
    st.markdown(f'<p style="color: #0000FF;">{selected}</p>', unsafe_allow_html=True)


