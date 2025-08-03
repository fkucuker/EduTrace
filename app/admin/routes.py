from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.admin.forms import DepartmentForm, TrainingForm, TrainingSectionForm, UserAssignmentForm, UserForm, UserPasswordForm
from app.models import Department, Training, Level, TrainingSection, User, UserTraining
from datetime import datetime

def admin_required(f):
    """Admin yetkisi gerektiren decorator"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def index():
    # İstatistikler
    stats = {
        'total_users': User.query.count(),
        'total_trainings': Training.query.count(),
        'total_departments': Department.query.count(),
        'completed_trainings': UserTraining.query.filter_by(durum='tamamlandi').count()
    }
    
    # Son eklenen eğitimler
    recent_trainings = Training.query.order_by(Training.created_at.desc()).limit(5).all()
    
    # Son kullanıcılar
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/index.html', 
                         stats=stats, 
                         recent_trainings=recent_trainings,
                         recent_users=recent_users)

# Bölüm Yönetimi
@bp.route('/departments')
@login_required
@admin_required
def departments():
    departments = Department.query.all()
    return render_template('admin/departments.html', departments=departments)

@bp.route('/departments/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(
            ad=form.ad.data,
            aciklama=form.aciklama.data
        )
        db.session.add(department)
        db.session.commit()
        flash('Bölüm başarıyla eklendi.', 'success')
        return redirect(url_for('admin.departments'))
    
    return render_template('admin/department_form.html', form=form, title='Bölüm Ekle')

@bp.route('/departments/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_department(id):
    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    
    if form.validate_on_submit():
        department.ad = form.ad.data
        department.aciklama = form.aciklama.data
        db.session.commit()
        flash('Bölüm başarıyla güncellendi.', 'success')
        return redirect(url_for('admin.departments'))
    
    return render_template('admin/department_form.html', form=form, title='Bölüm Düzenle')

@bp.route('/departments/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_department(id):
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('Bölüm başarıyla silindi.', 'success')
    return redirect(url_for('admin.departments'))

# Eğitim Yönetimi
@bp.route('/trainings')
@login_required
@admin_required
def trainings():
    trainings = Training.query.all()
    return render_template('admin/trainings.html', trainings=trainings)

@bp.route('/trainings/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_training():
    form = TrainingForm()
    if form.validate_on_submit():
        training = Training(
            kod=form.kod.data,
            baslik=form.baslik.data,
            aciklama=form.aciklama.data,
            pre_requisite_id=form.pre_requisite_id.data if form.pre_requisite_id.data != 0 else None
        )
        db.session.add(training)
        db.session.commit()
        flash('Eğitim başarıyla eklendi.', 'success')
        return redirect(url_for('admin.trainings'))
    
    return render_template('admin/training_form.html', form=form, title='Eğitim Ekle')

@bp.route('/trainings/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_training(id):
    training = Training.query.get_or_404(id)
    form = TrainingForm(obj=training)
    
    if form.validate_on_submit():
        training.kod = form.kod.data
        training.baslik = form.baslik.data
        training.aciklama = form.aciklama.data
        training.pre_requisite_id = form.pre_requisite_id.data if form.pre_requisite_id.data != 0 else None
        db.session.commit()
        flash('Eğitim başarıyla güncellendi.', 'success')
        return redirect(url_for('admin.trainings'))
    
    return render_template('admin/training_form.html', form=form, title='Eğitim Düzenle')

@bp.route('/trainings/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_training(id):
    training = Training.query.get_or_404(id)
    db.session.delete(training)
    db.session.commit()
    flash('Eğitim başarıyla silindi.', 'success')
    return redirect(url_for('admin.trainings'))

# Eğitim-Bölüm İlişkilendirme
@bp.route('/training-sections')
@login_required
@admin_required
def training_sections():
    sections = TrainingSection.query.all()
    return render_template('admin/training_sections.html', sections=sections)

@bp.route('/training-sections/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_training_section():
    form = TrainingSectionForm()
    if form.validate_on_submit():
        # Aynı eğitim-bölüm ilişkisi var mı kontrol et
        existing = TrainingSection.query.filter_by(
            egitim_id=form.egitim_id.data,
            bolum_id=form.bolum_id.data
        ).first()
        
        if existing:
            flash('Bu eğitim-bölüm ilişkisi zaten mevcut.', 'warning')
        else:
            section = TrainingSection(
                egitim_id=form.egitim_id.data,
                bolum_id=form.bolum_id.data,
                seviye_id=form.seviye_id.data
            )
            db.session.add(section)
            db.session.commit()
            flash('Eğitim-bölüm ilişkisi başarıyla eklendi.', 'success')
        
        return redirect(url_for('admin.training_sections'))
    
    return render_template('admin/training_section_form.html', form=form, title='Eğitim-Bölüm İlişkisi Ekle')

@bp.route('/training-sections/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_training_section(id):
    section = TrainingSection.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    flash('Eğitim-bölüm ilişkisi başarıyla silindi.', 'success')
    return redirect(url_for('admin.training_sections'))

# Kullanıcı Atama
@bp.route('/user-assignments')
@login_required
@admin_required
def user_assignments():
    user_trainings = UserTraining.query.all()
    return render_template('admin/user_assignments.html', user_trainings=user_trainings)

@bp.route('/user-assignments/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user_assignment():
    form = UserAssignmentForm()
    if form.validate_on_submit():
        user = User.query.get(form.kullanici_id.data)
        
        for egitim_id in form.egitim_ids.data:
            # Kullanıcının bu eğitimi zaten var mı kontrol et
            existing = UserTraining.query.filter_by(
                kullanici_id=user.id,
                egitim_id=egitim_id
            ).first()
            
            if not existing:
                user_training = UserTraining(
                    kullanici_id=user.id,
                    egitim_id=egitim_id,
                    durum='baslamadi'
                )
                db.session.add(user_training)
        
        db.session.commit()
        flash('Eğitimler başarıyla atandı.', 'success')
        return redirect(url_for('admin.user_assignments'))
    
    return render_template('admin/user_assignment_form.html', form=form, title='Kullanıcı Eğitim Ata')

# Kullanıcı Yönetimi
@bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            isim=form.isim.data,
            email=form.email.data,
            rol=form.rol.data,
            bolum_id=form.bolum_id.data if form.bolum_id.data != 0 else None,
            is_active=form.is_active.data
        )
        # Varsayılan şifre: 123456
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()
        flash(f'Kullanıcı başarıyla eklendi. Varsayılan şifre: 123456', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/user_form.html', form=form, title='Yeni Kullanıcı Ekle')

@bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        # Kullanıcı bilgilerini güncelle
        user.isim = form.isim.data
        user.email = form.email.data
        user.rol = form.rol.data
        user.bolum_id = form.bolum_id.data if form.bolum_id.data != 0 else None
        user.is_active = form.is_active.data
        
        try:
            db.session.commit()
            flash('Kullanıcı başarıyla güncellendi.', 'success')
            return redirect(url_for('admin.users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Kullanıcı güncellenirken hata oluştu: {str(e)}', 'danger')
    elif form.errors:
        flash('Form hataları var. Lütfen kontrol edin.', 'danger')
    
    return render_template('admin/user_form.html', form=form, title='Kullanıcı Düzenle')

@bp.route('/users/<int:id>/password', methods=['GET', 'POST'])
@login_required
@admin_required
def change_user_password(id):
    user = User.query.get_or_404(id)
    form = UserPasswordForm()
    
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Kullanıcı şifresi başarıyla değiştirildi.', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/user_password_form.html', form=form, user=user)

@bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user == current_user:
        flash('Kendinizi silemezsiniz.', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Kullanıcı başarıyla silindi.', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/users/<int:user_id>/assign-trainings', methods=['GET', 'POST'])
@login_required
@admin_required
def assign_trainings(user_id):
    user = User.query.get_or_404(user_id)
    form = UserAssignmentForm()
    form.kullanici_id.data = user_id
    
    if form.validate_on_submit():
        for egitim_id in form.egitim_ids.data:
            # Kullanıcının bu eğitimi zaten var mı kontrol et
            existing = UserTraining.query.filter_by(
                kullanici_id=user.id,
                egitim_id=egitim_id
            ).first()
            
            if not existing:
                user_training = UserTraining(
                    kullanici_id=user.id,
                    egitim_id=egitim_id,
                    durum='baslamadi'
                )
                db.session.add(user_training)
        
        db.session.commit()
        flash('Eğitimler başarıyla atandı.', 'success')
        return redirect(url_for('admin.users'))
    
    # Kullanıcının mevcut eğitimlerini seçili hale getir
    user_trainings = UserTraining.query.filter_by(kullanici_id=user_id).all()
    form.egitim_ids.data = [ut.egitim_id for ut in user_trainings]
    
    return render_template('admin/assign_trainings.html', form=form, user=user) 