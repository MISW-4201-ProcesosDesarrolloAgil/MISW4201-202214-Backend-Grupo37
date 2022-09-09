from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Apuesta(db.Model):
    __tablename__ = 'apuesta'

    id = db.Column(db.Integer, primary_key=True)
    valor_apostado = db.Column(db.Numeric)
    valor_ganancia = db.Column(db.Numeric, default=0)
    nombre_apostador = db.Column(db.String(128))
    fecha_apuesta = db.Column(db.String(128))
    id_competidor = db.Column(db.Integer, db.ForeignKey('competidor.id'))
    id_EventoDeportivo = db.Column(db.Integer, db.ForeignKey('evento_deportivo.id'))

class Competidor(db.Model):
    __tablename__ = 'competidor'

    id = db.Column(db.Integer, primary_key=True)
    nombre_competidor = db.Column(db.String(128))
    probabilidad = db.Column(db.String(100))
    puntaje = db.Column(db.String(100))
    cuota = db.Column(db.String(100))
    es_ganador = db.Column(db.Boolean, default=False)
    estatus = db.Column(db.Boolean, default=False)
    id_EventoDeportivo = db.Column(db.Integer, db.ForeignKey('evento_deportivo.id'))

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    #nombre = db.Column(db.String(50))
    usuario = db.Column(db.String(50))
    email = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    rol = db.Column(db.Integer, default=True) # 0: admin, 1: apostador
    phone = db.Column(db.String(50))
    no_cuenta = db.Column(db.String(20))
    nombre_banco = db.Column(db.String(50))
    saldo = db.Column(db.String(50), default='0.0')
    medio_pago = db.Column(db.String(50))
    EventoDeportivos = db.relationship('EventoDeportivo', cascade='all, delete, delete-orphan')

class EventoDeportivo(db.Model):
    __tablename__ = 'evento_deportivo'

    id = db.Column(db.Integer, primary_key=True)
    nombre_EventoDeportivo = db.Column(db.String(128))
    estado = db.Column(db.Boolean, default=True)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    competidores = db.relationship('Competidor', cascade='all, delete, delete-orphan')
    apuestas = db.relationship('Apuesta', cascade='all, delete, delete-orphan')    

class EventoCarrera(EventoDeportivo):
    __tablename__ = 'evento_carrera'

    #id = db.Column(db.Integer, primary_key=True)
    id = db.Column(None, db.ForeignKey('evento_deportivo.id'), primary_key=True)
    id_competidor_ganador = db.Column(db.Integer, db.ForeignKey('competidor.id'))

class EventoMarcador(EventoDeportivo):
    __tablename__ = 'evento_marcador'

    #id = db.Column(db.Integer, primary_key=True)
    id = db.Column(None, db.ForeignKey('evento_deportivo.id'), primary_key=True)
    id_marcador = db.Column(db.Integer, db.ForeignKey("marcador.id"))

class Marcador(db.Model):
    __tablename__ = 'marcador'

    id = db.Column(db.Integer, primary_key=True)
    marcador = db.Column(db.String(50))
    id_competidor_ganador = db.Column(db.Integer, db.ForeignKey('competidor.id'))
    id_competidor_perdedor  = db.Column(db.Integer, db.ForeignKey('competidor.id'))



class ApuestaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Apuesta
        include_relationships = True
        include_fk = True
        load_instance = True

    valor_apostado = fields.String()
    ganancia = fields.String()


class CompetidorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Competidor
        include_relationships = True
        load_instance = True

    probabilidad = fields.String()
    cuota = fields.String()


class EventoDeportivoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventoDeportivo
        include_relationships = True
        load_instance = True
        many = True

    competidores = fields.List(fields.Nested(CompetidorSchema()))
    apuestas = fields.List(fields.Nested(ApuestaSchema()))
    ganancia_casa = fields.Float()


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True


class ReporteSchema(Schema):
    carrera = fields.Nested(EventoDeportivoSchema())
    ganancia_casa = fields.Float()
