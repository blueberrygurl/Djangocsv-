from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
    path('analyse/', views.analyze_csv, name='analyze_csv'),
    path('visualiser/', views.visualize_data, name='visualize_data'),  # Page de visualisation
    path('upload_success/', views.upload_success, name='upload_success'),
    path('compare_columns/', views.compare_columns, name='compare_columns'),  
]
