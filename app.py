import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

@st.cache_data
def load_data():
    df = pd.read_csv('london to korea.csv')
    df['Depart date'] = pd.to_datetime(df['Depart date'])
    df['Return date'] = pd.to_datetime(df['Return date'])
    #pound sign not showing in table
    df['Price'] = df['Price'].replace('[^\d.]', '', regex=True).astype(float)
    df['Price'] = df['Price'].apply(lambda x: f"£{x:.2f}")
   
        
    return df

image = Image.open('korea.jpg')

#column layouts
col1, col2 = st.columns([3, 1])

df = load_data()
with col1:
    st.title('London to Korea Flights')

    depart_date = st.date_input("Select departure date", min_value=datetime(2024, 11, 1), max_value=datetime(2024, 11, 25))
    return_date = st.date_input("Select return date", min_value=datetime(2025, 1, 15), max_value=datetime(2025, 1, 15))

    #fix zeros in the depart and return dates
    filtered_df = df[(df['Depart date'].dt.date == depart_date) & (df['Return date'].dt.date == return_date)]

    if not filtered_df.empty:
        st.write(f"Showing results for: {depart_date} to {return_date}")
        filtered_df['Depart date'] = filtered_df['Depart date'].dt.strftime('%Y-%m-%d')
        filtered_df['Return date'] = filtered_df['Return date'].dt.strftime('%Y-%m-%d')
        st.dataframe(filtered_df.reset_index(drop=True), hide_index=True)
        
    else:
        st.write("No flights found these dates.")
    
    
#button to show cheapest flight in november
if st.button('Show Cheapest Flight in November'):
    
    df['Price'] = df['Price'].replace('[^\d.]', '', regex=True).astype(float)
    cheapest_flight = df.loc[df['Price'].idxmin()]
    cheapest_flight['Price'] = f"£{cheapest_flight['Price']:.2f}"
    #fix zeros in the depart and return dates
    cheapest_flight['Depart date'] = cheapest_flight['Depart date'].strftime('%Y-%m-%d')
    cheapest_flight['Return date'] = cheapest_flight['Return date'].strftime('%Y-%m-%d')
    st.write("Cheapest Flight in November:")
    st.table(cheapest_flight.to_frame().T.reset_index(drop=True)) 
    
with col2:    
    st.image(Image.open('korea.jpg'))
    