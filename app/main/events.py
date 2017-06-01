from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
messages = dict()


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = message['msg']
    join_room(room)
    session['room'] = room
    if messages.get(room, -1) == -1:
        messages[room] = []
    chats = ''
    if len(messages.get(room)) != 0:
        for i in messages.get(room):
            chats += i + '\n'
    emit('join', {'msg': session.get('name') + ' has entered the room.', 'chats': chats}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    # print("room", session.get("room"))
    # print('session', session)
    # print('name', session.get('name'))
    room = message.get('room')
    chat = session.get('name') + ':' + message.get('msg')
    messages[room].append(chat)
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    session.pop('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

