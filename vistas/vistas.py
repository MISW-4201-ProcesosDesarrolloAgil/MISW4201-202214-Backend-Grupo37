import email
import re
from flask import request

from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from modelos.modelos2 import db, Apuesta, ApuestaSchema, Usuario, UsuarioSchema, CompetidorSchema, Competidor, ReporteSchema, EventoDeportivo, EventoDeportivoSchema



apuesta_schema = ApuestaSchema()
eventod_schema = EventoDeportivoSchema()
competidor_schema = CompetidorSchema()
usuario_schema = UsuarioSchema()
reporte_schema = ReporteSchema()


class VistaUsuarios(Resource):
    #@jwt_required
    def get(self):
        usuarios = Usuario.query.all()
        return usuario_schema.dump(usuarios, many=True)

class VistaSignInAdmin(Resource):

    def post(self):
        nuevo_usuario = Usuario(usuario=request.json["usuario"], email=request.json["u_email"], 
        contrasena = request.json["contrasena"], phone = request.json["phone"], rol=0, no_cuenta='', nombre_banco='', saldo='0.0', medio_pago='')
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {"mensaje": "usuario admin creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id, "rol": nuevo_usuario.rol}

class VistaSignInApostador(Resource):
    
    def post(self):
        nuevo_usuario = Usuario(usuario=request.json["usuario"], email=request.json["u_email"], 
        contrasena=request.json["contrasena"], phone = request.json["phone"], rol=1, no_cuenta='', nombre_banco='', saldo=0.0, medio_pago='')
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {"mensaje": "usuario apostador creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id, "rol": nuevo_usuario.rol}

class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                        Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "rol": usuario.rol}
    def put(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                        Usuario.id == request.json["id"],
                                        Usuario.rol == request.json["rol"]).first()
        if(usuario is None):
            return "El usuario no existe", 404
        usuario.contrasena = request.json.get("contrasena_new", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)
    
    def delete(self):
        ##usuario = Usuario.query.get_or_404(id_usuario)
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                        Usuario.id == request.json["id"],
                                        Usuario.rol == request.json["rol"]).first()
        if(usuario is None):
            return "El usuario no existe", 404
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

class VistaEventosUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nuevo_eventod = EventoDeportivo(nombre_EventoDeportivo=request.json["nombre"])
        for item in request.json["competidores"]:
            cuota = round((item["probabilidad"] / (1 - item["probabilidad"])), 2)
            competidor = Competidor(nombre_competidor=item["competidor"],
                                    probabilidad=item["probabilidad"],
                                    cuota=cuota,
                                    id_carrera=nuevo_eventod.id)
            nuevo_eventod.competidores.append(competidor)
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.carreras.append(nuevo_eventod)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un carrera con dicho nombre', 409

        return eventod_schema.dump(nuevo_eventod)

    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [eventod_schema.dump(eventod) for eventod in usuario.EventoDeportivos]

class VistaEventos(Resource):

    @jwt_required()
    def get(self, id_eventod):
        return eventod_schema.dump(EventoDeportivo.query.get_or_404(id_eventod))

    @jwt_required()
    def put(self, id_eventod):
        evento_deportivo = EventoDeportivo.query.get_or_404(id_eventod)
        evento_deportivo.nombre_carrera = request.json.get("nombre", evento_deportivo.nombre_EventoDeportivo)
        evento_deportivo.competidores = []

        for item in request.json["competidores"]:
            probabilidad = float(item["probabilidad"])
            cuota = round((probabilidad / (1 - probabilidad)), 2)
            competidor = Competidor(nombre_competidor=item["competidor"],
                                    probabilidad=probabilidad,
                                    cuota=cuota,
                                    id_EventoDeportivo=evento_deportivo.id)
            evento_deportivo.competidores.append(competidor)

        db.session.commit()
        return eventod_schema.dump(evento_deportivo)

    @jwt_required()
    def delete(self, id_eventod):
        eventod = EventoDeportivo.query.get_or_404(id_eventod)
        db.session.delete(eventod)
        db.session.commit()
        return '', 204

class VistaApuestas(Resource):

    @jwt_required()
    def post(self):
        nueva_apuesta = Apuesta(valor_apostado=request.json["valor_apostado"],
                                nombre_apostador=request.json["nombre_apostador"],
                                id_competidor=request.json["id_competidor"], id_carrera=request.json["id_carrera"])
        db.session.add(nueva_apuesta)
        db.session.commit()
        return apuesta_schema.dump(nueva_apuesta)

    @jwt_required()
    def get(self):
        return [apuesta_schema.dump(ca) for ca in Apuesta.query.all()]

class VistaApuesta(Resource):

    @jwt_required()
    def get(self, id_apuesta):
        return apuesta_schema.dump(Apuesta.query.get_or_404(id_apuesta))

    @jwt_required()
    def put(self, id_apuesta):
        apuesta = Apuesta.query.get_or_404(id_apuesta)
        apuesta.valor_apostado = request.json.get("valor_apostado", apuesta.valor_apostado)
        apuesta.nombre_apostador = request.json.get("nombre_apostador", apuesta.nombre_apostador)
        apuesta.id_competidor = request.json.get("id_competidor", apuesta.id_competidor)
        apuesta.id_carrera = request.json.get("id_carrera", apuesta.id_carrera)
        db.session.commit()
        return apuesta_schema.dump(apuesta)

    @jwt_required()
    def delete(self, id_apuesta):
        apuesta = Apuesta.query.get_or_404(id_apuesta)
        db.session.delete(apuesta)
        db.session.commit()
        return '', 204

class VistaTerminacionEventoConGanador(Resource):

    def put(self, id_competidor):
        competidor = Competidor.query.get_or_404(id_competidor)
        competidor.es_ganador = True
        eventod = EventoDeportivo.query.get_or_404(competidor.id_EventoDeportivo)
        eventod.abierta = False

        for apuesta in eventod.apuestas:
            if apuesta.id_competidor == competidor.id:
                apuesta.ganancia = apuesta.valor_apostado + (apuesta.valor_apostado/competidor.cuota)
            else:
                apuesta.ganancia = 0

        db.session.commit()
        return competidor_schema.dump(competidor)

class VistaReporte(Resource):

    @jwt_required()
    def get(self, id_eventod):
        EDReporte = EventoDeportivo.query.get_or_404(id_eventod)
        ganancia_casa_final = 0

        for apuesta in EDReporte.apuestas:
            ganancia_casa_final = ganancia_casa_final + apuesta.valor_apostado - apuesta.ganancia

        reporte = dict(carrera=EDReporte, ganancia_casa=ganancia_casa_final)
        schema = ReporteSchema()
        return schema.dump(reporte)

class VistaCompetidores(Resource):
    
    #@jwt_required()
    def get(self):
        competidores = Competidor.query.all()
        return competidor_schema.dump(competidores, many=True)

class FinalizarEvento(Resource):

    #@jwt_required
    def put(self, id_eventod):
        print('hola ' + id_eventod)
        eventoDeportivo = EventoDeportivo.query.get_or_404(id_eventod)
        eventoDeportivo.estado = False
        db.session.commit()
        return eventod_schema.dump(eventoDeportivo)

class VistaEventosDisponibles(Resource):
    
    #@jwt_required
    def get(self):
        eventosDeportivos = EventoDeportivo.query.all()
        #eventosDeportivos = db.session(EventoDeportivo).filter(EventoDeportivo.estado is True).all()
    
        ''''if(eventosDeportivos is None or np.size(eventosDeportivos) > 0 ):
            return "No hay eventos Disponibles", 404 '''
        eventosD = []
        for evento in eventosDeportivos:
            if(evento.estado is True):
                
                eventosD.append(evento)
       # return eventod_schema.dump(eventosDeportivos, many=True)
        return eventod_schema.dump(eventosD)
