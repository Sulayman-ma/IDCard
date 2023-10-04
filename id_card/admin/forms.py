from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SelectField,
    EmailField,
    TelField,
    SubmitField,
    DateField,
    BooleanField
)
from wtforms.validators import Email



class EditStudent(FlaskForm):
    user_id = StringField(label="Registration Number", render_kw={
        'placeholder': 'Registration Number',
        'readonly': 'readonly'
    })
    first_name = StringField(label="First Name", render_kw={
        'placeholder': 'First Name'
    })
    middle_name = StringField(label="Middle Name", render_kw={
        'placeholder': 'Middle Name'
    })
    last_name = StringField(label="Last Name", render_kw={
        'placeholder': 'Last Name'
    })
    email = EmailField(label="E-mail", render_kw={
        'placeholder': 'Email'
    }, validators=[Email()])
    number = TelField(label="Number", render_kw={
        'placeholder': 'Number'
    })
    address = StringField(label="Address", render_kw={
        'placeholder': 'Address'
    })
    rusticated = BooleanField()
    dob = DateField(label='Date of Birth')
    is_active = BooleanField()
    save = SubmitField(label='Save Changes')
    
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