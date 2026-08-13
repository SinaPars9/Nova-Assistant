import requests
from translations import translate , text_reshape_farsi
def get_fact(assistant):
    '''tell a random fact'''
    lang = assistant.language
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



if __name__ == '__main__':
    f =get_fact()
    print(f)


