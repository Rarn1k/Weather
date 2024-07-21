from django.http import JsonResponse, HttpRequest
import json
from dadata import Dadata


def is_ajax(request: HttpRequest) -> bool:
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def search(request: HttpRequest) -> JsonResponse:
    token = "355e5e8d327000ad563154208ce57cae73290594"
    dadata = Dadata(token)
    if request.method == "POST" and is_ajax(request=request):
        city = request.POST["city"]
        result = dadata.suggest(name='address', query=city, count=5, from_bound={"value": "city"},
                                to_bound={"value": "city"})
        cities = []
        for res in result:
            cities.append({'city_name': res['data']['city']})

        cities_json = json.dumps(cities)
        return JsonResponse({"success": True, "cities_json": cities_json}, status=200)
    return JsonResponse({"success": False, "cities_json": ''}, status=500)
