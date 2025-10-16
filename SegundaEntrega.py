# Importamos herramientas para clases abstractas y anotaciones de tipo
from abc import ABC, abstractmethod
from typing import List, Optional

# Clase que representa un mensaje de correo
class Mensaje:
    def __init__(self, remitente: str, destinatario: str, contenido: str):
        # Atributos privados para proteger la información
        self._remitente = remitente
        self._destinatario = destinatario
        self._contenido = contenido
        self._info_extra = ("importante", "urgente")  # Tupla como ejemplo de metadatos

    # Propiedades para acceder a los atributos de forma segura
    @property
    def remitente(self):
        return self._remitente

    @property
    def destinatario(self):
        return self._destinatario

    @property
    def contenido(self):
        return self._contenido

    @property
    def info_extra(self):
        return self._info_extra


# Clase Carpeta ahora es recursiva: puede contener subcarpetas
class Carpeta:
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._mensajes: List[Mensaje] = []
        self._subcarpetas: List['Carpeta'] = []  # Lista de subcarpetas

    @property
    def nombre(self):
        return self._nombre

    # Agrega un mensaje a esta carpeta
    def agregar_mensaje(self, mensaje: Mensaje):
        self._mensajes.append(mensaje)

    # Devuelve todos los mensajes de esta carpeta
    def listar_mensajes(self):
        return self._mensajes

    # Agrega una subcarpeta a esta carpeta
    def agregar_subcarpeta(self, subcarpeta: 'Carpeta'):
        self._subcarpetas.append(subcarpeta)

    # Busca una subcarpeta por nombre (no recursiva)
    def obtener_subcarpeta(self, nombre: str) -> Optional['Carpeta']:
        for sub in self._subcarpetas:
            if sub.nombre == nombre:
                return sub
        return None

    # Mueve un mensaje desde esta carpeta a otra
    def mover_mensaje(self, mensaje: Mensaje, carpeta_destino: 'Carpeta'):
        if mensaje in self._mensajes:
            self._mensajes.remove(mensaje)
            carpeta_destino.agregar_mensaje(mensaje)

    # Búsqueda recursiva de mensajes por texto (en contenido o remitente)
    def buscar_mensajes(self, texto: str) -> List[Mensaje]:
        encontrados = [m for m in self._mensajes if texto in m.contenido or texto in m.remitente]
        for sub in self._subcarpetas:
            encontrados.extend(sub.buscar_mensajes(texto))
        return encontrados


# Interfaz que define los métodos que debe tener cualquier clase de correo
class ICorreo(ABC):
    @abstractmethod
    def enviar_mensaje(self, mensaje: Mensaje):
        pass

    @abstractmethod
    def recibir_mensaje(self, mensaje: Mensaje):
        pass

    @abstractmethod
    def listar_mensajes(self, carpeta: str):
        pass


# Clase Usuario ahora gestiona un árbol de carpetas
class Usuario(ICorreo):
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._raiz = Carpeta("raiz")  # Carpeta raíz del árbol
        self._crear_estructura_basica()

    # Crea las carpetas básicas por defecto
    def _crear_estructura_basica(self):
        entrada = Carpeta("bandeja_entrada")
        enviados = Carpeta("enviados")
        self._raiz.agregar_subcarpeta(entrada)
        self._raiz.agregar_subcarpeta(enviados)

    @property
    def nombre(self):
        return self._nombre

    # Búsqueda recursiva de una carpeta por nombre
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

    # Envía un mensaje y lo guarda en la carpeta "enviados"
    def enviar_mensaje(self, mensaje: Mensaje):
        carpeta = self._buscar_carpeta("enviados")
        if carpeta:
            carpeta.agregar_mensaje(mensaje)

    # Recibe un mensaje y lo guarda en la "bandeja_entrada"
    def recibir_mensaje(self, mensaje: Mensaje):
        carpeta = self._buscar_carpeta("bandeja_entrada")
        if carpeta:
            carpeta.agregar_mensaje(mensaje)

    # Lista los mensajes de una carpeta específica
    def listar_mensajes(self, carpeta: str):
        c = self._buscar_carpeta(carpeta)
        return c.listar_mensajes() if c else []

    # Mueve un mensaje de una carpeta a otra
    def mover_mensaje(self, mensaje: Mensaje, origen: str, destino: str):
        origen_carpeta = self._buscar_carpeta(origen)
        destino_carpeta = self._buscar_carpeta(destino)
        if origen_carpeta and destino_carpeta:
            origen_carpeta.mover_mensaje(mensaje, destino_carpeta)

    # Búsqueda recursiva de mensajes por texto (remitente o contenido)
    def buscar_mensajes(self, texto: str):
        return self._raiz.buscar_mensajes(texto)


# Clase que representa el servidor de correo
class ServidorCorreo:
    def __init__(self):
        self._usuarios = {}  # Diccionario de usuarios registrados

    # Registra un nuevo usuario
    def registrar_usuario(self, usuario: Usuario):
        self._usuarios[usuario.nombre] = usuario

    # Envía un mensaje entre usuarios registrados
    def enviar(self, mensaje: Mensaje):
        if mensaje.destinatario in self._usuarios:
            self._usuarios[mensaje.destinatario].recibir_mensaje(mensaje)
        if mensaje.remitente in self._usuarios:
            self._usuarios[mensaje.remitente].enviar_mensaje(mensaje)

# Modular imports
from mensaje import Mensaje
from carpeta import Carpeta
from icorreo import ICorreo
from usuario import Usuario
from servidor import ServidorCorreo
