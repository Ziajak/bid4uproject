from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import json
import requests
from datetime import datetime, timedelta


# Dla ułatwienia, definiujemy domyślne wartości (tak zwane stałe), są one uniwersalne
DEFAULT_OAUTH_URL = 'https://allegro.pl/auth/oauth'
DEFAULT_REDIRECT_URI = 'http://localhost:8000/bid4u/code/{id}'
DEFAULT_REDIRECT_URI_CHECK = 'http://localhost:8000/bid4u/check/{id}'
DEFAULT_REDIRECT_URI_TOKEN = 'http://localhost:8000/bid4u'
#redirect_uri = 'http://localhost:8000/movies/code/{id}'



# Implementujemy funkcję, której parametry przyjmują kolejno:
#  - client_id (ClientID), api_key (API Key) oraz opcjonalnie redirect_uri i oauth_url
# (jeżeli ich nie podamy, zostaną użyte domyślne zdefiniowane wyżej)

def get_access_code(client_id, api_key, id, oauth_url=DEFAULT_OAUTH_URL, redirect_uri=DEFAULT_REDIRECT_URI):
    # zmienna auth_url zawierać będzie zbudowany na podstawie podanych parametrów URL do zdobycia kodu
    auth_url = '{}/authorize' \
               '?response_type=code' \
               '&client_id={}' \
               '&api-key={}' \
               '&redirect_uri={}'.format(oauth_url, client_id, api_key, redirect_uri.format(id=id))
    #redirect_uri.format(id=id)



    webbrowser.open(auth_url)

    return auth_url


def get_access_code_check(client_id, api_key, id, oauth_url=DEFAULT_OAUTH_URL, redirect_uri=DEFAULT_REDIRECT_URI_CHECK):
    # zmienna auth_url zawierać będzie zbudowany na podstawie podanych parametrów URL do zdobycia kodu
    auth_url = '{}/authorize' \
               '?response_type=code' \
               '&client_id={}' \
               '&api-key={}' \
               '&redirect_uri={}'.format(oauth_url, client_id, api_key, redirect_uri.format(id=id))
    #redirect_uri.format(id=id)

    webbrowser.open(auth_url)

    return auth_url


def sign_in(client_id, client_secret, id, access_code, redirect_uri=DEFAULT_REDIRECT_URI, oauth_url=DEFAULT_OAUTH_URL):
    token_url = oauth_url + '/token'
    #client_id = '55730326fccf459196b7441357a4d614'
    #client_secret = 'hf54iV5YdGzRtjGEWXYgpb5Ye8RsmPCye3aVMLanO8eDdIM8oKMQdaypjW1ddtPg'

    access_token_data = {'grant_type': 'authorization_code',
                         'code': access_code,

                         'redirect_uri': redirect_uri.format(id=id)}

    response = requests.post(url=token_url,
                             auth=requests.auth.HTTPBasicAuth(client_id, client_secret),
                             data=access_token_data)

    #print('access_token:' + response.json()['access_token'])

    token = response.json()['access_token']
    print(token)

    return token

def put_bid(token, link, amount):
    link = link.split('-')[-1]

    ALLEGRO_JSON = "application/vnd.allegro.public.v1+json"
    headers = {
        "Accept-Language": "pl-PL",
        "Content-Type": ALLEGRO_JSON,
        "Accept": ALLEGRO_JSON,
        "Authorization": f"Bearer {token}",
    }

    with requests.Session() as session:
        session.headers.update(headers)

        DEFAULT_API_URL = 'https://api.allegro.pl'

        payload = {
            "maxAmount": {
                "amount": str(amount),
                "currency": "PLN"
            }
        }
        print(link)

        response = session.put(url=DEFAULT_API_URL + f'/bidding/offers/{link}/bid', json=payload,
                               headers=headers)

        # /sale/offers?offer.id=14980907004
        # /bid4uproject/offers/14980907004/bid
        # /sale/offers?offer.id={offer.id}
        # Wypisz odpowiedź w formacie JSON
        print(f"{response.status_code}: {response.reason}")
        print(response.json())

    # Dla przykładu: tutaj już opuściliśmy nasz 'with'
    print("Koniec programu")

