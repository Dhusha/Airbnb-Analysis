# Importing Libraries
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Setting up page configuration
icon = Image.open(r"C:\Users\tpsna\OneDrive\Desktop\VSCode\Airbnb_project\icn.png")
st.set_page_config(
    page_title="Airbnb Data Visualization | By Dhusha",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """# This dashboard app is created by *Dhusha*!"""})

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Home", "Overview", "Explore"],
        icons=["house", "graph-up-arrow", "bar-chart-line"],
        menu_icon="menu-button-wide",
        default_index=0,
        styles={
            "nav-link": {
                "font-size": "20px",
                "text-align": "left",
                "margin": "-2px",
                "--hover-color": "#FF5A5F",
            },
            "nav-link-selected": {"background-color": "#FF5A5F"},
        },
    )

# HOME PAGE
if selected == "Home":
    # Title and Introduction Section
    st.title(":red[Welcome to the Airbnb Data Insights Dashboard🏠]")
    
    # Dynamic Columns Layout
    col1, col2 = st.columns([2, 1], gap="medium")
    
    with col1:
        st.markdown("### :red[Domain]: Travel Industry, Property Management, and Tourism")
        st.markdown("### :red[Technologies Used]: Python, Pandas, Plotly, Streamlit")
        st.markdown(
            "### :red[Overview]: This project involves analyzing Airbnb data through comprehensive data cleaning and preparation, developing interactive visualizations, and creating dynamic plots. The goal is to uncover insights into pricing variations, availability patterns, and location-based trends."
        )
    with col2:
        st.image("C:/Users/tpsna/OneDrive/Desktop/VSCode/Airbnb_project/sideimage.jfif", caption="Explore the World of Airbnb Data")
    
    # Adding Interactive Elements
    st.markdown("---")
    st.markdown("### :red[Dive Deeper into the Data]")
    
    col3, col4, col5 = st.columns(3, gap="medium")
    
    with col3:
        if st.button("View Pricing Insights"):
            st.write("Explore the interactive visualization to see how pricing varies across different locations and times of the year.")
    
    with col4:
        if st.button("Check Availability Patterns"):
            st.write("Analyze availability trends to understand how occupancy rates fluctuate seasonally and geographically.")
    
    with col5:
        if st.button("Discover Location Trends"):
            st.write("Gain insights into popular areas and emerging hotspots by visualizing location-based trends in Airbnb listings.")

# OVERVIEW PAGE
if selected == "Overview":
    col1, col2 = st.columns(2)

        # Read the CSV file into a DataFrame
    df = pd.read_csv(r"C:\Users\tpsna\OneDrive\Desktop\VSCode\Airbnb_project\Airbnb_data.csv")

    # RAW DATA TAB
    with col1:
        if st.button("Click to view Raw data"):
            raw_data = pd.read_csv('Airbnb_data.csv.csv')
            st.write(raw_data)

        if st.button("Click to view DataFrame"):
            st.write(df)

#INSIGHTS TAB
    with col1:
        country = st.sidebar.multiselect('Select a Country', sorted(df['Country'].unique()), sorted(df['Country'].unique()))
        prop = st.sidebar.multiselect('Select Property Type', sorted(df['Property_type'].unique()), sorted(df['Property_type'].unique()))
        room = st.sidebar.multiselect('Select Room Type', sorted(df['Room_type'].unique()), sorted(df['Room_type'].unique()))
        price = st.slider('Select Price', df['Price'].min(), df['Price'].max(), (df['Price'].min(), df['Price'].max()))

        query = f"Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}"

    col1, col2 = st.columns(2, gap='medium')

    with col1:
        df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
        fig = px.bar(df1, title='Top 10 Property Types', x='Listings', y='Property_type', orientation='h', color='Property_type', color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

        df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
        fig = px.bar(df2, title='Top 10 Hosts with Highest number of Listings', x='Listings', y='Host_name', orientation='h', color='Host_name', color_continuous_scale=px.colors.sequential.Agsunset)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
        fig = px.pie(df1, title='Total Listings in each Room Types', names='Room_type', values='counts', color_discrete_sequence=px.colors.sequential.Rainbow)
        fig.update_traces(textposition='outside', textinfo='value+label')
        st.plotly_chart(fig, use_container_width=True)

        country_df = df.query(query).groupby(['Country'], as_index=False)['Name'].count().rename(columns={'Name': 'Total_Listings'})
        fig = px.choropleth(country_df, title='Total Listings in each Country', locations='Country', locationmode='country names', color='Total_Listings', color_continuous_scale=px.colors.sequential.Plasma)
        st.plotly_chart(fig, use_container_width=True)

# EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")
    
    df = pd.read_csv(r"C:\Users\tpsna\OneDrive\Desktop\VSCode\Airbnb_project\Airbnb_data.csv")

    country = st.sidebar.multiselect('Select a Country', sorted(df['Country'].unique()), sorted(df['Country'].unique()))
    prop = st.sidebar.multiselect('Select Property_type', sorted(df['Property_type'].unique()), sorted(df['Property_type'].unique()))
    room = st.sidebar.multiselect('Select Room_type', sorted(df['Room_type'].unique()), sorted(df['Room_type'].unique()))
    price = st.slider('Select Price', df['Price'].min(), df['Price'].max(), (df['Price'].min(), df['Price'].max()))
    
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    st.markdown("## Price Analysis")
    
    col1, col2 = st.columns(2, gap='medium')
    
    with col1:
        pr_df = df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(pr_df, x='Room_type', y='Price', color='Price', title='Avg Price in each Room type')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("## Availability Analysis")
        
        fig = px.box(df.query(query), x='Room_type', y='Availability_365', color='Room_type', title='Availability by Room_type')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        country_df = df.query(query).groupby('Country', as_index=False)['Price'].mean()
        fig = px.scatter_geo(country_df, locations='Country', color='Price', hover_data=['Price'], locationmode='country names', size='Price', title='Avg Price in each Country', color_continuous_scale='agsunset')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#   ")
        st.markdown("#   ")
        
        country_df = df.query(query).groupby('Country', as_index=False)['Availability_365'].mean()
        country_df['Availability_365'] = country_df['Availability_365'].astype(int)
        fig = px.scatter_geo(country_df, locations='Country', color='Availability_365', hover_data=['Availability_365'], locationmode='country names', size='Availability_365', title='Avg Availability in each Country', color_continuous_scale='agsunset')
        st.plotly_chart(fig, use_container_width=True)
