"""Rest API"""

from flask import redirect, url_for, render_template
from ethiens_sme import app, jwt
from ethiens_sme.route.user_route import user
from ethiens_sme.route.seance_route import seance
from ethiens_sme.route.movie_route import movie
from ethiens_sme.route.frontend_route import frontend


@app.errorhandler(401)
def unauthorized(error):
    # Hide the existence of the page by showing 404 instead of redirecting to login
    # or showing a JSON error.
    return render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@jwt.unauthorized_loader
def my_unauthorized_callback(reason):
    # Missing cookie or header
    return render_template('404.html'), 404

@jwt.invalid_token_loader
def my_invalid_token_callback(reason):
    # Invalid token
    return render_template('404.html'), 404

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    # Expired token
    return render_template('404.html'), 404

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
        use_reloader=False # Disable reloader in parent process when running with debug=True
    )
