from django.urls import path
from . import views

urlpatterns = [
    path('paper_list/', views.paper_list),
    path('paper_detail/', views.paper_detail),
    path('get_all_paths/', views.get_all_paths),
    path('get_node_types/', views.get_node_types),
    path('get_relationship_types/', views.get_relationship_types),
]