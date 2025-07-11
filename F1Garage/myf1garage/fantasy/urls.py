from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path("team/create/", views.create_fantasy_team, name="create_team"),
    path("team/edit/", views.edit_fantasy_team, name="edit_team"),

    
    path("team/<int:team_id>/", views.view_fantasy_team, name="view_team"),
    path("team/", views.view_fantasy_team_redirect, name="view_team_redirect"),
    
    path("leaderboard/", views.leaderboard, name="leaderboard"),

    path("admin/assign-points/", views.assign_points, name="assign_points"),


]
