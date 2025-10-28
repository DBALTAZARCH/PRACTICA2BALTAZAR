
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import find_by_username, create
import hashlib

auth_bp = Blueprint('auth', __name__, url_prefix='')

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')
        user = find_by_username(username)
        if user and user['password_hash'] == hash_password(password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Bienvenido, {}'.format(user['username']), 'success')
            return redirect(url_for('paquetes.home'))
        flash('Usuario o contraseña incorrectos', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('paquetes.home'))

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')
        if not username or not password:
            flash('Usuario y contraseña obligatorios', 'danger')
            return redirect(url_for('auth.register'))
        if find_by_username(username):
            flash('El usuario ya existe', 'warning')
            return redirect(url_for('auth.register'))
        create(username, hash_password(password))
        flash('Registro exitoso. Ahora inicia sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')
