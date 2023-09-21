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
    course = db.Column(db.String(64), nullable=False)
    department = db.Column(db.String(64), nullable=False)
    expiry_date = db.Column(db.Date)
    email = db.Column(db.String(128), nullable=False, unique=True)
    number = db.Column(db.String(64))
    address = db.Column(db.String(128))

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
    is_active = db.Column(db.BOOLEAN, default=True)
    

    """RELATIONSHIPS"""


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
        token = generate_password_hash(self.user_id)
        data = url_for('student.verify', id=self.id, token=token, _external=True)
        qr = qrcode.make(
            data=data,
            box_size=2,
            border=2
        )
        qr.save('./id_card/static/img/qrs/{}.jpg'.format(self.user_id))

    def __repr__(self) -> str:
        return '<{} - {}>'.format(self.role, self.user_id)

    """STATIC AND CLASS METHODS"""
    def generate_verify_token(self):
        pass

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
                'Zamfara'
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
                number = '0{}'.format(faker.msisdn()[:10]),
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
                nok_number = '0{}'.format(faker.msisdn()),
                role = 'STUDENT',
                password = 'pass'
            )
            db.session.add(user)
        db.session.commit()
    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)