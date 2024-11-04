import os
import requests as req
import util_time_formatter as currtime

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': os.getenv("OPEN_WEATHER_API_KEY"),
        'units': 'metric'
    }
    response = req.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        city_name = data['name']
        country = data['sys']['country']
        return f"Weather in {city_name}, {country}: {weather_desc}, Temperature: {temp}°C"
    else:
        return "City not found or error fetching weather data."

# currently returns only a single city
def geocoder_to_coords(city : str, state_code : str = None, country_code : str = None) -> dict[str,str]:
    
    '''
    Direct geocoding converts the specified name of a location or zip/post code into the exact geographical coordinates; -- type shi
    '''

    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    
    q = city.strip()
    if(state_code):
        q += ","
        q += state_code.strip()

    if(country_code):
        q += ','
        q += country_code.strip()
    params = {
        "q" : q,
        "appid" : os.getenv("OPEN_WEATHER_API_KEY"),
        # "limit" : "10" # this would limit how many entries in the main list in the res, since commented = 1 max rn
    }

    res = req.get(base_url, params=params)
    if(res.status_code == 200):
        data = res.json() # -- returns a list of dictionaries, each dictionary has a city with the info
        
        if(len(data) == 0):
            print(f"[!] {currtime.get_curr_timestamp()} : Response received from openweather geocoder API but the request matches no cities")
            return None
        
        else:
            return {

                "name"  :   data[0]['name'],
                "state"   :   data[0]['state'],
                "country"   : data[0]['country'],
                "lat"   : data[0]['lat'],
                "lon" : data[0]['lon']
            }

    else:

        print(f'[!] {currtime.get_curr_timestamp()} :Request failed with code = {res.status_code}')

def get_current_weather(data:dict[str,str]) -> str:
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {

        "lat" : data['lat'],
        'lon' : data['lon'],
        'appid' : os.getenv("OPEN_WEATHER_API_KEY"),
        'units' : 'metric'
    }

    res = req.get(base_url, params = params)
    if res.status_code == 200:
        received = res.json()

        if(len(received) == 0):
            print(f'[!] {currtime.get_curr_timestamp()} : Response received with code = {res.status_code}, but no data in the payload')
            print(received)
            return "We are experiencing a technical problem connecting to weather services, please try again later."

        city_name = received['name']
        state = data['state']
        country = data['country']
        temp = received['main']['temp']
        feels = received['main']['feels_like']
        humidity =  received['main']['humidity']
        description = received['weather'][0]['description']
        wind_speed = received['wind']['speed']

        description = description + format_with_emotes(str(received['weather'][0]['id']), received['weather'][0]['icon'])

        return f'''
                Weather in {city_name}, {state}, {country}
                
                {description}
                
                Temperature: {temp} °C, feels like {feels}°C
                Humidity: {humidity}%
                Wind speed: {wind_speed}ms
                '''

    else:
        print(f'[!] {currtime.get_curr_timestamp()} :Request failed with code = {res.status_code}')
        return f'We are experiencing a technical problem connecting to weather services, please try again later. (Request failed with code = {res.status_code})'

def format_with_emotes(weather_code: str, icon:str) -> str:
    if(weather_code[0] == '2'):
        return " - Try to stay indoors! :thunder_cloud_rain: "
    elif(weather_code[0] == '3'):
        return " :cloud_rain: "
    elif(weather_code[0] == "5"):
        return " :cloud_rain: "
    elif(weather_code[0] == '6'):
        return " - Dress warm! :snowflake: "
    elif(weather_code[0] == '7' and weather_code[1] == '4'):
        return " :fog: "
    elif(int(weather_code) == 800 and icon[2] == 'n' ):
        return " - Nice clear sky! :crescent_moon: "
    elif(int(weather_code) == 800 and icon[2] == 'd' ):
        return " - Nice clear sky! :sun: "
    elif(int(weather_code) == 801 and icon[2] == 'd'):
        return " :white_sun_small_cloud: "
    elif(int(weather_code) == 801 and icon[2] == 'n'):
        return " :cloud: "
    elif(int(weather_code) == 802 and icon[2] == 'd'):
        return " :partly_sunny: "
    elif(int(weather_code) == 802 and icon[2] == 'n'):
        return " :cloud: "
    elif(int(weather_code) == 803 and icon[2] == 'd'):
        return " :white_sun_cloud: "
    elif(int(weather_code) == 803 and icon[2] == 'n'):
        return " :cloud: "
    elif(int(weather_code) == 804 and icon[2] == 'd'):
        return " :white_sun_cloud: "
    elif(int(weather_code) == 804 and icon[2] == 'n'):
        return " :cloud: "
    else:
        return ""