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
from PIL import Image



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
                # convert PIL.Image.Image object and resize image
                photo = Image.open(photo)
                photo = photo.convert(mode='RGB')
                photo = photo.resize(size=(200, 200))
                photo_filename = '{}.jpg'.format(user.user_id)
                photo.save('./id_card/static/img/profiles/{}.jpg'.format(user.user_id))
            if sign.filename != '':
                sign_filename = '{}.jpg'.format(user.user_id)
                sign.save('./id_card/static/img/signs/{}.jpg'.format(user.user_id))
            db.session.commit()
            flash('Update Successful', 'info')
            return redirect(url_for('.index', id=id))
        except KeyError:
            flash('Please upload a profile photo and a signature', 'warning')
            return redirect(url_for('.index', id=id))
    return render_template('student/profile.html', form=form)


@student.route('/preview_info/<int:id>')
@login_required
def preview_info(id):
    """Enables the students to preview the information they have updated on their profiles, specifically the ones that will appear on the ID cards. They are notified of any missing fields.
    If QR code is missing, generate one here for the student and save the file.
    
    Keyword arguments:
    id -- user ID
    Return: template of preview_info
    """
    user = User.query.get(id)
    # ensuring necessary fields are filled
    # req_fields = {
    #     'First Name': user.first_name, 
    #     'Last Name': user.last_name, 
    #     'Gender': user.gender,
    #     'Date of Birth': user.dob, 
    #     'Phone Number': user.number, 
    #     'Next of Kin Fullname':user.nok_fullname, 
    #     'Next of Kin Address':user.nok_address, 
    #     'Next of Kind Phone No.':user.nok_number
    # }
    # fields = []
    # for k, v in req_fields.items():
    #     if v is None or v == '':
    #         fields.append(k)
    response = user.check_id_ready()
    # checking if QR code was generated
    qr_exists = False
    for _, _, files in os.walk('./id_card/static/img/qrs'):
        for file in files:
            if file.startswith(user.user_id):
                qr_exists = True
                break
    # generate QR if not found
    if not qr_exists:
        # generate full URL with token as QR data
        data = '{}/{}'.format('https://idcard.onrender.com/verify_id', user.id)
        qr = qrcode.make(
            data=data,
            box_size=2,
            border=2
        )
        qr.save('./id_card/static/img/qrs/{}.jpg'.format(user.user_id))
    return render_template('student/preview_info.html', fields=response['fields'])


@student.route('/verify_id/<int:id>')
def verify_id(id):
    """Performs the verification of the ID card QR code after scanning it"""
    user = User.query.get(id)
    if user is not None:
        # return card page if user exist
        return redirect(url_for('.card', id=id))
    # abort if student not found
    else:
        abort(404)


@student.route('/card/<int:id>')
def card(id):
    user = User.query.get(id)
    return render_template('student/card.html', user=user)


@student.route('/digital_id/<int:id>')
@login_required
def digital_id(id):
    user = User.query.get(id)
    return render_template('student/digital_id.html')