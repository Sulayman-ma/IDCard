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
            # with remember me token for 1 day
            login_user(user, duration=timedelta(days=1))
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


@app.shell_context_processor
def context_processor():
    return dict(db=db, User=User)