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

    def test_GetAllEventosDisponibles(self):
        endpoint_eventosDisponibles = '/eventod/eventosdisponibles'
        solicitud_eventosDisponibles = json.loads(self.client.get(endpoint_eventosDisponibles,
                                                  data = '',
                                                  headers={'Content-Type': 'application/json'}).get_data())
        self.assertTrue(len(solicitud_eventosDisponibles) > 0)

    def test_TerminarEventoConGanador(self):
        endpoint_terminarEvento = "/eventod/terminarevento/{}/{}".format(1, 1)
        eventoDesportivo = json.loads(self.client.post(endpoint_terminarEvento,
                                                  data = '',
                                                  headers={'Content-Type': 'application/json'}).get_data())
        self.assertTrue(eventoDesportivo['estado'] == 'False')