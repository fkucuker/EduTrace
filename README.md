# Eğitim Yönetim Sistemi

Flask ve SQLite ile geliştirilmiş modern bir eğitim yönetimi ve takip sistemi.

## 🚀 Özellikler

### Yönetim Paneli
- **Bölüm Yönetimi**: Yeni bölümler ekleme, düzenleme ve silme
- **Eğitim Yönetimi**: Eğitim tanımlama ve yönetimi
- **Seviye Tanımlama**: Temel, Orta, İleri seviye kategorileri
- **Eğitim-Bölüm İlişkilendirme**: Çapraz birim eğitim programları
- **Kullanıcı Atamaları**: Personel eğitim atama sistemi

### Kullanıcı Yönetimi
- **Kayıt ve Giriş Sistemi**: Güvenli kimlik doğrulama
- **Rol Tabanlı Yetkilendirme**: Admin, Eğitmen, Personel rolleri
- **Profil Yönetimi**: Kullanıcı bilgileri ve şifre değiştirme

### Eğitim Takip Sistemi
- **Eğitim Listesi**: Atanan eğitimlerin görüntülenmesi
- **İlerleme Takibi**: Başlamadı, Devam Ediyor, Tamamlandı durumları
- **Tamamlama Sistemi**: Eğitim tamamlama ve sertifikasyon
- **Ön Koşul Kontrolü**: Eğitimler arası bağımlılık yönetimi
- **Kariyer Yolu Analizi**: Bölüm bazlı ilerleme görselleştirme

### Arayüz Özellikleri
- **Responsive Tasarım**: Bootstrap 5 ile modern arayüz
- **Kullanıcı Dostu**: Sezgisel navigasyon ve işlemler
- **Filtreleme ve Arama**: Gelişmiş listeleme özellikleri
- **Detaylı Sayfalar**: Kapsamlı eğitim ve kullanıcı bilgileri

## 🛠️ Teknoloji Yığını

- **Backend**: Python Flask 3.0
- **Veritabanı**: SQLite + SQLAlchemy ORM (PostgreSQL'e geçiş için hazır)
- **Frontend**: Bootstrap 5 + Font Awesome
- **Kimlik Doğrulama**: Flask-Login
- **Form Yönetimi**: Flask-WTF
- **Veritabanı Migrasyon**: Flask-Migrate

## 📋 Gereksinimler

- Python 3.8+
- pip (Python paket yöneticisi)
- SQLite (Python ile birlikte gelir)

## 🚀 Kurulum

### 1. Projeyi Klonlayın
```bash
git clone <repository-url>
cd egitim-yonetim-sistemi
```

### 2. Sanal Ortam Oluşturun
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Ayarlayın (Opsiyonel)
`.env` dosyası oluşturun (isteğe bağlı):
```env
SECRET_KEY=your-secret-key-here
FLASK_APP=run.py
FLASK_ENV=development
```

### 5. Veritabanını Başlatın
```bash
flask init-db
```

### 6. Veritabanını Test Edin (Opsiyonel)
```bash
python test_db.py
```

### 7. Uygulamayı Çalıştırın
```bash
python run.py
```

Uygulama http://localhost:5000 adresinde çalışacaktır.

## 👤 Varsayılan Kullanıcılar

Sistem kurulumu sonrası otomatik olarak oluşturulan admin kullanıcısı:
- **E-posta**: admin@example.com
- **Şifre**: admin123

## 📁 Proje Yapısı

```
egitim-yonetim-sistemi/
├── app/                          # Ana uygulama paketi
│   ├── __init__.py              # Flask uygulama fabrikası
│   ├── models.py                # Veritabanı modelleri
│   ├── auth/                    # Kimlik doğrulama blueprint'i
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/
│   ├── admin/                   # Yönetim paneli blueprint'i
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/
│   ├── user/                    # Kullanıcı işlemleri blueprint'i
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/
│   ├── main/                    # Ana sayfa blueprint'i
│   │   ├── __init__.py
│   │   └── routes.py
│   └── templates/               # HTML şablonları
├── config.py                    # Uygulama konfigürasyonu
├── requirements.txt             # Python bağımlılıkları
├── run.py                       # Uygulama başlatıcı
└── README.md                    # Proje dokümantasyonu
```

## 🔧 Kullanım

### Admin Paneli
1. Admin hesabıyla giriş yapın
2. Bölümler, eğitimler ve kullanıcıları yönetin
3. Eğitim-bölüm ilişkilerini tanımlayın
4. Kullanıcılara eğitim atayın

### Kullanıcı Paneli
1. Kullanıcı hesabıyla giriş yapın
2. Dashboard'da eğitim ilerlemenizi görün
3. Eğitimlerinizi başlatın ve tamamlayın
4. Kariyer yolunuzu takip edin

## 🗄️ Veritabanı Modelleri

### User (Kullanıcı)
- id, isim, email, sifre_hash, rol, bolum_id

### Department (Bölüm)
- id, ad, aciklama

### Level (Seviye)
- id, ad (Temel, Orta, İleri)

### Training (Eğitim)
- id, kod, baslik, aciklama, pre_requisite_id

### TrainingSection (Eğitim-Bölüm İlişkisi)
- id, egitim_id, bolum_id, seviye_id

### UserTraining (Kullanıcı-Eğitim İlişkisi)
- id, kullanici_id, egitim_id, durum, tamamlanma_tarihi

## 🔒 Güvenlik

- Şifreler hash'lenerek saklanır (Werkzeug)
- CSRF koruması (Flask-WTF)
- Rol tabanlı erişim kontrolü
- Güvenli oturum yönetimi (Flask-Login)

## 🚀 Geliştirme

### Yeni Özellik Ekleme
1. İlgili blueprint'te route ekleyin
2. Form sınıfı oluşturun (gerekirse)
3. HTML şablonu ekleyin
4. Veritabanı modelini güncelleyin (gerekirse)

### Veritabanı Değişiklikleri
```bash
flask db migrate -m "Açıklama"
flask db upgrade
```

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 İletişim

Proje hakkında sorularınız için issue açabilirsiniz. 