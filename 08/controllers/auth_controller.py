from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Profile

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['username'] = user.username
            return redirect('/')
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        if User.query.filter_by(username=request.form['username']).first():
            return render_template('register.html', error="Username taken")
        user = User(
            username=request.form['username'],
            password=generate_password_hash(request.form['password'])
        )
        db.session.add(user)
        db.session.commit()
        profile = Profile(user_id=user.id, name="")
        db.session.add(profile)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/login')
    user = User.query.filter_by(username=session['username']).first()
    if request.method == "POST":
        user.profile.name = request.form['name']
        db.session.commit()
    return render_template('profile.html', profile=user.profile)
