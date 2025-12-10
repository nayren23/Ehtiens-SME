from flask import Blueprint, request, jsonify
from ethiens_sme.utils.role_user import RoleUser, role_required
from ethiens_sme.utils.exception.exceptions import ApiException
from ethiens_sme.service import seance_service

seance = Blueprint("seance", __name__, url_prefix="/seance")


@seance.route("", methods=["POST"])
@role_required(RoleUser.DRIVER)
def add_car_information():
    """Add seance car endpoint"""
    try:
        json_object = request.json
        validate_fields(
            json_object,
            {
                "model": str,
                "license_plate": str,
                "country_license_plate": str,
                "color": str,
                "brand": str,
                "total_places": int,
            },
        )
        car_bo = CarBO(
            model=json_object.get("model").strip(),
            license_plate=json_object.get("license_plate").strip(),
            country_license_plate=json_object.get("country_license_plate").strip(),
            color=json_object.get("color").strip(),
            brand=json_object.get("brand").strip(),
            total_places=json_object.get("total_places"),
            user_id=["id"],
        )
        add_car(car_bo)
        response = jsonify({"message": "CAR_CREATED_SUCCESSFULLY", "id_car": car_bo.id}), 200
    except ApiException as e:
        response = jsonify({"message": e.message}), e.status_code
    return response


@seance.route("/<ville_name>", methods=["GET"])
@role_required(RoleUser.DRIVER)
def get_seances_by_city(ville_name):
    """Get information about the seance's car endpoint"""
    try:
        available_seance = seance_service.get_seance_info_by_city_name(ville_name)
        response = jsonify(available_seance), 200
    except ApiException as e:
        response = jsonify({"message": e.message}), e.status_code
    return response
