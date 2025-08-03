from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, SelectMultipleField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
from app.models import Department, Training, Level, User

class DepartmentForm(FlaskForm):
    ad = StringField('Bölüm Adı', validators=[DataRequired(), Length(min=2, max=100)])
    aciklama = TextAreaField('Açıklama', validators=[Length(max=500)])
    submit = SubmitField('Kaydet')
    
    def validate_ad(self, ad):
        department = Department.query.filter_by(ad=ad.data).first()
        if department is not None and hasattr(self, '_obj') and department != self._obj:
            raise ValidationError('Bu bölüm adı zaten kullanılıyor.')

class TrainingForm(FlaskForm):
    kod = StringField('Eğitim Kodu', validators=[DataRequired(), Length(min=2, max=20)])
    baslik = StringField('Eğitim Başlığı', validators=[DataRequired(), Length(min=5, max=200)])
    aciklama = TextAreaField('Açıklama', validators=[Length(max=1000)])
    pre_requisite_id = SelectField('Ön Koşul Eğitim', coerce=int, default=0)
    submit = SubmitField('Kaydet')
    
    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.pre_requisite_id.choices = [(0, 'Ön koşul yok')] + [(t.id, f"{t.kod} - {t.baslik}") for t in Training.query.all()]
    
    def validate_kod(self, kod):
        training = Training.query.filter_by(kod=kod.data).first()
        if training is not None and hasattr(self, '_obj') and training != self._obj:
            raise ValidationError('Bu eğitim kodu zaten kullanılıyor.')

class TrainingSectionForm(FlaskForm):
    egitim_id = SelectField('Eğitim', coerce=int, validators=[DataRequired()])
    bolum_id = SelectField('Bölüm', coerce=int, validators=[DataRequired()])
    seviye_id = SelectField('Seviye', coerce=int, validators=[DataRequired()])
    submit = SubmitField('İlişkilendir')
    
    def __init__(self, *args, **kwargs):
        super(TrainingSectionForm, self).__init__(*args, **kwargs)
        self.egitim_id.choices = [(t.id, f"{t.kod} - {t.baslik}") for t in Training.query.all()]
        self.bolum_id.choices = [(d.id, d.ad) for d in Department.query.all()]
        self.seviye_id.choices = [(l.id, l.ad) for l in Level.query.all()]

class UserAssignmentForm(FlaskForm):
    kullanici_id = SelectField('Kullanıcı', coerce=int, validators=[DataRequired()])
    egitim_ids = SelectMultipleField('Eğitimler', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Ata')
    
    def __init__(self, *args, **kwargs):
        super(UserAssignmentForm, self).__init__(*args, **kwargs)
        self.kullanici_id.choices = [(u.id, f"{u.isim} ({u.email})") for u in User.query.all()]
        self.egitim_ids.choices = [(t.id, f"{t.kod} - {t.baslik}") for t in Training.query.all()]

class UserForm(FlaskForm):
    isim = StringField('Ad Soyad', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    rol = SelectField('Rol', choices=[
        ('Personel', 'Personel'),
        ('Eğitmen', 'Eğitmen'),
        ('Admin', 'Admin')
    ], validators=[DataRequired()])
    bolum_id = SelectField('Bölüm', coerce=int, default=0)
    is_active = BooleanField('Aktif')
    submit = SubmitField('Kaydet')
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.bolum_id.choices = [(0, 'Bölüm seçiniz')] + [(d.id, d.ad) for d in Department.query.all()]
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None and hasattr(self, '_obj') and user != self._obj:
            raise ValidationError('Bu e-posta adresi zaten kullanılıyor.')

class UserPasswordForm(FlaskForm):
    password = PasswordField('Yeni Şifre', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Şifre Tekrar', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Şifreyi Değiştir') 