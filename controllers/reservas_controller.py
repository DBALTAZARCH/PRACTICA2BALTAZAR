
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.paquete_model import get_by_id
from models.cliente_model import all as clientes_all, create as create_cliente
from models.reserva_model import create as create_reserva, all as all_reservas, delete as delete_reserva

reservas_bp = Blueprint('reservas', __name__, url_prefix='/reservas')

@reservas_bp.route('/reservar/<int:id_paquete>', methods=['GET','POST'])
def reservar(id_paquete):
    paquete = get_by_id(id_paquete)
    clientes = clientes_all()
    if not paquete:
        flash('Paquete no encontrado', 'warning')
        return redirect(url_for('paquetes.home'))
    if request.method == 'POST':
        id_cliente = request.form.get('id_cliente')
        # allow quick-adding a cliente inline
        if id_cliente == 'new':
            nombres = request.form.get('nombres_new','').strip()
            email = request.form.get('email_new','').strip()
            telefono = request.form.get('telefono_new','').strip()
            if not nombres:
                flash('Nombres del nuevo cliente son obligatorios', 'danger')
                return redirect(url_for('reservas.reservar', id_paquete=id_paquete))
            id_cliente = create_cliente(nombres,email,telefono)
        if not id_cliente:
            flash('Seleccione o cree un cliente', 'danger')
            return redirect(url_for('reservas.reservar', id_paquete=id_paquete))
        fecha = request.form.get('fecha')
        if not fecha:
            flash('Fecha es obligatoria', 'danger')
            return redirect(url_for('reservas.reservar', id_paquete=id_paquete))
        create_reserva(id_cliente, id_paquete, fecha)
        flash('Reserva registrada', 'success')
        return redirect(url_for('paquetes.home'))
    return render_template('reservas/add.html', paquete=paquete, clientes=clientes)

@reservas_bp.route('/list')
def list_reservas():
    rows = all_reservas()
    return render_template('reservas/list.html', reservas=rows)

@reservas_bp.route('/delete/<int:id_reserva>', methods=['POST'])
def delete(id_reserva):
    delete_reserva(id_reserva)
    flash('Reserva eliminada', 'success')
    return redirect(url_for('reservas.list_reservas'))
