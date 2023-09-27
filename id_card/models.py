from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager
from faker import Faker
from faker.providers import DynamicProvider, BaseProvider
from random import Random
import qrcode
from flask import current_app, url_for
import os



class User(db.Model, UserMixin):
    """Base user model for appliactiion."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # `user_id` will serve as both reg number and admin ID
    user_id = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    gender = db.Column(db.CHAR)
    state_of_origin = db.Column(db.String(64))
    blood_group = db.Column(db.String(5))
    dob = db.Column(db.Date)
    course = db.Column(db.String(64))
    department = db.Column(db.String(64))
    expiry_date = db.Column(db.Date)
    email = db.Column(db.String(128), unique=True, nullable=False)
    number = db.Column(db.String(64))
    address = db.Column(db.String(128))
    id_ready = db.Column(db.BOOLEAN, default=False)
    rusticated = db.Column(db.BOOLEAN, default=False)

    # next of kin information
    nok_fullname = db.Column(db.String(128))
    nok_address = db.Column(db.String(128))
    nok_number = db.Column(db.String(64))

    """ User role column instead of Role model.
    Roles are:
    : STUDENT
    : ADMIN
    """
    role = db.Column(db.String(64), nullable=False)
    # set to False when student graduates or leaves the school for any reason
    is_active = db.Column(db.BOOLEAN, default=True)

    """PASSWORD METHODS AND VERIFICATION"""
    @property
    def password(self) -> AttributeError:
        raise AttributeError('PROPERTY NOT ACCESSIBLE')

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    """----------------------------------------------------------"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # generate live Render URL with token as QR data
        # token = generate_password_hash(self.user_id)
        # data = '{}/{}/{}'.format('https://idcard.onrender.com', self.id, token)

        # qr = qrcode.make(
        #     data=data,
        #     box_size=2,
        #     border=2
        # )
        # qr.save('./id_card/static/img/qrs/{}.jpg'.format(self.user_id))

    def __repr__(self) -> str:
        return '<{} - {}>'.format(self.role, self.user_id)

    """STATIC AND CLASS METHODS"""
    def check_id_status(self) -> dict:
        """Checks if the student ID is ready by querying against the necessary fields that are to appear on the ID card. Including the ID picture and the signature.
        
        Keyword arguments:
        self -- instance reference
        Return: Dictionary
        """
        req_fields = {
            'First Name': self.first_name, 
            'Last Name': self.last_name, 
            'Gender': self.gender,
            'Date of Birth': self.dob, 
            'Phone Number': self.number, 
            'Next of Kin Fullname':self.nok_fullname, 
            'Next of Kin Address':self.nok_address, 
            'Next of Kind Phone No.':self.nok_number
        }
        response = {'status': True, 'fields':[]}
        for k, v in req_fields.items():
            if v is None or v == '':
                response['fields'].append(k)
        if len(response['fields']) > 0:
            response['status'] = False
        id_exists = False
        sign_exists = False
        # querying for ID and signature
        for _, _, files in os.walk(os.path.join(current_app.config['PROFILE_FOLDER'])):
            for file in files:
                if file.startswith(self.user_id):
                    id_exists = True
                    break
        for _, _, files in os.walk(os.path.join(current_app.config['SIGN_FOLDER'])):
            for file in files:
                if file.startswith(self.user_id):
                    sign_exists = True
                    break
        if not id_exists:
            response['fields'].append('Profile Picture')
        if not sign_exists:
            response['fields'].append('Signature')
        return response
        

    # def refresh_status(self) -> None:
    #     """Refresh student's ID status by checking expiry date.
        
    #     Keyword arguments:
    #     self -- class instance
    #     Return: None
    #     """
    #     date = datetime.today().date()
    #     # if ID has expired
    #     if date <= self.expiry_date:
    #         self.id_status = 'EXPIRED'
    #     db.session.commit()


    def generate_users(number: int) -> None:
        """Generates fake students to populate the database with, with all names included, email and every other detail. Custom fields are added using custom dynamic providers.
        
        Keyword arguments:
        number -- Number of student records to generate
        Return: adds each student record to the database
        """
        faker = Faker()

        # custom dynamic providers
        departments_provider = DynamicProvider(
            provider_name='department',
            elements=[
                'Computer Science', 'Mathematics', 'Statistics', 'Physics', 'Chemistry', 'Geography', 'Geology'
            ]
        )
        courses_provider = DynamicProvider(
            provider_name='course',
            elements=[
                'B.Sc. Computer Science', 'B.Sc Mathematics', 'B.Sc. Statistics', 'B.Sc. Chemistry', 'B.Sc. Geography', 'B.Sc. Geology'
            ]
        )
        states_provider = DynamicProvider(
            provider_name='state',
            elements=[
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
            ]
        )
        reg_prefix = DynamicProvider(
            provider_name='prefix',
            elements=['CS', 'MT', 'ST', 'PH', 'CH', 'GG', 'GL']
        )
        faker.add_provider(departments_provider)
        faker.add_provider(courses_provider)
        faker.add_provider(states_provider)
        faker.add_provider(reg_prefix)

        r = Random()

        available = [str(r.randint(1, 200)) for _ in range(number)]
        for _ in range(number):
            # each student instance
            user = User(
                user_id = 'U17{}{}'.format(
                    faker.prefix(), 
                    available.pop().zfill(4)
                ),
                first_name = faker.first_name(),
                middle_name = faker.first_name(),
                last_name = faker.last_name(),
                number = '080{}'.format(faker.msisdn()[:8]),
                blood_group = faker.profile()['blood_group'],
                gender = faker.profile()['sex'],
                email = faker.email(),
                state_of_origin = faker.state(),
                address = faker.address(),
                course = faker.course(),
                expiry_date = datetime.strptime(faker.date(), "%Y-%m-%d").date(),
                dob = datetime.strptime(faker.date(), "%Y-%m-%d").date(),
                department = faker.department(),
                
                # next of kin stuff
                nok_fullname = faker.name(),
                nok_address = faker.address(),
                nok_number = '070{}'.format(faker.msisdn()[:8]),
                role = 'STUDENT',
                password = 'pass'
            )
            db.session.add(user)
        db.session.commit()
    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)