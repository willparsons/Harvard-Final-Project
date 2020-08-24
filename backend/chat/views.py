from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from chat.models import Room
from users.models import Profile, FriendRequest


@login_required
def index(request):
    return render(request, "chat/layout.html", {
        "friends": request.user.profile.all_friends(),
        "friend_requests": request.user.profile.received_requests.all(),
        "rooms": request.user.profile.rooms.all()
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


@login_required
def create_room(request, display_name, participants: str):
    participants_list = [request.user.profile]

    for p in participants.split(";"):
        try:
            participant = Profile.objects.get(user__username=p)
            participants_list.append(participant)
        except Profile.DoesNotExist:
            return JsonResponse({"error": f"{p} was not found."})

    try:
        Room.create_room(display_name, participants_list)
    except Exception as e:
        return JsonResponse({"error": e})

    return JsonResponse({"success": "Room created."})
