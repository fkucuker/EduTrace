from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.user import bp
from app.user.forms import ProfileForm
from app.models import UserTraining, Training, TrainingSection, Department
from datetime import datetime

@bp.route('/dashboard')
@login_required
def dashboard():
    # Kullanıcının eğitimleri
    user_trainings = UserTraining.query.filter_by(kullanici_id=current_user.id).all()
    
    # İstatistikler
    stats = {
        'total_assigned': len(user_trainings),
        'completed': len([ut for ut in user_trainings if ut.durum == 'tamamlandi']),
        'in_progress': len([ut for ut in user_trainings if ut.durum == 'devam']),
        'not_started': len([ut for ut in user_trainings if ut.durum == 'baslamadi'])
    }
    
    # Devam eden eğitimler
    in_progress = [ut for ut in user_trainings if ut.durum == 'devam']
    
    # Tamamlanan eğitimler
    completed = [ut for ut in user_trainings if ut.durum == 'tamamlandi']
    
    return render_template('user/dashboard.html', 
                         stats=stats,
                         in_progress=in_progress,
                         completed=completed)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(original_email=current_user.email)
    
    if form.validate_on_submit():
        current_user.isim = form.isim.data
        current_user.email = form.email.data
        current_user.bolum_id = form.bolum_id.data
        db.session.commit()
        flash('Profiliniz başarıyla güncellendi.', 'success')
        return redirect(url_for('user.profile'))
    elif request.method == 'GET':
        form.isim.data = current_user.isim
        form.email.data = current_user.email
        form.bolum_id.data = current_user.bolum_id
    
    return render_template('user/profile.html', form=form)

@bp.route('/trainings')
@login_required
def my_trainings():
    user_trainings = UserTraining.query.filter_by(kullanici_id=current_user.id).all()
    return render_template('user/trainings.html', user_trainings=user_trainings)

@bp.route('/training/<int:training_id>/start', methods=['POST'])
@login_required
def start_training(training_id):
    user_training = UserTraining.query.filter_by(
        kullanici_id=current_user.id,
        egitim_id=training_id
    ).first()
    
    if not user_training:
        flash('Bu eğitim size atanmamış.', 'danger')
        return redirect(url_for('user.my_trainings'))
    
    if user_training.durum == 'baslamadi':
        user_training.durum = 'devam'
        user_training.baslama_tarihi = datetime.utcnow()
        db.session.commit()
        flash('Eğitime başladınız.', 'success')
    
    return redirect(url_for('user.my_trainings'))

@bp.route('/training/<int:training_id>/complete', methods=['POST'])
@login_required
def complete_training(training_id):
    user_training = UserTraining.query.filter_by(
        kullanici_id=current_user.id,
        egitim_id=training_id
    ).first()
    
    if not user_training:
        flash('Bu eğitim size atanmamış.', 'danger')
        return redirect(url_for('user.my_trainings'))
    
    if user_training.durum == 'devam':
        user_training.durum = 'tamamlandi'
        user_training.tamamlanma_tarihi = datetime.utcnow()
        db.session.commit()
        flash('Eğitimi başarıyla tamamladınız!', 'success')
    
    return redirect(url_for('user.my_trainings'))

@bp.route('/training/<int:training_id>')
@login_required
def training_detail(training_id):
    user_training = UserTraining.query.filter_by(
        kullanici_id=current_user.id,
        egitim_id=training_id
    ).first()
    
    if not user_training:
        flash('Bu eğitim size atanmamış.', 'danger')
        return redirect(url_for('user.my_trainings'))
    
    training = Training.query.get(training_id)
    sections = TrainingSection.query.filter_by(egitim_id=training_id).all()
    
    return render_template('user/training_detail.html', 
                         user_training=user_training,
                         training=training,
                         sections=sections)

@bp.route('/career-path')
@login_required
def career_path():
    # Kullanıcının bölümü
    user_department = current_user.bolum
    
    # Bölümdeki tüm eğitimler
    department_trainings = TrainingSection.query.filter_by(bolum_id=user_department.id).all()
    
    # Kullanıcının tamamladığı eğitimler
    completed_trainings = UserTraining.query.filter_by(
        kullanici_id=current_user.id,
        durum='tamamlandi'
    ).all()
    
    # Seviye bazında ilerleme
    progress_by_level = {}
    for section in department_trainings:
        level_name = section.seviye.ad
        if level_name not in progress_by_level:
            progress_by_level[level_name] = {'total': 0, 'completed': 0}
        
        progress_by_level[level_name]['total'] += 1
        
        # Bu eğitimi tamamlamış mı kontrol et
        for ut in completed_trainings:
            if ut.egitim_id == section.egitim_id:
                progress_by_level[level_name]['completed'] += 1
                break
    
    return render_template('user/career_path.html',
                         user_department=user_department,
                         progress_by_level=progress_by_level,
                         department_trainings=department_trainings,
                         completed_trainings=completed_trainings) 