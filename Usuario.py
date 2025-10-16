from carpeta import Carpeta
from mensaje import Mensaje
from icorreo import ICorreo
from typing import Optional

class Usuario(ICorreo):
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._raiz = Carpeta("raiz")
        self._crear_estructura_basica()

    def _crear_estructura_basica(self):
        entrada = Carpeta("bandeja_entrada")
        enviados = Carpeta("enviados")
        self._raiz.agregar_subcarpeta(entrada)
        self._raiz.agregar_subcarpeta(enviados)

    @property
    def nombre(self):
        return self._nombre

    def _buscar_carpeta(self, nombre: str, carpeta: Carpeta = None) -> Optional[Carpeta]:
        if carpeta is None:
            carpeta = self._raiz
        if carpeta.nombre == nombre:
            return carpeta
        for sub in carpeta._subcarpetas:
            resultado = self._buscar_carpeta(nombre, sub)
            if resultado:
                return resultado
        return None

    def enviar_mensaje(self, mensaje: Mensaje):
        carpeta = self._buscar_carpeta("enviados")
        if carpeta:
            carpeta.agregar_mensaje(mensaje)

    def recibir_mensaje(self, mensaje: Mensaje):
        carpeta = self._buscar_carpeta("bandeja_entrada")
        if carpeta:
            carpeta.agregar_mensaje(mensaje)

    def listar_mensajes(self, carpeta: str):
        c = self._buscar_carpeta(carpeta)
        return c.listar_mensajes() if c else []

    def mover_mensaje(self, mensaje: Mensaje, origen: str, destino: str):
        origen_carpeta = self._buscar_carpeta(origen)
        destino_carpeta = self._buscar_carpeta(destino)
        if origen_carpeta and destino_carpeta:
            origen_carpeta.mover_mensaje(mensaje, destino_carpeta)

    def buscar_mensajes(self, texto: str):
        return self._raiz.buscar_mensajes(texto)
