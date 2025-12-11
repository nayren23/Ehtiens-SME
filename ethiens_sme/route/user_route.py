"""User related endpoints"""

from flask import Blueprint, request, jsonify, make_response
from ethiens_sme.service import user_service
from ethiens_sme.utils.exception.exceptions import ApiException
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    create_refresh_token,
    set_refresh_cookies,
)

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/test", methods=["GET"])
def register():
    """Hello World endpoint"""
    try:
        response = jsonify(message="HELLO_WORLD"), 200
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user.route("/auth", methods=["POST"])
def authenticate():
    """Authenfication endpoint"""
    json_object = request.json
    try:
        user_bo = user_service.authenticate(json_object.get("login", None), json_object.get("password", None))

        response = make_response(jsonify(message="AUTHENTIFIED_SUCCESSFULLY", pseudo_verified=user_bo.pseudo))

        # --- CORRECTION ICI ---
        # On passe directement l'ID converti en string
        # Au lieu de {"id": user_bo.id}
        user_id_str = str(user_bo.id)

        access_token = create_access_token(identity=user_id_str)
        set_access_cookies(response, access_token)

        if json_object.get("keepLoggedIn", False):
            refresh_token = create_refresh_token(identity=user_id_str)
            set_refresh_cookies(response, refresh_token)

        response.status_code = 200

    except ApiException as e:
        response = jsonify(message=e.message), e.status_code

    return response
