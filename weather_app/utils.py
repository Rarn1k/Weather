import openmeteo_requests
import requests_cache
import datetime
from retry_requests import retry


def get_weather_response(lat: float, lon: float):
    """ Returns the information with weather aboutn place with given latitude and longitude """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "weather_code"],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
        "timezone": "Europe/Moscow",
    }
    responses = openmeteo.weather_api(url, params=params)
    return responses[0]


def get_current_weather(city: str, response) -> dict:
    """ Returns from response current weather """
    current = response.Current()
    weather = get_weather_description(str(int(current.Variables(1).Value())))
    weather_data = {
        'city': city,
        'temperature': round(current.Variables(0).Value()),
        'description': weather['description'],
        'img': weather['image']
    }
    return weather_data


def get_forecast_weather(response) -> list:
    """ Returns from response list with data about weather at forecast days """
    daily = response.Daily()
    daily_forecasts = []
    days_of_week = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг', 4: 'Пятница', 5: 'Суббота',
                    6: 'Воскресенье'}
    for i in range(1, 6):
        dt = datetime.datetime.fromtimestamp(daily.Time() + i * 86400)
        weather = get_weather_description(str(int(daily.Variables(0).Values(i))))
        daily_forecasts.append({
            'day_of_week': days_of_week[datetime.datetime.weekday(dt)],
            'data': datetime.datetime.strftime(dt, '%d.%m.%Y'),
            'min_temp': round(daily.Variables(2).Values(i)),
            'max_temp': round(daily.Variables(1).Values(i)),
            'description': weather['description'],
            'img': weather['image']
        })
    return daily_forecasts


def get_weather_description(code: str) -> dict:
    """ Returns the description and image for the given weather code """
    code_desc = {
        "0": {
            "description": "Солнечно",
            "image": "http://openweathermap.org/img/wn/01d@2x.png"
        },
        "1": {
            "description": "Преимущественно солнечно",
            "image": "http://openweathermap.org/img/wn/01d@2x.png"
        },
        "2": {
            "description": "Переменная облачность",
            "image": "http://openweathermap.org/img/wn/02d@2x.png"
        },
        "3": {
            "description": "Облачно",
            "image": "http://openweathermap.org/img/wn/03d@2x.png"
        },
        "45": {
            "description": "Туманно",
            "image": "http://openweathermap.org/img/wn/50d@2x.png"

        },
        "48": {
            "description": "Изморозь",
            "image": "http://openweathermap.org/img/wn/50d@2x.png"
        },
        "51": {
            "description": "Легкая морось",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "53": {
            "description": "Морось",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "55": {
            "description": "Сильный моросящий дождь",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "56": {
            "description": "Легкий моросящий дождь",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "57": {
            "description": "Замораживающая изморозь",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "61": {
            "description": "Легкий дождь",
            "image": "http://openweathermap.org/img/wn/10d@2x.png"
        },
        "63": {
            "description": "Дождь",
            "image": "http://openweathermap.org/img/wn/10d@2x.png"
        },
        "65": {
            "description": "Ливень",
            "image": "http://openweathermap.org/img/wn/10d@2x.png"
        },
        "66": {
            "description": "Небольшой ледяной дождь",
            "image": "http://openweathermap.org/img/wn/10d@2x.png"
        },
        "67": {
            "description": "Ледяной дождь",
            "image": "http://openweathermap.org/img/wn/10d@2x.png"

        },
        "71": {
            "description": "Небольшой снег",
            "image": "http://openweathermap.org/img/wn/13d@2x.png"
        },
        "73": {
            "description": "Снег",
            "image": "http://openweathermap.org/img/wn/13d@2x.png"
        },
        "75": {
            "description": "Сильный снегопад",
            "image": "http://openweathermap.org/img/wn/13d@2x.png"
        },
        "77": {
            "description": "Снежные зерна",
            "image": "http://openweathermap.org/img/wn/13d@2x.png"
        },
        "80": {
            "description": "Небольшие ливни",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "81": {
            "description": "Ливень",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "82": {
            "description": "Сильный ливень",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "85": {
            "description": "Небольшие ливневые снегопады",
            "image": "http://openweathermap.org/img/wn/13d@2x.png"
        },
        "86": {
            "description": "Снегопад",
            "image": "http://openweathermap.org/img/wn/13d@2x.png"
        },
        "95": {
            "description": "Гроза",
            "image": "http://openweathermap.org/img/wn/11d@2x.png"
        },
        "96": {
            "description": "Слабые грозы с градом",
            "image": "http://openweathermap.org/img/wn/11d@2x.png"
        },
        "99": {
            "description": "Гроза с градом",
            "image": "http://openweathermap.org/img/wn/11d@2x.png"
        }
    }
    return code_desc.get(code)
