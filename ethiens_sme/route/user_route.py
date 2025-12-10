from flask import Blueprint, jsonify, request
from ethiens_sme import connect_mysql

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/test", methods=["GET"])
def register():
    """Hello World endpoint"""
    try:
        response = jsonify(message="HELLO_WORLD"), 200
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500
