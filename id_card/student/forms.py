from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SelectField,
    FileField,
    EmailField,
    TelField,
    SubmitField,
    DateField,
    TextAreaField
)
from wtforms.validators import Email



class Registration(FlaskForm):
    photo = FileField(label='Upload Profile Picture')
    signature = FileField(label='Upload signature')
    user_id = StringField(label="Registration Number", render_kw={
        'placeholder': 'Registration Number',
        'readonly': 'readonly'
    })
    first_name = StringField(label="First Name", render_kw={
        'placeholder': 'First Name',
        'readonly': 'readonly'
    })
    middle_name = StringField(label="Middle Name", render_kw={
        'placeholder': 'Middle Name',
        'readonly': 'readonly'
    })
    last_name = StringField(label="Last Name", render_kw={
        'placeholder': 'Last Name',
        'readonly': 'readonly'
    })
    email = EmailField(label="E-mail", render_kw={
        'placeholder': 'Email'
    }, validators=[Email()])
    number = TelField(label="Number", render_kw={
        'placeholder': 'Number'
    })
    address = TextAreaField(label="Address", render_kw={
        'placeholder': 'Address'
    })
    state_of_origin = SelectField(label="State of Origin", choices=[
        'Abia',
        'Adamawa',
        'Akwa Ibom',
        'Anambra',
        'Bauchi',
        'Bayelsa',
        'Benue',
        'Borno',
        'Cross River',
        'Delta',
        'Ebonyi',
        'Edo',
        'Ekiti',
        'Enugu',
        'Gombe',
        'Imo',
        'Jigawa',
        'Kaduna',
        'Kano',
        'Katsina',
        'Kebbi',
        'Kogi',
        'Kwara',
        'Lagos',
        'Nasarawa',
        'Niger',
        'Ogun',
        'Ondo',
        'Osun',
        'Oyo',
        'Plateau',
        'Rivers',
        'Sokoto',
        'Taraba',
        'Yobe',
        'Zamfara',
        'F.C.T. Abuja'
    ])
    dob = DateField(label='Date of Birth')

    # next of kin information
    nok_fullname = StringField(label='Next of Kin', render_kw={
        'placeholder': 'Fullname'
    })
    nok_address = TextAreaField(label='Address', render_kw={
        'placeholder': 'Address'
    })
    nok_number = TelField(label='Contact Phone', render_kw={
        'placeholder': 'Phone Number'
    })
    save = SubmitField(label='Save Changes')