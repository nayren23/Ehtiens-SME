import os
import sys

# Ensure the current directory (project root) is in sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from ethiens_sme import app
import ethiens_sme.rest_api # Register error handlers
from ethiens_sme.route.user_route import user
from ethiens_sme.route.seance_route import seance
from ethiens_sme.route.movie_route import movie
from ethiens_sme.route.frontend_route import frontend

# Register Blueprints (since rest_api.py only does it in its main block)
if 'user' not in app.blueprints:
    app.register_blueprint(user)
if 'seance' not in app.blueprints:
    app.register_blueprint(seance)
if 'movie' not in app.blueprints:
    app.register_blueprint(movie)
if 'frontend' not in app.blueprints:
    app.register_blueprint(frontend)

if __name__ == "__main__":
    print("Starting Eh Tiens! Server...")
    print(f"Access the app at: {os.getenv('FRONT_END_URL', 'http://localhost:5000')}")
    app.run(
        debug=os.getenv("FLASK_DEBUG", "True") == "True",
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_PORT", 5000))
    )