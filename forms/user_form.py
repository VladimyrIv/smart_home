from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, DateField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange, InputRequired
from app.models.Users import Users


class RegistrationForm(FlaskForm):
    username = StringField("Ім'я", validators=[DataRequired()])
    # address = SelectField(
    #     'Адреса',
    #     choices=[
    #         ('м. Одеса, Одеська обл., вул. Щепкіна, буд. 2', 'м. Одеса, Одеська обл., вул. Щепкіна, буд. 2'),
    #         ('м. Дніпро, Дніпропетровська обл., вул. Соборна, буд. 49', 'м. Дніпро, Дніпропетровська обл., вул. Соборна, буд. 49'),
    #         ('м. Рені, Одеська обл., вул. Шевченка, буд. 24', 'м. Рені, Одеська обл., вул. Шевченка, буд. 24')
    #     ]
    # )
    phone = StringField('Телефон', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторіть пароль', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Зареєструватися')

    def validate_phone(self, phone):
        user = Users.query.filter_by(phone=phone.data).first()
        if user is not None:
            raise ValidationError('Акаунт з даним номером вже існує.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Акаунт з даною поштою вже існує.')


class LoginForm(FlaskForm):
    phone = StringField("Телефон", validators=[InputRequired()])
    password = PasswordField("Пароль", validators=[InputRequired()])
    remember = BooleanField("Залишатись в системі")
    submit = SubmitField("Увійти")


class EditProfileForm(FlaskForm):
    username = StringField("Прізвище", validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Зберегти зміни')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Поточний пароль', validators=[DataRequired()])
    new_password = PasswordField('Новий пароль', validators=[DataRequired()])
    confirm_new_password = PasswordField('Підтвердіть новий пароль',
                                         validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Змінити пароль')


