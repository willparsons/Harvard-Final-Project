from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("chat/<str:room_name>/", views.room, name="room"),

    # api routes
    path("friend/<str:username>/add/", views.send_friend_request, name="send_friend_request"),
    path("friend/<str:username>/accept/", views.accept_friend_request, name="accept_friend_request"),
    path("friend/<str:username>/reject/", views.reject_friend_request, name="reject_friend_request")
]
