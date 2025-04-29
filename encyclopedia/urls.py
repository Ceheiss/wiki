from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create-page", views.create_page, name="create-page"),
    path("random-page", views.random_page, name="random-page"),
    path("wiki/<str:entry>/", views.entry, name="entry")
]
