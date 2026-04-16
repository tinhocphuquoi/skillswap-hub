from flask_socketio import emit, join_room
from . import socketio
from flask_login import current_user
from .models import Message, db
from . import db

@socketio.on('send_message')
def handle_message(data):
    msg = Message(sender_id=current_user.id, receiver_id=data['receiver_id'], content=data['message'])
    db.session.add(msg)
    db.session.commit()
    emit('receive_message', {
        'sender': current_user.username,
        'message': data['message'],
        'time': msg.timestamp.strftime('%H:%M')
    }, room=f'chat_{min(current_user.id, data["receiver_id"])}_{max(current_user.id, data["receiver_id"])}')