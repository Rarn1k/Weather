from django.urls import path

from . import views_ajax
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('search_ajax/', views_ajax.search, name='search_ajax')
]