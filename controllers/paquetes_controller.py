
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.paquete_model import all as all_paquetes, get_by_id, create, update, delete

paquetes_bp = Blueprint('paquetes', __name__, url_prefix='')

@paquetes_bp.route('/')
def home():
    paquetes = all_paquetes()
    return render_template('index.html', paquetes=paquetes)

@paquetes_bp.route('/paquetes')
def list_paquetes():
    paquetes = all_paquetes()
    return render_template('paquetes/list.html', paquetes=paquetes)

@paquetes_bp.route('/paquetes/add', methods=['GET','POST'])
def add_paquete():
    if request.method == 'POST':
        nombre = request.form.get('nombre','').strip()
        precio = request.form.get('precio','').strip()
        if not nombre or not precio:
            flash('Nombre y precio son obligatorios', 'danger')
            return redirect(url_for('paquetes.add_paquete'))
        try:
            precio_v = float(precio)
        except:
            flash('Precio debe ser numérico', 'danger')
            return redirect(url_for('paquetes.add_paquete'))
        create(nombre, precio_v)
        flash('Paquete agregado', 'success')
        return redirect(url_for('paquetes.list_paquetes'))
    return render_template('paquetes/add.html')

@paquetes_bp.route('/paquetes/edit/<int:id_destino>', methods=['GET','POST'])
def edit_paquete(id_destino):
    paquete = get_by_id(id_destino)
    if not paquete:
        flash('Paquete no encontrado', 'warning')
        return redirect(url_for('paquetes.list_paquetes'))
    if request.method == 'POST':
        nombre = request.form.get('nombre','').strip()
        precio = request.form.get('precio','').strip()
        if not nombre or not precio:
            flash('Nombre y precio son obligatorios', 'danger')
            return redirect(url_for('paquetes.edit_paquete', id_destino=id_destino))
        try:
            precio_v = float(precio)
        except:
            flash('Precio debe ser numérico', 'danger')
            return redirect(url_for('paquetes.edit_paquete', id_destino=id_destino))
        update(id_destino, nombre, precio_v)
        flash('Paquete actualizado', 'success')
        return redirect(url_for('paquetes.list_paquetes'))
    return render_template('paquetes/edit.html', paquete=paquete)

@paquetes_bp.route('/paquetes/delete/<int:id_destino>', methods=['POST'])
def delete_paquete(id_destino):
    paquete = get_by_id(id_destino)
    if not paquete:
        flash('Paquete no encontrado', 'warning')
    else:
        delete(id_destino)
        flash('Paquete eliminado', 'success')
    return redirect(url_for('paquetes.list_paquetes'))
