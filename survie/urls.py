from django.urls import path
from . import views

app_name = 'survie'

urlpatterns = [
    path('', views.game_view, name='game'),
    path('api/scenario/<int:scenario_id>/', views.scenario_view, name='scenario'),
    path('api/choix/<int:choix_id>/', views.choix_view, name='choix'),
] 