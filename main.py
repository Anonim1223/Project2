import requests
import json


def get_location_key(latitude, longitude, api_key):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={api_key}&q={latitude},{longitude}"

    response = requests.get(url)

    if response.status_code == 200:
        location_data = response.json()
        return location_data['Key'], location_data['LocalizedName']
    else:
        print(f"Ошибка получения ключа локации: {response.status_code}")
        return None, None


def get_weather(location_key, api_key):
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}&details=true"

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return {
            'temperature': weather_data[0]['Temperature']['Metric']['Value'],
            'humidity': weather_data[0]['RelativeHumidity'],
            'wind_speed': weather_data[0]['Wind']['Speed']['Metric']['Value'],
            'precipitation_probability': weather_data[0]['Precip1hr']['Metric']['Value']
        }
    else:
        print(f"Ошибка получения погоды: {response.status_code}")
        return None


def save_weather_to_json(weather_info, city_name):
    # Создаем словарь с данными о погоде
    data_to_save = {
        'city': city_name,
        'weather': weather_info
    }

    # Сохраняем данные в файл JSON
    with open('weather_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_to_save, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    latitude = float(input("Введите широту: "))
    longitude = float(input("Введите долготу: "))

    api_key = 'ВАШ_API_КЛЮЧ'

    location_key, city_name = get_location_key(latitude, longitude, api_key)

    if location_key:
        print(f"Город: {city_name}")
        weather_info = get_weather(location_key, api_key)

        if weather_info:
            print(f"Температура: {weather_info['temperature']} °C")
            print(f"Влажность: {weather_info['humidity']} %")
            print(f"Скорость ветра: {weather_info['wind_speed']} м/с")
            print(f"Вероятность дождя: {weather_info['precipitation_probability']} %")

            # Сохраняем данные о погоде в файл JSON
            save_weather_to_json(weather_info, city_name)
