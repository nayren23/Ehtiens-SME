from flask import Blueprint, request, jsonify
from ethiens_sme.utils.role_user import RoleUser, role_required
from ethiens_sme.utils.exception.exceptions import ApiException
from ethiens_sme.service import seance_service

seance = Blueprint("seance", __name__, url_prefix="/seance")


@seance.route("/test", methods=["GET"])
def test():
    """Get information about the seance's car endpoint"""
    return jsonify("message")


@seance.route("/<ville_name>", methods=["GET"])
def get_seances_by_city(ville_name):
    """Get information about the seance's car endpoint"""
    try:
        available_seance = seance_service.get_seance_info_by_city_name(ville_name)
        response = jsonify(available_seance), 200
    except ApiException as e:
        response = jsonify({"message": e.message}), e.status_code
    return response
