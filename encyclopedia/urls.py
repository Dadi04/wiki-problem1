from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.index, name="wiki"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("edit_page/<str:name>", views.edit_page, name="edit_page"),
    path("submit/<str:name>", views.submit, name="submit"),
    path("random_page", views.random_page, name="random_page")
]
