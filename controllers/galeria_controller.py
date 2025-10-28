import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename

galeria_bp = Blueprint('galeria', __name__, url_prefix='/galeria')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@galeria_bp.route('/')
def index():
    images = []
    static_images = os.path.join(current_app.static_folder, 'images')
    if os.path.exists(static_images):
        for fname in os.listdir(static_images):
            if allowed_file(fname):
                images.append('images/' + fname)
    return render_template('galeria/index.html', images=images)

@galeria_bp.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'imagen' not in request.files:
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)
        file = request.files['imagen']
        if file.filename == '':
            flash('Nombre de archivo vacío', 'warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.static_folder, 'images', filename)
            file.save(upload_path)
            flash('Imagen subida correctamente', 'success')
            return redirect(url_for('galeria.index'))
        else:
            flash('Formato no permitido. Solo PNG/JPG/GIF.', 'danger')
    return render_template('galeria/upload.html')
