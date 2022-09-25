import json
from unittest import TestCase

from faker import Faker
from faker.generator import random

from app import app

class TestEventoDeportivo(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

        nuevo_usuario = {
            "usuario": self.data_factory.name(),
            "contrasena": self.data_factory.word()
        }

        '''solicitud_nuevo_usuario = self.client.post("/signin",
                                                   data=json.dumps(nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})

        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())

        self.token = respuesta_al_crear_usuario["token"]
        self.usuario_code = respuesta_al_crear_usuario["id"] '''
    
    def test_GetAllEventosDisponibles(self):
        endpoint_eventosDisponibles = '/eventod/eventosdisponibles'
        solicitud_eventosDisponibles = json.loads(self.client.get(endpoint_eventosDisponibles,
                                                  data = '',
                                                  headers={'Content-Type': 'application/json'}).get_data())
        #print(solicitud_eventosDisponibles)
        self.assertTrue(len(solicitud_eventosDisponibles) > 0)

    def test_TerminarEventoConGanador(self):
        #endpoint_carreras = "/usuario/{}/carreras".format(str(self.usuario_code))
        endpoint_terminarEvento = "/eventod/terminarevento/{}/{}".format(1, 1)
        eventoDesportivo = json.loads(self.client.post(endpoint_terminarEvento,
                                                  data = '',
                                                  headers={'Content-Type': 'application/json'}).get_data())
        #print(eventoDesportivo['estado'])
        self.assertTrue(eventoDesportivo['estado'] == 'False')