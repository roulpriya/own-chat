from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from .gpt_handler import LLMHandler
from .models import db, LLMModel, Chat

api = Blueprint('api', __name__)


@api.route('/chats', methods=['POST'])
@login_required
def start_chat():
    data = request.json
    model_name = data.get('model')

    # Find the model
    llm_model = LLMModel.query.filter_by(name=model_name, is_active=True).first()

    if not llm_model:
        return jsonify({'message': 'Invalid model selected'}), 400

    # Check user's chat limit
    chat_count = Chat.query.filter_by(user_id=current_user.id).count()
    if chat_count >= 100:
        return jsonify({'error': 'Chat limit reached'}), 429

    # Create new chat
    new_chat = Chat(
        user_id=current_user.id,
        llm_model_id=llm_model.id,
        title=f"Chat with {model_name}"
    )
    db.session.add(new_chat)
    db.session.commit()

    response = LLMHandler.generate_response(model_name, "")

    return jsonify({
        'chat_id': new_chat.id,
        'model': llm_model.name,
        'initial_response': response
    }), 201


@api.route('/chats', methods=['GET'])
@login_required
def get_previous_chats():
    # Get all chats for the current user
    chats = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.created_at.desc()).all()

    return jsonify({
        'chats': [
            {
                'id': chat.id,
                'title': chat.title,
                'model': chat.llm_model.name,
                'created_at': chat.created_at.isoformat()
            } for chat in chats
        ]
    }), 200


@api.route('/chats/<int:chat_id>', methods=['DELETE'])
@login_required
def delete_chat(chat_id):
    chat = Chat.query.filter_by(
        id=chat_id,
        user_id=current_user.id
    ).first()

    if not chat:
        return jsonify({'error': 'Chat not found'}), 404

    db.session.delete(chat)
    db.session.commit()

    return jsonify({'message': 'Chat deleted successfully'}), 200
