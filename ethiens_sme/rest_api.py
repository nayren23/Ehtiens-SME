"""Rest API"""

from ethiens_sme import app
from ethiens_sme.route.user_route import user

if __name__ == "__main__":
    app.register_blueprint(user)

    # Launch Flask server
    app.run(
        debug=app.config["FLASK_DEBUG"],
        host=app.config["FLASK_HOST"],
        port=app.config["FLASK_PORT"],
    )
