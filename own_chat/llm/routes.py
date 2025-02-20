from flask import Blueprint, jsonify

from own_chat.llm.models import MODELS

llm_blueprint = Blueprint('llm', __name__, url_prefix='/llm')


@llm_blueprint.route('/llm_models', methods=['GET'])
def get_llm_models():
    return jsonify([model.serialize() for model in MODELS]), 200
