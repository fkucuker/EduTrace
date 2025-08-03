from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.models import User, Department

class ProfileForm(FlaskForm):
    isim = StringField('Ad Soyad', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    bolum_id = SelectField('Bölüm', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Profili Güncelle')
    
    def __init__(self, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
        self.bolum_id.choices = [(d.id, d.ad) for d in Department.query.all()]
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Bu e-posta adresi zaten kullanılıyor.') 