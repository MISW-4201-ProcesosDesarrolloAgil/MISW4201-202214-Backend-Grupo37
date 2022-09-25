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

    '''def test_crear_apuesta(self):
        nueva_carrera = {
            "nombre": self.data_factory.sentence(),
            "competidores": [
                {
                    "probabilidad": 0.6,
                    "competidor": "Lorem ipsum"
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                }
            ]
        }

        endpoint_carreras = "/usuario/{}/carreras".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nueva_carrera = self.client.post(endpoint_carreras,
                                                   data=json.dumps(nueva_carrera),
                                                   headers=headers)

        respuesta_al_crear_carrera = json.loads(solicitud_nueva_carrera.get_data())
        id_carrera = respuesta_al_crear_carrera["id"]
        id_competidor = \
        [x for x in respuesta_al_crear_carrera["competidores"] if x["nombre_competidor"] == "Lorem ipsum"][0]["id"]

        nueva_apuesta = {
            "valor_apostado": random.uniform(100, 500000),
            "nombre_apostador": "Angelica Benitez",
            "id_competidor": id_competidor,
            "id_carrera": id_carrera
        }

        endpoint_apuestas = "/apuestas"

        solicitud_nueva_apuesta = self.client.post(endpoint_apuestas,
                                                   data=json.dumps(nueva_apuesta),
                                                   headers=headers)

        respuesta_al_crear_apuesta = json.loads(solicitud_nueva_apuesta.get_data())
        nombre_apostador = respuesta_al_crear_apuesta["nombre_apostador"]

        self.assertEqual(solicitud_nueva_apuesta.status_code, 200)
        self.assertEqual(nombre_apostador, "Angelica Benitez") '''

    def test_GetApuestaById(self):
        endpoint_apuesta = '/apuesta/{}'.format(1)
        headers = {'Content-Type': 'application/json'}

        solicitud_getAuesta = json.loads(self.client.get(endpoint_apuesta,
                                                   data= '',
                                                   headers=headers).get_data())
        #print(str(solicitud_getAuesta['id_EventoDeportivo']))
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
        #print(str(solicitud_CrearApuesta['id']))
        self.assertIsNotNone(solicitud_CrearApuesta['id'])

