import requests
from bs4 import BeautifulSoup
import openai

def tenki():
    url = "https://tenki.jp/forecast/3/17/4610/14130/1hour.html"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    element = soup.find(id="forecast-point-1h-today")

    weather_dict = {}

    weather_row = element.find('tr', class_='weather')
    weather_data = weather_row.find_all('p')
    temperature_row = element.find('tr', class_='temperature')
    temperature_data = temperature_row.find_all('span')
    prob_precip_row = element.find('tr', class_='prob-precip')
    prob_precip_data = prob_precip_row.find_all('span')
    humidity_row = element.find('tr', class_='humidity')
    humidity_data = humidity_row.find_all('span')

    for i, p in enumerate(weather_data, start=1):
        weather_dict[str(i)+"時"] = {"weather:": p.text,
                                    "temperature": temperature_data[i-1].text,
                                    "humidity": humidity_data[i-1].text,
                                    "prob_precip_data": prob_precip_data[i-1].text, }
    return weather_dict

def withOpenAI(user_message):
    openai.api_key = ""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"dict形式で与えられた川崎市の今日の天気予報です。{tenki()}"},
            {"role": "system", "content": "出かける時間だったり、用事、雰囲気などを指定するするので、天気情報なども甘味しながら、良さそうな服装をスタイリストとして3パターンほど提示して下さい。"},
            {"role": "system", "content": "雨が降りそうであったら、傘を持って行った方がいいなどのアドバイスもして下さい。"},
            {"role": "system", "content": "天気の情報や、湿度の情報は提示しないでください。"},
            {"role":"user","content":user_message}
        ],
    )
    return response.choices[0]["message"]["content"].strip()