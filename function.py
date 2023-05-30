from typing import Any, Literal
from flask import jsonify

def check_main_params(data: dict) -> (tuple[Any, Literal[400, 403, 404]] | None):
    if len(data.keys()) == 0:
        return jsonify({'message': 'Need parameters'}), 403
    
    if "gender" not in data.keys():
        return jsonify({'message': 'Bad request'}), 403
    
    if "region" not in data.keys():
        return jsonify({'message': 'Bad request'}), 403
    
    return None