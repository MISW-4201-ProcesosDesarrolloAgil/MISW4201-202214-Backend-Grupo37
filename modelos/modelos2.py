from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class Apuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor_apostado = db.Column(db.Numeric)
    valor_ganancia = db.Column(db.Numeric, default=0)
    nombre_apostador = db.Column(db.String(128))
    fecha_apuesta = db.Column(db.String(128))
    id_competidor = db.Column(db.Integer, db.ForeignKey('competidor.id'))
    id_EventoDeportivo = db.Column(db.Integer, db.ForeignKey('EventoDeportivo.id'))

class EventoDeportivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_EventoDeportivo = db.Column(db.String(128))
    estado = db.Column(db.Boolean, default=True)
    competidores = db.relationship('Competidor', cascade='all, delete, delete-orphan')
    apuestas = db.relationship('Apuesta', cascade='all, delete, delete-orphan')
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))

class Competidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_competidor = db.Column(db.String(128))
    probabilidad = db.Column(db.Numeric)
    puntaje = db.Column(db.Numeric)
    cuota = db.Column(db.Numeric);
    es_ganador = db.Column(db.Boolean, default=False)
    estatus = db.Column(db.Boolean, default=False)
    id_EventoDeportivo = db.Column(db.Integer, db.ForeignKey('EventoDeportivo.id'))

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    usuario = db.Column(db.String(50))
    email = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    rol = db.Column(db.Boolean, default=True)
    no_cuenta = db.Column(db.String(20))
    nombre_banco = db.Column(db.String(50))
    saldo = db.Column(db.Numeric, default=0)
    medio_pago = db.Column(db.String(50))
    EventoDeportivos = db.relationship('EventoDeportivo', cascade='all, delete, delete-orphan')

class EventoMarcador(EventoDeportivo):
    id = db.Column(db.Integer, primary_key=True)
    id_marcador = db.Column(db.Integer, db.ForeignKey("marcador.id"))

class Marcador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marcador = db.Column(db.String(50))
    id_competidor_ganador = db.Column(db.Integer, db.ForeignKey('competidor.id'))
    id_competidor_perdedor  = db.Column(db.Integer, db.ForeignKey('competidor.id'))

class EventoCarrera(EventoDeportivo):
    id = db.Column(db.Integer, primary_key=True)
    id_competidor_ganador = db.Column(db.Integer, db.ForeignKey('competidor.id'))




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


class CarreraSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Carrera
        include_relationships = True
        load_instance = True

    competidores = fields.List(fields.Nested(CompetidorSchema()))
    apuestas = fields.List(fields.Nested(ApuestaSchema()))
    ganancia_casa = fields.Float()


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True


class ReporteSchema(Schema):
    carrera = fields.Nested(CarreraSchema())
    ganancia_casa = fields.Float()