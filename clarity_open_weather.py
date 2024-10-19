import os
import requests
def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': os.getenv("OPEN_WEATHER_API_KEY"),
        'units': 'metric'
    }
    print(os.getenv("OPEN_WEATHER_API_KEY"))
    response = requests.get(base_url, params=params)
    print(response.status_code)
    print(response)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        city_name = data['name']
        country = data['sys']['country']
        return f"Weather in {city_name}, {country}: {weather_desc}, Temperature: {temp}°C"
    else:
        return "City not found or error fetching weather data."