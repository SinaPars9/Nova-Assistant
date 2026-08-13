import requests
from translations import translate , text_reshape_farsi

def joke(assistant):
    '''tell a random joke'''
    lang = assistant.language
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

if __name__ == '__main__':
    f= joke()
    print(f)