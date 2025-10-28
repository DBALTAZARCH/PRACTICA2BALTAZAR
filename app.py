
from flask import Flask, render_template, session
from controllers.clientes_controller import clientes_bp
from controllers.paquetes_controller import paquetes_bp
from controllers.reservas_controller import reservas_bp
from controllers.reportes_controller import reportes_bp
from controllers.galeria_controller import galeria_bp
from controllers.auth_controller import auth_bp
from database import init_db
from config import Config

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)
    app.secret_key = app.config.get('SECRET_KEY')
    init_db(app)
    # register blueprints
    app.register_blueprint(clientes_bp)
    app.register_blueprint(paquetes_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(galeria_bp)
    app.register_blueprint(auth_bp)
    # error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404
    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
