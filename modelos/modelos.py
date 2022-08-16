from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class Apuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor_apostado = db.Column(db.Numeric)
    ganancia = db.Column(db.Numeric, default=0)
    nombre_apostador = db.Column(db.String(128))
    id_competidor = db.Column(db.Integer, db.ForeignKey('competidor.id'))
    id_carrera = db.Column(db.Integer, db.ForeignKey('carrera.id'))


class Carrera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_carrera = db.Column(db.String(128))
    abierta = db.Column(db.Boolean, default=True)
    competidores = db.relationship('Competidor', cascade='all, delete, delete-orphan')
    apuestas = db.relationship('Apuesta', cascade='all, delete, delete-orphan')
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))


class Competidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_competidor = db.Column(db.String(128))
    probabilidad = db.Column(db.Numeric)
    cuota = db.Column(db.Numeric);
    es_ganador = db.Column(db.Boolean, default=False)
    id_carrera = db.Column(db.Integer, db.ForeignKey('carrera.id'))


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    carreras = db.relationship('Carrera', cascade='all, delete, delete-orphan')


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