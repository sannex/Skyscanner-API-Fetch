import requests
from datetime import datetime, timedelta
import pandas as pd

url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-roundtrip"

headers = {
    "x-rapidapi-key": "9ffa9681d0mshd60e89540e0d1a9p15addfjsnf0f87345df5a",
    "x-rapidapi-host": "skyscanner80.p.rapidapi.com"
}

# Function to get the flight data for a specific departure and return date and changed layout to be more readable instead of one line
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


# function to fix the formatting on excel
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

    # variable to store all the flight data and the current date
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
            # legs is a list of legs, each leg is a dictionary with the departure, arrival, duration and origin and destination
            for leg in legs:
                flight_data = {
                    'Depart date': depart_date,
                    'Return date': return_date,
                    'Origin': leg['origin']['displayCode'],
                    'Destination': leg['destination']['displayCode'],
                    'Departure time': format_time(leg['departure']),
                    'Arrival time': format_time(leg['arrival']),
                    'Duration': format_duration(leg['durationInMinutes']),
                    # adding the price in pounds for excel formatting
                    'Price': f"£{price}"
                }
                all_data.append(flight_data)

        # Moves to the next day so that the next departure date is the current date plus one day
        current_date += timedelta(days=1)

    # pandas dataframe yep
    df = pd.DataFrame(all_data)

    # save the dataframe to an excel file and print that it has been saved
    df.to_excel("london to korea.xlsx", index=False)
    print("Data saved to london to korea.xlsx")

if __name__ == "__main__":
    main()
