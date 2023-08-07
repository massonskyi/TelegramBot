import requests

API: str = "b65fa46c52b6495dac295839230708"


def get_weather_now(sity: str, aqi: str = None, api: str = API) -> str:
    url = "http://api.weatherapi.com/v1/current.json"
    dataset = {
        'q': sity,
        'aqi': aqi,
        "key": api
    }
    response = requests.get(url, params=dataset)
    data = response.json()
    result_str: str = (
        f"Страна: {data['location']['country']}\n",
        f"Регион: {data['location']['region']} \n",
        f"Время: {data['location']['localtime']}\n"
        f"Время обновления: {data['current']['last_updated']}\n",
        f"Температура: {data['current']['temp_c']}C, {data['current']['temp_f']}F\n",
        f"Скорость ветра: {data['current']['wind_mph']}/{data['current']['wind_kph']} mph/kph\n",
        f"Давление: {data['current']['pressure_mb']}/{data['current']['pressure_in']}\n",
        f"Влажность: {data['current']['humidity']}%\n",
        f"Облачность: {data['current']['precip_mm']}/{data['current']['precip_in']}\n"
    )
    return result_str
