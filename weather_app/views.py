import urllib

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from dadata import Dadata

from weather_app.utils import get_weather_response, get_current_weather, get_forecast_weather


def set_viewed_city_cookie(response: HttpResponse, city: str):
    data = urllib.parse.quote(city, safe='')
    response.set_cookie('city', data, max_age=3600 * 24 * 30)


def get_viewed_city_cookie(request: HttpRequest):
    data = request.COOKIES.get('city')
    if not data:
        return None
    return urllib.parse.unquote(data)


def index(request: HttpRequest) -> HttpResponse:
    last_city = get_viewed_city_cookie(request)
    city_name = request.GET.get('city')
    if request.method == 'POST':
        city_name = request.POST['city']
        return redirect(f'/?city={city_name}')
    if city_name:
        token = "355e5e8d327000ad563154208ce57cae73290594"
        dadata = Dadata(token)
        sugges = dadata.suggest(name='address', query=city_name, count=1, from_bound={"value": "city"},
                                to_bound={"value": "city"})
        if len(sugges) < 1:
            return render(request, 'weather_app/index.html', {'last_city': last_city})
        current_city = sugges[0]
        lat, lon = current_city['data']['geo_lat'], current_city['data']['geo_lon']
        resp = get_weather_response(lat, lon)
        weather_data = get_current_weather(current_city['data']['city'], resp)
        daily_forecasts = get_forecast_weather(resp)
        context = {
            'weather_data': weather_data,
            'daily_forecasts': daily_forecasts,
        }
        response = render(request, 'weather_app/index.html', context)
        set_viewed_city_cookie(response, current_city['data']['city'])
        return response
    return render(request, 'weather_app/index.html', {'last_city': last_city})
