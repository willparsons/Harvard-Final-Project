from chat.models import Room, Message


def message_to_json(message: Message, room: Room):
    # TODO: format this better
    time = str(message.timestamp.time())

    return {
        "id": message.id,
        "author": message.author.user.username,
        "image": message.author.image.url,
        "room": room.name,
        "content": message.content,
        "timestamp": time
    }


def messages_to_json(messages, room: Room):
    return [message_to_json(message, room) for message in messages]
