from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/seance')
def seance():
    return render_template('seance.html')

@frontend.route('/login')
def login():
    return render_template('login.html')

@frontend.route('/admin/dashboard')
@jwt_required()
def admin_dashboard():
    # In a real app, check for session/auth here or handle redirect in JS if 401
    return render_template('dashboard.html')

@frontend.route('/admin/movie/add')
@jwt_required()
def add_movie():
    return render_template('add_movie.html')

@frontend.route('/admin/seance/add')
@jwt_required()
def add_seance():
    return render_template('add_seance.html')

@frontend.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    return render_template('movie_detail.html', movie_id=movie_id)

@frontend.route('/cinema/<int:cinema_id>')
def cinema_detail(cinema_id):
    return render_template('cinema_detail.html', cinema_id=cinema_id)
