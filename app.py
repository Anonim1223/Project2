from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def get_location_key(city_name, api_key):
    """Получение ключа локации по названию города"""
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city_name}"

    response = requests.get(url)

    if response.status_code == 200 and response.json():
        return response.json()[0]['Key']
    else:
        return None


def get_weather(location_key, api_key):
    """Получение текущих погодных условий по ключу локации"""
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}&details=true"

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return {
            'temperature': weather_data[0]['Temperature']['Metric']['Value'],
            'wind_speed': weather_data[0]['Wind']['Speed']['Metric']['Value'],
            'precipitation_probability': weather_data[0]['Precip1hr']['Metric']['Value']
        }
    else:
        return None


def check_bad_weather(temperature, wind_speed, precipitation_probability):
    """Оценка погодных условий"""
    if temperature < 0 or temperature > 35:
        return "плохая погода"
    if wind_speed > 50:
        return "плохая погода"
    if precipitation_probability > 70:
        return "плохая погода"

    return "хорошая погода"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/check_weather', methods=['POST'])
def check_weather_route():
    start_city = request.form['start_city']
    end_city = request.form['end_city']

    api_key = ''

    try:
        start_location_key = get_location_key(start_city, api_key)
        end_location_key = get_location_key(end_city, api_key)

        if not start_location_key or not end_location_key:
            raise ValueError("Не удалось получить данные о городах.")

        # Получаем данные о погоде
        start_weather_info = get_weather(start_location_key, api_key)
        end_weather_info = get_weather(end_location_key, api_key)

        # Проверяем погоду
        if start_weather_info and end_weather_info:
            result1 = 'В начале пути ' + check_bad_weather(
                start_weather_info['temperature'],
                start_weather_info['wind_speed'],
                start_weather_info['precipitation_probability']
            )
            result2 = 'В конце пути ' + check_bad_weather(
                end_weather_info['temperature'],
                end_weather_info['wind_speed'],
                end_weather_info['precipitation_probability']
            )
            return render_template('index.html', result1=result1, result2=result2)

        raise ValueError("Не удалось получить данные о погоде.")

    except Exception as e:
        return render_template('index.html', error=str(e))


if __name__ == "__main__":
    app.run(debug=True)
