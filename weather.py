import requests
from translations import translate , text_reshape_farsi
def weather(assistant):
    if not assistant.city:
        city = input('your city : ')
        assistant.city = city
        assistant.save()
    else:
        city = assistant.city
    lang = assistant.language
    coords = assistant.get_coordinates()
    if coords is None:
        return "city not found"
    lat, lon = coords
    url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={lat}&longitude={lon}"
    f"&current_weather=true")
    try:
        response = requests.get(url,timeout=10)
        data = response.json()
        temp = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]
        time = data["current_weather"]["time"]
        text ={'city': assistant.city,
        'temp': temp}
        return  text
    except requests.exceptions.Timeout:
        return 'time out : server took too long'
    except requests.exceptions.ConnectionError:
        return 'connection Error :check your connection'
    except requests.RequestException:
        return ('weather unavailable')
    
if __name__ == '__main__':
    f = weather()
    print(f)
   
 