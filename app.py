from id_card import db, create_app
from id_card.models import User
from config import Config
from flask import (
    render_template, 
    request,
    url_for, 
    redirect,
    flash
)
from flask_login import (
    login_user, 
    login_required,
    logout_user
)
from datetime import timedelta



app = create_app(Config)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        user = User.query.filter_by(user_id=user_id).first()
        if user is not None and user.check_password(password):
            if not user.is_active:
                flash('User is inactive, contact an admin', 'warning')
                return redirect(url_for('login'))
            login_user(user, request.form.get('remember_me'))
            endpoint = '{}.index'.format(user.role.lower())
            next = url_for(endpoint, id=user.id)
            return redirect(next)
        flash('Incorrect user ID or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# @app.before_request
# @login_required
# def before_request():
#     """A before app request handler for refreshing all ID statuses"""
#     users = User.query.filter_by(role='STUDENT')
#     for user in users:
#         response = user.check_id_status()
#         if response.get('status') is True:
#             user.id_ready = True
#         user.refresh_status()
#     db.session.commit()


@app.shell_context_processor
def context_processor():
    return dict(db=db, User=User)