from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("krish", views.krish, name="krish"),
  path("<str:name>", views.greet, name="greet")
]