import sqlalchemy
import json
from unittest import TestCase
from faker import Faker
from faker.generator import random
from app import app


class TestUsuario(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

        nuevo_usuario = {
            "usuario": self.data_factory.name(),
            "contrasena": self.data_factory.word()
        }

    def test_GetAllUsuarios(self):
        endpoint_carreras = "/usuarios"
        solicitud_all_Users = json.loads(self.client.get(endpoint_carreras).get_data())
        self.assertIsNotNone(solicitud_all_Users)

    def test_SignInAdmin(self):
        nuevo_usuario_admin = {
            "usuario": self.data_factory.name(),
            "u_email":  self.data_factory.email(),
            "contrasena": self.data_factory.word(), 
            "phone": self.data_factory.word() , 
            "rol": 0, 
            "no_cuenta": '', 
            "nombre_banco":'', 
            "saldo": '0.0',
            "medio_pago": ''
        }
        endpoint_carreras = "/signin/admin"
        solicitud_Sing_Admin = self.client.post(endpoint_carreras,
                            data= json.dumps(nuevo_usuario_admin),
                            headers={'Content-Type': 'application/json'}).get_data().decode("utf-8")
        self.assertTrue(str.__contains__(solicitud_Sing_Admin, "usuario admin creado exitosamente"))

    def test_SignInApostador(self):
        nuevo_usuario_Apostador = {
            "usuario": self.data_factory.name(),
            "u_email":  self.data_factory.email(),
            "contrasena": self.data_factory.word(), 
            "phone": self.data_factory.word() , 
            "rol": 1, 
            "no_cuenta": '', 
            "nombre_banco":'', 
            "saldo": '0.0',
            "medio_pago": ''
        }
        endpoint_carreras = "/signin/apostador"
        solicitud_Sing_Apostador =  self.client.post(endpoint_carreras,
                                    data= json.dumps(nuevo_usuario_Apostador),
                                    headers={'Content-Type': 'application/json'}).get_data().decode("utf-8")
        self.assertTrue(str.__contains__(solicitud_Sing_Apostador, "usuario apostador creado exitosamente"))
    
    def test_LogInSuccessful(self):
        usuario_LogIn = {
            "usuario": "Sebas",
            "contrasena": "12345",
        }
        endpoint_login = '/login'
        solicitud_LogIn =  self.client.post(endpoint_login,
                            data= json.dumps(usuario_LogIn),
                            headers={'Content-Type': 'application/json'}).get_data().decode("utf-8")
        self.assertTrue(str.__contains__(solicitud_LogIn, "Inicio de sesi"))

    def test_LogInNotSuccessful(self):
        usuario_LogIn = {
            "usuario": self.data_factory.name(),
            "contrasena": self.data_factory.word(),
        }
        endpoint_login = '/login'
        solicitud_LogIn =  self.client.post(endpoint_login,
                            data= json.dumps(usuario_LogIn),
                            headers={'Content-Type': 'application/json'}).get_data().decode("utf-8")
        self.assertFalse(str.__contains__(solicitud_LogIn, "Inicio de sesi"))
    
    def test_GetAllCompetidores(self):
        endpoint_competidores = "/competidores"
        solicitud_all_Competidores = json.loads(self.client.get(endpoint_competidores).get_data())
        self.assertIsNotNone(solicitud_all_Competidores)