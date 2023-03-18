from django.urls import path
from . import views

urlpatterns = [
    path('papers/', views.paper_list, name='paper_list'),
    path('papers/detail/', views.paper_detail, name='paper_detail'),
]