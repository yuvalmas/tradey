import requests, os

def get_data_from_api(stock_symbol):
    url = "https://alpha-vantage.p.rapidapi.com/query"

    querystring = {"function":"GLOBAL_QUOTE","symbol":f'{stock_symbol}'}

    headers = {
        'x-rapidapi-key': os.environ.get("RAPIDAPI-KEY"),
        'x-rapidapi-host': "alpha-vantage.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text
