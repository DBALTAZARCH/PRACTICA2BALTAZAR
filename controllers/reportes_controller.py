
from flask import Blueprint, render_template
from models.reserva_model import ventas_por_destino

reportes_bp = Blueprint('reportes', __name__, url_prefix='')

@reportes_bp.route('/ventas_por_destino')
def ventas():
    rows = ventas_por_destino()
    return render_template('reports/ventas.html', rows=rows)
