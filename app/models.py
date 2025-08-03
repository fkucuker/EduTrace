from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    isim = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sifre_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='Personel')  # Admin, Eğitmen, Personel
    bolum_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # İlişkiler
    bolum = db.relationship('Department', backref='kullanicilar')
    egitimler = db.relationship('UserTraining', back_populates='kullanici', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.sifre_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.sifre_hash, password)
    
    def is_admin(self):
        return self.rol == 'Admin'
    
    def is_egitmen(self):
        return self.rol == 'Eğitmen'
    
    def __repr__(self):
        return f'<User {self.isim}>'

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), unique=True, nullable=False)
    aciklama = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    egitimler = db.relationship('TrainingSection', back_populates='bolum', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Department {self.ad}>'

class Level(db.Model):
    __tablename__ = 'levels'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50), unique=True, nullable=False)  # Temel, Orta, İleri
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    egitim_bolumleri = db.relationship('TrainingSection', back_populates='seviye')
    
    def __repr__(self):
        return f'<Level {self.ad}>'

class Training(db.Model):
    __tablename__ = 'trainings'
    
    id = db.Column(db.Integer, primary_key=True)
    kod = db.Column(db.String(20), unique=True, nullable=False)
    baslik = db.Column(db.String(200), nullable=False)
    aciklama = db.Column(db.Text)
    pre_requisite_id = db.Column(db.Integer, db.ForeignKey('trainings.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    pre_requisite = db.relationship('Training', remote_side=[id], backref='dependent_trainings')
    bolumler = db.relationship('TrainingSection', back_populates='egitim', cascade='all, delete-orphan')
    kullanicilar = db.relationship('UserTraining', back_populates='egitim', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Training {self.kod}: {self.baslik}>'

class TrainingSection(db.Model):
    __tablename__ = 'training_sections'
    
    id = db.Column(db.Integer, primary_key=True)
    egitim_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=False)
    bolum_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    seviye_id = db.Column(db.Integer, db.ForeignKey('levels.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    egitim = db.relationship('Training', back_populates='bolumler')
    bolum = db.relationship('Department', back_populates='egitimler')
    seviye = db.relationship('Level', back_populates='egitim_bolumleri')
    
    # Benzersizlik kısıtı
    __table_args__ = (db.UniqueConstraint('egitim_id', 'bolum_id', name='_egitim_bolum_uc'),)
    
    def __repr__(self):
        return f'<TrainingSection {self.egitim.kod} - {self.bolum.ad} - {self.seviye.ad}>'

class UserTraining(db.Model):
    __tablename__ = 'user_trainings'
    
    id = db.Column(db.Integer, primary_key=True)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    egitim_id = db.Column(db.Integer, db.ForeignKey('trainings.id'), nullable=False)
    durum = db.Column(db.String(20), nullable=False, default='baslamadi')  # baslamadi, devam, tamamlandi
    tamamlanma_tarihi = db.Column(db.DateTime)
    baslama_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    kullanici = db.relationship('User', back_populates='egitimler')
    egitim = db.relationship('Training', back_populates='kullanicilar')
    
    # Benzersizlik kısıtı
    __table_args__ = (db.UniqueConstraint('kullanici_id', 'egitim_id', name='_kullanici_egitim_uc'),)
    
    def __repr__(self):
        return f'<UserTraining {self.kullanici.isim} - {self.egitim.kod} - {self.durum}>' 