from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User ,SkorUser
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route("login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        usernameForm = request.form.get('username')
        passwordForm = request.form.get('password')
        user = User.query.filter_by(username = usernameForm).first()
        if user:
            if check_password_hash(user.password, passwordForm):
                flash("Login in Successfully!", category='success')
                login_user(user)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password !!, please try again", category='error')
        else:
            flash('username does not exist', category='error')
        
    return render_template("Login.html.jinja")


@auth.route("logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    
    
@auth.route("register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        usernameForm = request.form.get('username')
        passwordForm = request.form.get('password')
        confirmPasswordForm = request.form.get('confirmPassword')
        nickNameForm = request.form.get('nickName')
    
        user = User.query.filter_by(username = usernameForm).first()
        if user:
            flash('username already exist', category='error')
        elif len(passwordForm) < 8:
            flash('password minimal 8 character', category='error')
        elif confirmPasswordForm != passwordForm:
            flash('confirmasi password tidak sama dengan password', category='error')
        else:
            newUser = User(
                username = usernameForm,
                password = generate_password_hash(passwordForm,method='pbkdf2:sha256', salt_length=8),
                nickname = nickNameForm,
            )

            db.session.add(newUser)
            db.session.commit()
            user = User.query.filter_by(username = usernameForm).first()
            db.session.add(
                SkorUser(idUser=user.id, skor=0)
            )
            db.session.commit()
            
            flash('Account created!', category='success')

            return redirect(url_for('auth.login'))
    
    return render_template("Register.html.jinja")
