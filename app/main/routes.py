from flask import render_template, redirect, url_for
from flask_login import current_user
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.index'))
        else:
            return redirect(url_for('user.dashboard'))
    
    return render_template('index.html', title='Eğitim Yönetim Sistemi')

@bp.route('/about')
def about():
    return render_template('about.html', title='Hakkında') 