def check_bad_weather(temperature, wind_speed, precipitation_probability):
    if temperature < 0 or temperature > 35:
        return "плохие погодные условия"
    if wind_speed > 50:
        return "плохие погодные условия"
    if precipitation_probability > 70:
        return "плохие погодные условия"

    return "хорошие погодные условия"


# Примеры проверки модели
print(check_bad_weather(-5, 30, 10))  # Ожидается "плохие"
print(check_bad_weather(25, 40, 80))  # Ожидается "плохие"
print(check_bad_weather(20, 10, 20))  # Ожидается "хорошие"
