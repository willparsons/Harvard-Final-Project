import json
from builtins import isinstance

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core import serializers
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from users.models import Profile


def index(request):
    # TODO: we need a better way of handling Anon or no friends
    if isinstance(request.user, AnonymousUser):
        return render(request, "chat/index.html", {
            "profiles": Profile.objects.all()
        })

    return render(request, "chat/index.html", {
        "profiles": Profile.objects.all(),
        "friends": request.user.profile.all_friends()
    })


@login_required
def room(request, room_name):
    return render(request, "chat/room.html", {
        "room_name": room_name
    })


def messages_api(request, user_id: int):
    try:
        recipient = Profile.objects.get(user_id=user_id)
    except IntegrityError:
        return JsonResponse({"error": "User id is not valid"})

    if request.method == "GET":
        sent_messages = request.user.profile.sent_messages.filter(recipient=recipient)

        # TODO: see if there is a better way to JSON QuerySet, since we only care about "fields"
        data = serializers.serialize("json", list(sent_messages),
                                     fields=("author", "recipient", "content", "timestamp"))

        return JsonResponse({"messages": json.loads(data)})

    elif request.method == "POST":
        # TODO: setup sending messages
        pass

    return HttpResponse(status=204)
