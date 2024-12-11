from app import check_bad_weather


# Примеры проверки модели
print(check_bad_weather(-5, 30, 10))  # Ожидается "плохая"
print(check_bad_weather(25, 40, 80))  # Ожидается "плохая"
print(check_bad_weather(20, 10, 20))  # Ожидается "хорошая"
