import json
from unittest import TestCase

from faker import Faker
from faker.generator import random

from app import app


class TestCarrera(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

        nuevo_usuario = {
            "usuario": self.data_factory.name(),
            "contrasena": self.data_factory.word()
        }

        solicitud_nuevo_usuario = self.client.post("/signin",
                                                   data=json.dumps(nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})

        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())

        self.token = respuesta_al_crear_usuario["token"]
        self.usuario_code = respuesta_al_crear_usuario["id"]

    def test_crear_carrera(self):
        nueva_carrera = {
            "nombre": self.data_factory.sentence(),
            "competidores": [
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
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

        self.assertEqual(solicitud_nueva_carrera.status_code, 200)

    def test_editar_carrera(self):
        nueva_carrera_1 = {
            "nombre": "Sakhir. 57 vueltas",
            "competidores": [
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
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

        nueva_carrera_2 = {
            "nombre": "Sakhir 130 vueltas",
            "competidores": [
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

        endpoint_crear_carrera = "/usuario/{}/carreras".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nueva_carrera_1 = self.client.post(endpoint_crear_carrera,
                                                     data=json.dumps(nueva_carrera_1),
                                                     headers=headers)

        respuesta_al_crear_carrera = json.loads(solicitud_nueva_carrera_1.get_data())
        id_carrera = respuesta_al_crear_carrera["id"]

        endpoint_editar_carrera = "/carrera/{}".format(str(id_carrera))

        solicitud_editar_carrera = self.client.put(endpoint_editar_carrera,
                                                   data=json.dumps(nueva_carrera_2),
                                                   headers=headers)

        carrera_editada = json.loads(solicitud_editar_carrera.get_data())

        self.assertEqual(solicitud_editar_carrera.status_code, 200)
        self.assertEqual(carrera_editada["nombre_carrera"], "Sakhir 130 vueltas")

    def test_obtener_carrera_por_id(self):
        nueva_carrera = {
            "nombre": "GP de Miami",
            "competidores": [
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

        endpoint_crear_carrera = "/usuario/{}/carreras".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nueva_carrera = self.client.post(endpoint_crear_carrera,
                                                   data=json.dumps(nueva_carrera),
                                                   headers=headers)

        respuesta_al_crear_carrera = json.loads(solicitud_nueva_carrera.get_data())
        id_carrera = respuesta_al_crear_carrera["id"]

        endpoint_obtener_carrera = "/carrera/{}".format(str(id_carrera))

        solicitud_consultar_carrera_por_id = self.client.get(endpoint_obtener_carrera, headers=headers)
        carrera_obtenida = json.loads(solicitud_consultar_carrera_por_id.get_data())

        self.assertEqual(solicitud_consultar_carrera_por_id.status_code, 200)
        self.assertEqual(carrera_obtenida["nombre_carrera"], "GP de Miami")

    def test_obtener_carreras(self):
        nueva_carrera = {
            "nombre": self.data_factory.sentence(),
            "competidores": [
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

        endpoint = "/usuario/{}/carreras".format(str(self.usuario_code))
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_consultar_carreras_antes = self.client.get(endpoint, headers=headers)
        total_carreras_antes = len(json.loads(solicitud_consultar_carreras_antes.get_data()))

        solicitud_consultar_carreras_despues = self.client.post(endpoint,
                                                                data=json.dumps(nueva_carrera),
                                                                headers=headers)

        total_carreras_despues = len(json.loads(solicitud_consultar_carreras_despues.get_data()))

        self.assertEqual(solicitud_consultar_carreras_despues.status_code, 200)
        self.assertGreater(total_carreras_despues, total_carreras_antes)

    def test_eliminar_carrera(self):
        nueva_carrera = {
            "nombre": self.data_factory.sentence(),
            "competidores": [
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
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

        id_carrera = json.loads(solicitud_nueva_carrera.get_data())["id"]
        solicitud_consultar_carreras_antes = self.client.get(endpoint_carreras, headers=headers)
        total_carreras_antes = len(json.loads(solicitud_consultar_carreras_antes.get_data()))

        endpoint_carrera = "/carrera/{}".format(str(id_carrera))

        solicitud_eliminar_carrera = self.client.delete(endpoint_carrera, headers=headers)
        solicitud_consultar_carreras_despues = self.client.get(endpoint_carreras, headers=headers)
        total_carreras_despues = len(json.loads(solicitud_consultar_carreras_despues.get_data()))
        solicitud_consultar_carrera_por_id = self.client.get(endpoint_carrera, headers=headers)

        self.assertLess(total_carreras_despues, total_carreras_antes)
        self.assertEqual(solicitud_consultar_carrera_por_id.status_code, 404)
        self.assertEqual(solicitud_eliminar_carrera.status_code, 204)
