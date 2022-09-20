from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos.modelos2 import db
from vistas import VistaApuestas, VistaApuesta, VistaLogIn, VistaEventosUsuario, VistaEventos, VistaTerminacionEventoConGanador, VistaReporte, \
    VistaSignInApostador, VistaSignInAdmin, VistaUsuarios, VistaCompetidores, FinalizarEvento, VistaEventosDisponibles, VistaEventoTipo
#, VistaCarrerasUsuario, VistaCarrera, VistaTerminacionCarrera, VistaReporte

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eporra.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaSignInAdmin, '/signin/admin')
api.add_resource(VistaSignInApostador, '/signin/apostador')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaEventosUsuario, '/usuario/<int:id_usuario>/eventosd')
api.add_resource(VistaUsuarios, '/usuarios')
api.add_resource(VistaEventos, '/eventod/<int:id_eventod>')
api.add_resource(VistaFinalizarEvento, '/eventod/finalizareventodeportivo/<int:id_eventod>')
api.add_resource(VistaReporte, '/eventod/<int:id_eventod>/reporte')
api.add_resource(VistaEventosDisponibles, '/eventod/eventosdisponibles')
api.add_resource(VistaTerminacionEventoConGanador, '/eventod/terminarevento/<int:id_competidor>/terminacion')
api.add_resource(VistaApuestas, '/apuestas')
api.add_resource(VistaApuesta, '/apuesta/<int:id_apuesta>')
api.add_resource(VistaCompetidores, '/competidores')

#api.add_resource(VistaEventosDisponibles, '/eventod')

jwt = JWTManager(app)

