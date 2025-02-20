from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from own_chat.chats.models import Chat, Message
from own_chat.llm.factory import get_llm_handler
from own_chat.llm.llm_handler import Message as LLMMessage
from own_chat.llm.models import LLMModel
from own_chat.user.models import db

blueprint = Blueprint("chats", __name__)


# This route allows the user to start a new chat with a selected model.
# The user can select a model by providing the model name in the request body.
# The route creates a new chat instance in the database and returns the chat ID, model ID, and initial response from the model.
# If the model is not found or the user has reached the chat limit, an error message is returned.
@blueprint.route("/chats", methods=["POST"])
@login_required
def start_chat():
    data = request.json
    model_id = data.get("model_id")

    # Find the model
    llm_model = LLMModel.query.get_or_404(model_id)

    if not llm_model:
        return jsonify({"message": "Invalid model selected"}), 400

    # Check user's chat limit
    chat_count = Chat.query.filter_by(user_id=current_user.id).count()
    if chat_count >= 100:
        return jsonify({"error": "Chat limit reached"}), 429

    # Create new chat
    new_chat = Chat(
        user_id=current_user.id,
        llm_model_id=llm_model.id,
        title=f"Chat with {llm_model.name}",
    )
    db.session.add(new_chat)
    db.session.commit()

    handler = get_llm_handler("openai")
    response = handler.generate_response(model_name, "", [])

    return jsonify(
        {"chat_id": new_chat.id, "model": llm_model.id, "initial_response": response}
    ), 201


# Retrieves previous chats for a specific model and user.
@blueprint.route("/chats", methods=["GET"])
@login_required
def get_previous_chats():
    chats = Chat.query.filter_by(user_id=current_user.id).all()

    if not chats:
        return jsonify({"error": "No chats found"}), 404

    return jsonify({"chats": [chat.serialize() for chat in chats]}), 200


# send message to a chat
@blueprint.route("/chats/<int:chat_id>/messages", methods=["POST"])
@login_required
def send_message(chat_id: int):
    data = request.json
    message = data.get("message")

    chat = Chat.query.filter_by(id=chat_id, user_id=current_user.id).first_or_404(
        "Chat not found"
    )

    # Generate model response
    llm_handler = get_llm_handler("openai")
    response = llm_handler.generate_response(
        model_name=chat.llm_model.name,
        system_message="",
        messages=[
                     LLMMessage(role=message.sender, content=message.content)
                     for message in chat.messages
                 ] + [LLMMessage(role="user", content=message)],
    )

    # Save the message and response to the database
    db.session.add(Message(chat_id=chat.id, sender="user", content=message))
    model_response = Message(chat_id=chat.id, sender="assistant", content=response)
    db.session.add(model_response)

    db.session.commit()

    return jsonify(model_response.serialize()), 200


@blueprint.route("/chats/<int:chat_id>/messages", methods=["GET"])
@login_required
def get_messages(chat_id):
    chat = Chat.query.filter_by(id=chat_id, user_id=current_user.id).first_or_404(
        "Chat not found"
    )

    messages = [message.serialize() for message in chat.messages]

    return jsonify({"messages": messages}), 200


# delete chat
@blueprint.route("/chats/<int:chat_id>", methods=["DELETE"])
@login_required
def delete_chat(chat_id):
    chat = Chat.query.filter_by(id=chat_id, user_id=current_user.id).first()

    if not chat:
        return jsonify({"error": "Chat not found"}), 404

    db.session.delete(chat)
    db.session.commit()

    return jsonify({"message": "Chat deleted successfully"}), 200
