from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.reports import bp
from app.models import Department, Training, TrainingSection, Level, User, UserTraining
from app import db

def admin_required(f):
    """Admin yetkisi gerektiren dekoratör"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def index():
    """Raporlar ana sayfası"""
    return render_template('reports/index.html', title='Raporlar')

@bp.route('/department-trainings')
@login_required
@admin_required
def department_trainings():
    """Bölüme göre eğitimleri listele"""
    departments = Department.query.all()
    selected_department_id = request.args.get('department_id', type=int)
    
    if selected_department_id:
        department = Department.query.get(selected_department_id)
        if not department:
            flash('Seçilen bölüm bulunamadı.', 'danger')
            return redirect(url_for('reports.department_trainings'))
        
        # Bölüme ait eğitimleri getir
        training_sections = TrainingSection.query.filter_by(bolum_id=selected_department_id).all()
        
        # Eğitim detaylarını topla
        trainings_data = []
        for ts in training_sections:
            training = Training.query.get(ts.egitim_id)
            level = Level.query.get(ts.seviye_id)
            
            # Bu eğitimin kaç kullanıcıya atandığını say
            assigned_count = UserTraining.query.filter_by(egitim_id=ts.egitim_id).count()
            
            # Bu eğitimi tamamlayan kullanıcı sayısını say
            completed_count = UserTraining.query.filter_by(
                egitim_id=ts.egitim_id, 
                durum='tamamlandi'
            ).count()
            
            trainings_data.append({
                'training': training,
                'level': level,
                'assigned_count': assigned_count,
                'completed_count': completed_count,
                'completion_rate': round((completed_count / assigned_count * 100) if assigned_count > 0 else 0, 1)
            })
        
        return render_template('reports/department_trainings.html', 
                             title=f'{department.ad} - Eğitimler',
                             departments=departments,
                             selected_department=department,
                             trainings_data=trainings_data)
    
    return render_template('reports/department_trainings.html', 
                         title='Bölüm Eğitimleri',
                         departments=departments,
                         selected_department=None,
                         trainings_data=[]) 