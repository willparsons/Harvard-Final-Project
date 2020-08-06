from builtins import isinstance

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from users.models import Profile, FriendRequest


@login_required
def index(request):
    # TODO: remove hard-code
    return render(request, "chat/layout.html", {
        "room_name": "lobby",
        "friends": request.user.profile.all_friends(),
        "friend_requests": request.user.profile.received_requests.all()
    })


@login_required
def room(request, room_name):
    return render(request, "chat/index.html", {
        "room_name": room_name
    })


@login_required
def send_friend_request(request, username: str):
    try:
        to_user = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist as e:
        return JsonResponse({"error": "User not found."})

    fr, created = FriendRequest.objects.get_or_create(from_user=request.user.profile, to_user=to_user)

    if not created:
        return JsonResponse({"error": "Friend request already sent."})

    return JsonResponse({"success": "Friend request sent successfully."})


@login_required
def accept_friend_request(request, username: str):
    try:
        fr = FriendRequest.objects.get(from_user__user__username=username)
    except FriendRequest.DoesNotExist as e:
        print(e)
        return JsonResponse({"error": "FriendRequest not found"})

    fr.accept()

    return JsonResponse({"success": "FriendRequest accepted"})


@login_required
def reject_friend_request(request, username: str):
    try:
        fr = FriendRequest.objects.get(from_user__user__username=username)
    except FriendRequest.DoesNotExist as e:
        print(e)
        return JsonResponse({"error": "FriendRequest not found"})

    fr.reject()

    return JsonResponse({"success": "FriendRequest rejected"})


def old_index(request):
    # TODO: we need a better way of handling Anon or no friends
    if isinstance(request.user, AnonymousUser):
        return render(request, "chat/index.html", {
            "profiles": Profile.objects.all()
        })

    frs = FriendRequest.objects.filter(to_user=request.user.profile)
    print(frs)
    return render(request, "chat/index.html", {
        "profiles": Profile.objects.all(),
        "friends": request.user.profile.all_friends(),
        "friend_requests": FriendRequest.objects.filter(to_user=request.user.profile)
    })
