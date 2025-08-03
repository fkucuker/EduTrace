from app import create_app, db
from app.models import User, Department, Level, Training, TrainingSection, UserTraining

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Department': Department,
        'Level': Level,
        'Training': Training,
        'TrainingSection': TrainingSection,
        'UserTraining': UserTraining
    }

@app.cli.command()
def init_db():
    """Veritabanını başlat ve örnek veriler ekle"""
    try:
        print("Veritabanı tabloları oluşturuluyor...")
        db.create_all()
        print("✓ Veritabanı tabloları başarıyla oluşturuldu.")
        
        # Seviyeleri ekle
        if Level.query.count() == 0:
            levels = [
                Level(ad='Temel'),
                Level(ad='Orta'),
                Level(ad='İleri')
            ]
            for level in levels:
                db.session.add(level)
            db.session.commit()
            print("✓ Seviyeler eklendi.")
        else:
            print("✓ Seviyeler zaten mevcut.")
        
        # Örnek bölümleri ekle
        if Department.query.count() == 0:
            departments = [
                Department(ad='Yönetişim', aciklama='Yönetişim biriminin eğitimleri'),
                Department(ad='Sistem İşletme', aciklama='Sistem işletme biriminin eğitimleri'),
                Department(ad='Red Team', aciklama='Red Team biriminin eğitimleri'),
                Department(ad='Siber Olay Müdahale', aciklama='Siber olay müdahale biriminin eğitimleri')
            ]
            for dept in departments:
                db.session.add(dept)
            db.session.commit()
            print("✓ Bölümler eklendi.")
        else:
            print("✓ Bölümler zaten mevcut.")
        
        # Örnek eğitimleri ekle
        if Training.query.count() == 0:
            trainings = [
                Training(kod='CS101', baslik='Siber Güvenliğe Giriş', aciklama='Siber güvenlik temelleri'),
                Training(kod='CS201', baslik='Ağ Güvenliği', aciklama='Ağ güvenliği konuları'),
                Training(kod='CS301', baslik='İleri Düzey Saldırı Tespiti', aciklama='Gelişmiş saldırı tespit teknikleri'),
                Training(kod='MG101', baslik='Proje Yönetimi', aciklama='Proje yönetim temelleri')
            ]
            for training in trainings:
                db.session.add(training)
            db.session.commit()
            print("✓ Eğitimler eklendi.")
        else:
            print("✓ Eğitimler zaten mevcut.")
        
        # Admin kullanıcısı ekle
        if User.query.filter_by(email='admin@example.com').first() is None:
            admin = User(
                isim='Sistem Yöneticisi',
                email='admin@example.com',
                rol='Admin',
                bolum_id=1
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin kullanıcısı eklendi (email: admin@example.com, şifre: admin123)")
        else:
            print("✓ Admin kullanıcısı zaten mevcut.")
            
        print("\n🎉 Veritabanı başarıyla başlatıldı!")
        print("📝 Uygulamayı başlatmak için: python run.py")
        print("🔑 Admin girişi: admin@example.com / admin123")
        
    except Exception as e:
        print(f"❌ Veritabanı başlatma hatası: {str(e)}")
        print("💡 Çözüm önerileri:")
        print("   1. Gerekli paketlerin yüklü olduğundan emin olun: pip install -r requirements.txt")
        print("   2. Uygulama dizininde olduğunuzdan emin olun")
        print("   3. app.db dosyasının yazma izinlerini kontrol edin")
        db.session.rollback()

if __name__ == '__main__':
    app.run(debug=True) 