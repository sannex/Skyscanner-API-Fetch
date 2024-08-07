import requests
from datetime import datetime, timedelta
import csv
from dotenv import load_dotenv
import os


load_dotenv()
url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-roundtrip"

headers = {
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
    "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
}


# Function to get the flight data for a specific departure and return date from the Skyscanner API
def get_data(depart_date, return_date):
    querystring = {
        "fromId": "eyJzIjoiTE9ORCIsImUiOiIyNzU0NDAwOCIsImgiOiIyNzU0NDAwOCJ9",
        "toId": "\"eyJzIjoiU0VMQSIsImUiOiIyNzUzODYzOCIsImgiOiIyNzUzODYzOCJ9\"",
        "departDate": depart_date,
        "returnDate": return_date,
        "adults": "1",
        "cabinClass": "economy",
        "currency": "GBP",
        "market": "US",
        "locale": "en-US"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def format_duration(duration):
    hours = duration // 60
    minutes = duration % 60
    return f"{hours} hours {minutes} minutes"

#function to format the time in excel
def format_time(time):
    # 24 hour time format for excel
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")

def main():
    # the start and end dates for departure
    start_date = datetime(2024, 11, 1)
    end_date = datetime(2024, 11, 25)
    return_date = "2025-01-15" 
    # creates a list to store all the data
    current_date = start_date
    all_data = []
    
    # while loop to iterate through each day from the start date to the end date
    while current_date <= end_date:
        # format the departure date to be in the format needed for the api request
        depart_date = current_date.strftime("%Y-%m-%d")
        # makes output more readable and cleaner
        print(f"Fetching data for depart date: {depart_date}")

        # fetch the flight data for the current departure date and fixed return date
        response_json = get_data(depart_date, return_date)

        # Extract relevant data from the json response and store it in the all_data list
        for itinerary in response_json.get('data', {}).get('itineraries', []):
            price = itinerary['price']['raw']
            legs = itinerary['legs']
            # creates 2 legs for the round trip so it all can be displayed in one line on the dataframe
            if len(legs) == 2:
                outbound_leg = legs[0]
                return_leg = legs[1]
                flight_data = {
                    'Depart date': depart_date,
                    'Return date': return_date,
                    'Outbound Origin': outbound_leg['origin']['displayCode'],
                    'Outbound Destination': outbound_leg['destination']['displayCode'],
                    'Outbound Departure time': format_time(outbound_leg['departure']),
                    'Outbound Arrival time': format_time(outbound_leg['arrival']),
                    'Outbound Duration': format_duration(outbound_leg['durationInMinutes']),
                    'Return Origin': return_leg['origin']['displayCode'],
                    'Return Destination': return_leg['destination']['displayCode'],
                    'Return Departure time': format_time(return_leg['departure']),
                    'Return Arrival time': format_time(return_leg['arrival']),
                    'Return Duration': format_duration(return_leg['durationInMinutes']),
                    'Price': f"£{price:.2f}"  # Single price for the round trip
                }
                all_data.append(flight_data)
                
    # Moves to the next day so that the next departure date is the current date plus one day
        current_date += timedelta(days=1)
    # Writes the data to a csv file with the correct column names
    with open ('london to korea.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Depart date', 'Return date', 
            'Outbound Origin', 'Outbound Destination', 'Outbound Departure time', 'Outbound Arrival time', 'Outbound Duration', 
            'Return Origin', 'Return Destination', 'Return Departure time', 'Return Arrival time', 'Return Duration', 
            'Price'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)
        
    
    
if __name__ == "__main__":
    main()
