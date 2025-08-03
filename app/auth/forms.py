from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User, Department

class LoginForm(FlaskForm):
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember_me = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')

class RegistrationForm(FlaskForm):
    isim = StringField('Ad Soyad', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Şifre Tekrar', validators=[DataRequired(), EqualTo('password')])
    rol = SelectField('Rol', choices=[
        ('Personel', 'Personel'),
        ('Eğitmen', 'Eğitmen'),
        ('Admin', 'Admin')
    ], validators=[DataRequired()])
    bolum_id = SelectField('Bölüm', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Kayıt Ol')
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.bolum_id.choices = [(d.id, d.ad) for d in Department.query.all()]
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Bu e-posta adresi zaten kullanılıyor.')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Mevcut Şifre', validators=[DataRequired()])
    new_password = PasswordField('Yeni Şifre', validators=[DataRequired(), Length(min=6)])
    new_password2 = PasswordField('Yeni Şifre Tekrar', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Şifre Değiştir') 