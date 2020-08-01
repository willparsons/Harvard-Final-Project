from builtins import isinstance

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render

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
    return render(request, "chat/index.html", {
        "room_name": room_name
    })
