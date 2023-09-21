from . import student
from .forms import Registration
from ..models import User
from .. import db
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    current_app,
    flash,
    abort
)
from flask_login import login_required
import os
import qrcode
from werkzeug.security import check_password_hash



@student.route('/profile/<int:id>', methods=['GET', 'POST', 'PUT'])
@login_required
def index(id):
    user = User.query.get(id)
    form = Registration(obj=user)
    if form.is_submitted():
        try:
            # personal info update
            user.first_name = form.first_name.data
            user.middle_name = form.middle_name.data
            user.last_name = form.last_name.data
            user.user_id = form.user_id.data
            user.email = form.email.data
            user.number = form.number.data
            user.dob = form.dob.data
            user.state_of_origin = form.state_of_origin.data
            user.address = form.address.data

            # next of kin info
            user.nok_fullname = form.nok_fullname.data
            user.nok_address = form.nok_address.data
            user.nok_number = form.nok_number.data

            # file uploads
            photo = form.photo.data
            sign = form.signature.data

            # checking if files were uploaded before saving/overwriting
            if photo.filename != '':
                photo_filename = '{}.jpg'.format(
                    user.user_id,
                    photo.filename.split('.')[-1]
                )
                photo.save(os.path.join(current_app.config['PROFILE_FOLDER'], photo_filename))
            if sign.filename != '':
                sign_filename = '{}.jpg'.format(
                    user.user_id,
                    sign.filename.split('.')[-1]
                )
                sign.save(os.path.join(current_app.config['SIGN_FOLDER'], sign_filename))
            db.session.commit()
            flash('Update Successful', 'info')
            return redirect(url_for('.index', id=id))
        except:
            flash('Please upload a profile photo and a signature', 'warning')
            return redirect(url_for('.index', id=id))
    return render_template('student/profile.html', form=form, id=id, user=user)


@student.route('/preview_info/<int:id>')
@login_required
def preview_info(id):
    """Enables the students to preview the information they have updated on their profiles, specifically the ones that will appear on the ID cards. They are notified of any missing fields.
    
    Keyword arguments:
    id -- user ID
    Return: template of preview_info
    """
    user = User.query.get(id)
    return render_template('student/preview_info.html', id=id, user=user)


@student.route('/verify_id/<int:id>/<token>')
@login_required
def verify_id(id, token):
    """Performs the verification of the ID card QR code after scanning it"""
    user = User.query.get(id)
    if check_password_hash(token, user.user_id):
        # else return student ID
        return redirect(url_for('.card'))
    # abort if ID verification fails
    else:
        abort(404)


@student.route('/card/<int:id>')
@login_required
def card(id):
    user = User.query.get(id)
    return render_template('student/card.html', id=id, user=user)


@student.route('/digital_id/<int:id>')
@login_required
def digital_id(id):
    user = User.query.get(id)
    
    return render_template('student/digital_id.html', user=user, id=id)