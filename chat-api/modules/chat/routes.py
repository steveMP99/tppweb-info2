# app/auth/routes.py
from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.chat.models import Message, Converssation, Participant
from modules.auth.models import Personne
import random
import string

chat_bp = Blueprint('chat', __name__)

def randomStr(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Route d'enregistrement
@chat_bp.route('/sendMessage', methods=['POST'])
@jwt_required()
def send():
    personne = request.json.get('personne')
    converssation_id = request.json.get('converssation')
    message = request.json.get('message')
    type = request.json.get('type')
    current_user_id = get_jwt_identity()
    
    if current_user_id not in personne:
        return jsonify({'message': 'Echec de demarrage de discution'}), 401
    
    if converssation_id == None:    
        converssation = Converssation(
            code = randomStr(5),
            type = type
        )
        converssation.save_to_db()
        conv_id = converssation.id
        
        for id in personne:
            participant = Participant(
                converssation_id = conv_id,
                personne_id = id
            )
            participant.save_to_db()
        
    else:
        conv_id = converssation_id
    
    
    message = Message(
        converssation_id = conv_id,
        personnel_id = current_user_id,
        content = message
    )
    message.save_to_db()
    
    
    return jsonify({'message': 'Message envoyé registered successfully', 'data': "message"}), 200
    
@chat_bp.route("/getMessage", methods=["POST"])
@jwt_required()
def getMessages():
    converssation_id = request.json.get('converssation')
    current_user_id = get_jwt_identity()
    converssation = Converssation.get_by_id(converssation_id)
    participant = Participant.get_by_converssation_id(converssation_id)
    messages = Message.get_all(converssation_id)
    response = {
        "converssation": converssation,
        "participants" : participant,
        "messages": messages
    }
    
    return jsonify(response), 200
