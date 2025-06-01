from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models.user import User
import re

def validate_password_complexity(form, field):
    password = field.data
    
    if not re.search(r'\d', password):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру')
    
    if not re.search(r'[A-ZА-Я]', password):
        raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('Пароль должен содержать хотя бы один специальный символ')

class UnifiedRegistrationForm(FlaskForm):
    role = SelectField('Выберите роль', choices=[
        ('candidate', 'Кандидат'),
        ('employer', 'Работодатель')
    ], validators=[DataRequired(message='Пожалуйста, выберите роль')])

    email = StringField('Email', validators=[
        DataRequired(message='Введите email'),
        Email(message='Введите корректный email')
    ])
    
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Введите пароль'),
        Length(min=8, message='Пароль должен быть не менее 8 символов'),
        validate_password_complexity
    ])
    
    password2 = PasswordField('Повторите пароль', validators=[
        DataRequired(message='Повторите пароль'),
        # Явная проверка совпадения паролей
        EqualTo('password', message='Пароли должны совпадать')
    ])

    # ... остальные поля ...

    submit = SubmitField('Зарегистрироваться')

    def validate(self, extra_validators=None):
        # Вызов стандартной валидации FlaskForm
        initial_validation = super().validate(extra_validators)
        if not initial_validation:
            return False
        
        # Дополнительная проверка совпадения паролей (на случай, если EqualTo не сработал)
        if self.password.data != self.password2.data:
            self.password2.errors.append('Пароли не совпадают')
            return False
        
        return True

    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError('Пользователь с таким email уже существует.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[
        DataRequired(),
        Length(min=8, message='Пароль должен быть не менее 8 символов'),
        validate_password_complexity
    ])
    
    password2 = PasswordField('Повторите пароль', validators=[
    DataRequired(message='Повторите пароль'),
    EqualTo('password', message='Пароли должны совпадать')
])
    
    submit = SubmitField('Изменить пароль')

    def validate(self, extra_validators=None):
        initial_validation = super().validate(extra_validators)
        if not initial_validation:
            return False
        
        if self.password.data != self.password2.data:
            self.password2.errors.append('Пароли не совпадают')
            return False
        
        return True