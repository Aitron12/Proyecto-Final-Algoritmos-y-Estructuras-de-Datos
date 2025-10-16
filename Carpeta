from typing import List, Optional
from mensaje import Mensaje

class Carpeta:
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._mensajes: List[Mensaje] = []
        self._subcarpetas: List['Carpeta'] = []

    @property
    def nombre(self):
        return self._nombre

    def agregar_mensaje(self, mensaje: Mensaje):
        self._mensajes.append(mensaje)

    def listar_mensajes(self):
        return self._mensajes

    def agregar_subcarpeta(self, subcarpeta: 'Carpeta'):
        self._subcarpetas.append(subcarpeta)

    def obtener_subcarpeta(self, nombre: str) -> Optional['Carpeta']:
        for sub in self._subcarpetas:
            if sub.nombre == nombre:
                return sub
        return None

    def mover_mensaje(self, mensaje: Mensaje, carpeta_destino: 'Carpeta'):
        if mensaje in self._mensajes:
            self._mensajes.remove(mensaje)
            carpeta_destino.agregar_mensaje(mensaje)

    def buscar_mensajes(self, texto: str) -> List[Mensaje]:
        encontrados = [m for m in self._mensajes if texto in m.contenido or texto in m.remitente]
        for sub in self._subcarpetas:
            encontrados.extend(sub.buscar_mensajes(texto))
        return encontrados
