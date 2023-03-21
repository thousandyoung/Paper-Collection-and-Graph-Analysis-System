from django.urls import path
from . import views

urlpatterns = [
    path('papers/', views.paper_list, name='paper_list'),
    path('papers/detail/', views.paper_detail, name='paper_detail'),
    path('utils/get_node_types/', views.get_node_types, name='get_node_types'),
    path('utils/get_relationship_types/', views.get_relationship_types, name='get_relationship_types'),
    path('utils/get_all_paths', views.get_all_paths, name='get_all_paths')
]