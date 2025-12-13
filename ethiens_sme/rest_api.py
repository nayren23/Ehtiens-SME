"""Rest API"""

from ethiens_sme import app
from ethiens_sme.route.user_route import user
from ethiens_sme.route.seance_route import seance
from ethiens_sme.route.movie_route import movie
from ethiens_sme.route.frontend_route import frontend

if __name__ == "__main__":
    app.register_blueprint(user)
    app.register_blueprint(seance)
    app.register_blueprint(movie)
    app.register_blueprint(frontend)

    # Launch Flask server
    app.run(
        debug=app.config["FLASK_DEBUG"],
        host=app.config["FLASK_HOST"],
        port=app.config["FLASK_PORT"],
    )
