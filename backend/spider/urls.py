from django.urls import path
from . import views

urlpatterns = [
    path('spiders/', views.spiders),
    path('spiders/<int:spider_id>/', views.spider),
]
