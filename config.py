"""
Configuration file for necessary variables
"""
import os



class Config:
    """"Development configuration class."""
    SECRET_KEY = 'asdmnc5b4734-+*23'
    # CSRF_TOKEN = 'fmn3c7(#&(3misaER'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///id_card.db'
    PROFILE_FOLDER = './id_card/static/img/profiles'
    SIGN_FOLDER = './id_card/static/img/signs'
    QR_FOLDER = './id_card/static/img/qrs'
    # need this for some weird reason I cannot remember
    @staticmethod
    def init_app():
        pass