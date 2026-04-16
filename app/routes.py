from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User, Message
from .forms import RegisterForm, LoginForm, ProfileForm
from sqlalchemy import or_

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Đăng ký thành công! Hãy đăng nhập.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Email hoặc mật khẩu sai!', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.school = form.school.data
        current_user.district = form.district.data
        current_user.teach_skills = form.teach_skills.data
        current_user.learn_skills = form.learn_skills.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Cập nhật profile thành công!', 'success')
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.school.data = current_user.school
        form.district.data = current_user.district
        form.teach_skills.data = current_user.teach_skills
        form.learn_skills.data = current_user.learn_skills
        form.bio.data = current_user.bio
    return render_template('profile.html', form=form)

@main_bp.route('/matches')
@login_required
def matches():
    # Tìm người có kỹ năng trùng
    my_teach = [s.strip().lower() for s in (current_user.teach_skills or '').split(',') if s.strip()]
    my_learn = [s.strip().lower() for s in (current_user.learn_skills or '').split(',') if s.strip()]
    
    users = User.query.filter(User.id != current_user.id).all()
    results = []
    for u in users:
        their_teach = [s.strip().lower() for s in (u.teach_skills or '').split(',') if s.strip()]
        their_learn = [s.strip().lower() for s in (u.learn_skills or '').split(',') if s.strip()]
        match_score = len(set(my_learn) & set(their_teach)) + len(set(my_teach) & set(their_learn))
        if match_score > 0:
            results.append((u, match_score))
    results.sort(key=lambda x: x[1], reverse=True)
    return render_template('matches.html', results=results)

@main_bp.route('/chat/<int:user_id>')
@login_required
def chat(user_id):
    other = User.query.get_or_404(user_id)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp).all()
    return render_template('chat.html', other=other, messages=messages)

@main_bp.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.points.desc()).limit(20).all()
    return render_template('leaderboard.html', users=users)