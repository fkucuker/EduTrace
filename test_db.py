#!/usr/bin/env python3
"""
Veritabanı bağlantı testi
Bu script veritabanının düzgün çalışıp çalışmadığını test eder.
"""

import os
import sys

def test_database():
    """Veritabanı bağlantısını test et"""
    try:
        # Flask uygulamasını import et
        from app import create_app, db
        from app.models import User, Department, Level, Training
        
        print("🔍 Veritabanı bağlantısı test ediliyor...")
        
        # Uygulamayı oluştur
        app = create_app()
        
        with app.app_context():
            # Veritabanı bağlantısını test et
            with db.engine.connect() as conn:
                conn.execute(db.text('SELECT 1'))
            print("✓ Veritabanı bağlantısı başarılı!")
            
            # Tabloların varlığını kontrol et
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            expected_tables = ['users', 'departments', 'levels', 'trainings', 'training_sections', 'user_trainings']
            
            print(f"📋 Mevcut tablolar: {tables}")
            
            missing_tables = [table for table in expected_tables if table not in tables]
            if missing_tables:
                print(f"⚠️  Eksik tablolar: {missing_tables}")
                print("💡 Çözüm: flask init-db komutunu çalıştırın")
                return False
            else:
                print("✓ Tüm tablolar mevcut!")
            
            # Örnek veri kontrolü
            user_count = User.query.count()
            dept_count = Department.query.count()
            level_count = Level.query.count()
            training_count = Training.query.count()
            
            print(f"👥 Kullanıcı sayısı: {user_count}")
            print(f"🏢 Bölüm sayısı: {dept_count}")
            print(f"📊 Seviye sayısı: {level_count}")
            print(f"📚 Eğitim sayısı: {training_count}")
            
            if user_count == 0:
                print("⚠️  Hiç kullanıcı bulunamadı!")
                print("💡 Çözüm: flask init-db komutunu çalıştırın")
                return False
            
            print("\n🎉 Veritabanı testi başarılı!")
            return True
            
    except ImportError as e:
        print(f"❌ Import hatası: {e}")
        print("💡 Çözüm: pip install -r requirements.txt komutunu çalıştırın")
        return False
    except Exception as e:
        print(f"❌ Veritabanı hatası: {e}")
        print("💡 Çözüm önerileri:")
        print("   1. flask init-db komutunu çalıştırın")
        print("   2. app.db dosyasının yazma izinlerini kontrol edin")
        print("   3. Gerekli paketlerin yüklü olduğundan emin olun")
        return False

if __name__ == '__main__':
    success = test_database()
    sys.exit(0 if success else 1) 