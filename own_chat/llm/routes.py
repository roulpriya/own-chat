from flask import Blueprint, jsonify

from own_chat.llm.models import MODELS

llm_blueprint = Blueprint('llm', __name__, url_prefix='/llm')


# This route will return a list of all the models in the MODELS list
@llm_blueprint.route('/llm_models', methods=['GET'])
def get_llm_models():
    return jsonify([model.serialize() for model in MODELS]), 200



