import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'smart_home_key'
    APP_NAME = os.environ.get('APP_NAME') or 'Smart Home'
    SUPERUSERS = {'admin': 'admin'}
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                           'postgresql+psycopg2://postgres:05112002@localhost:5432/Smart_Home'

    SQLALCHEMY_DATABASE_URI = 'postgresql://test_db_oxfr_user:a7MTlLQm0MAK9mA2FpMrxYc0KaFepKXa@dpg-cplkcddds78s73elrsog-a.oregon-postgres.render.com/test_db_oxfr'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mysmarthomeproject2911@gmail.com'
    MAIL_PASSWORD = 'smarthome2911'
    ADMINS = ['mysmarthomeproject2911@gmail.com']