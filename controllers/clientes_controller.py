
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.cliente_model import create, all as all_clientes, get, update, delete

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientes_bp.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        nombres = request.form.get('nombres','').strip()
        email = request.form.get('email','').strip()
        telefono = request.form.get('telefono','').strip()
        # basic validation
        if not nombres:
            flash('El campo nombres es obligatorio', 'danger')
            return redirect(url_for('clientes.index'))
        create(nombres,email,telefono)
        flash('Cliente agregado correctamente', 'success')
        return redirect(url_for('clientes.index'))
    clientes = all_clientes()
    return render_template('clientes/list.html', clientes=clientes)

@clientes_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    cliente = get(id)
    if not cliente:
        flash('Cliente no encontrado', 'warning')
        return redirect(url_for('clientes.index'))
    if request.method == 'POST':
        nombres = request.form.get('nombres','').strip()
        email = request.form.get('email','').strip()
        telefono = request.form.get('telefono','').strip()
        if not nombres:
            flash('Nombres no puede estar vacío', 'danger')
            return redirect(url_for('clientes.edit', id=id))
        update(id, nombres, email, telefono)
        flash('Cliente actualizado', 'success')
        return redirect(url_for('clientes.index'))
    return render_template('clientes/edit.html', cliente=cliente)

@clientes_bp.route('/delete/<int:id>', methods=['POST'])
def remove(id):
    cliente = get(id)
    if not cliente:
        flash('Cliente no encontrado', 'warning')
    else:
        delete(id)
        flash('Cliente eliminado', 'success')
    return redirect(url_for('clientes.index'))
