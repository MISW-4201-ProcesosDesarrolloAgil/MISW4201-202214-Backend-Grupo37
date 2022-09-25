import json
from unittest import TestCase

from faker import Faker
from faker.generator import random

from app import app
class TestApuesta(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

        nuevo_usuario = {
            "usuario": self.data_factory.name(),
            "contrasena": self.data_factory.word()
        }

    def test_GetApuestaById(self):
        endpoint_apuesta = '/apuesta/{}'.format(1)
        headers = {'Content-Type': 'application/json'}

        solicitud_getAuesta = json.loads(self.client.get(endpoint_apuesta,
                                                   data= '',
                                                   headers=headers).get_data())
        self.assertAlmostEqual(solicitud_getAuesta['id_EventoDeportivo'], 1)
    
    def test_VistaApuestas(self):
        data = {"valor_apostado": 5000,
                "id_competidor": 3, 
                "id_apostador" : 1,
                "id_competidor": 4,
                "id_EventoDeportivo": 3}
        endpoint_apuesta = '/apuestas/{}'.format(data['id_apostador'])
        headers = {'Content-Type': 'application/json'}
        solicitud_CrearApuesta = json.loads(self.client.post(endpoint_apuesta,
                                                   data= json.dumps(data),
                                                   headers=headers).get_data())
        self.assertIsNotNone(solicitud_CrearApuesta['id'])

