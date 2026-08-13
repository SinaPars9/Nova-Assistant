import requests
from ddgs import DDGS
from typing import Annotated
def get_weather(city: str) -> str:
    '''
    get the current weather of the city with Open_Meteo
    Args:
    city: name of the city (e.g., tehran,shiraz,london)
    returns:
    str: current weather
    '''
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url, timeout=10)
        geo_data = geo_response.json()
        if not geo_data.get('results'):
            return f"didnt found{city}"

        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url,timeout=10)
        weather_data = weather_response.json()
        temp = weather_data['current_weather']['temperature']
        wind = weather_data['current_weather']['windspeed']
        return f'{city}:{temp}°C\nWind : {wind}km/h'
    except requests.exceptions.Timeout:
        return 'timout: server took too long to respond'
    except requests.exceptions.ConnectionError:
        return 'connection error : check your internet connection'
    except Exception:
        return f'weather unavaiable'

def get_joke() ->str :
    '''tell a random joke'''
    try:
        url = 'https://v2.jokeapi.dev/joke/Any'
        response = requests.get(url,timeout=10)
        data = response.json()
        if data['type'] == 'twopart':
            joke_text = (f"{data['setup']}\n{data['delivery']}")
        elif data['type'] == 'single':
            joke_text= data['joke']
        else:
            joke_text = "Unknown joke format"
    except requests.exceptions.Timeout:
        return 'time out : server took too long'
    except requests.exceptions.ConnectionError:
        return 'connection Error :check your connection'
    except requests.exceptions.RequestException:
        return('joke unavailable')
    return joke_text

def get_fact() -> str:
    '''tell a random fact'''
    try:
        url = 'https://uselessfacts.jsph.pl/api/v2/facts/random'
        respond = requests.get(url,timeout=10)
        data= respond.json()
        fact = data['text']
    except requests.exceptions.Timeout:
        return 'time out : server took too long'
    except requests.exceptions.ConnectionError:
        return 'connection Error :check your connection'
    except requests.RequestException:
        return('not avaialbe')
    return fact  

def search_web(query : Annotated[str,'search term']) -> str:
    '''wearch web and return results
    Args:
    query: search term (e.g., what is python?)
    Returns:
    str: search results
    '''
    try:
        with DDGS() as ddgs:
            results = []
            for r in ddgs.text(query, max_results=3):
                results.append(f"🔹 {r['title']}\n   {r['body']}\n   {r['href']}")
            if results:
                return "🔍 Search results:\n" + "\n\n".join(results)
            else:
                return "No results found."
    except Exception as e:
        return f"Search error: {e}"   
