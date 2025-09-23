# Clases principales y encapsulamiento

# Importamos herramientas para clases abstractas y anotaciones de tipo
from abc import ABC, abstractmethod
from typing import List

# Clase que representa un mensaje de correo
class Mensaje:
    def __init__(self, remitente: str, destinatario: str, contenido: str):
        # Guardamos el remitente, destinatario y contenido como atributos privados
        self._remitente = remitente
        self._destinatario = destinatario
        self._contenido = contenido
        self._info_extra = ("importante", "urgente")  # Tupla
    
    # Propiedad para acceder al remitente de forma segura
    @property
    def remitente(self):
        return self._remitente

    # Propiedad para acceder al destinatario de forma segura
    @property
    def destinatario(self):
        return self._destinatario

    # Propiedad para acceder al contenido de forma segura
    @property
    def contenido(self):
        return self._contenido

    # Propiedad para acceder a la tupla de información extra
    @property
    def info_extra(self):
        return self._info_extra

# Clase que representa una carpeta de mensajes (como bandeja de entrada o enviados)
class Carpeta:
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._mensajes: List[Mensaje] = []  # Lista para almacenar mensajes

    @property
    def nombre(self):
        return self._nombre

    # Método para agregar un mensaje a la carpeta
    def agregar_mensaje(self, mensaje: Mensaje):
        self._mensajes.append(mensaje)

    # Método para listar todos los mensajes de la carpeta
    def listar_mensajes(self):
        return self._mensajes

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

# Clase que representa a un usuario del sistema de correo
class Usuario(ICorreo):
    def __init__(self, nombre: str):
        self._nombre = nombre
        # Diccionario para almacenar las carpetas del usuario
        self._carpetas = {
            "bandeja_entrada": Carpeta("bandeja_entrada"),
            "enviados": Carpeta("enviados")
        }

    @property
    def nombre(self):
        return self._nombre

    # Método para enviar un mensaje (lo guarda en la carpeta de enviados)
    def enviar_mensaje(self, mensaje: Mensaje):
        self._carpetas["enviados"].agregar_mensaje(mensaje)

    # Método para recibir un mensaje (lo guarda en la bandeja de entrada)
    def recibir_mensaje(self, mensaje: Mensaje):
        self._carpetas["bandeja_entrada"].agregar_mensaje(mensaje)

    # Método para listar los mensajes de una carpeta específica
    def listar_mensajes(self, carpeta: str):
        if carpeta in self._carpetas:
            return self._carpetas[carpeta].listar_mensajes()
        return []

# Clase que representa el servidor de correo, encargado de gestionar usuarios y mensajes
class ServidorCorreo:
    def __init__(self):
        self._usuarios = {}  # Diccionario para almacenar usuarios por nombre

    # Método para registrar un nuevo usuario en el servidor
    def registrar_usuario(self, usuario: Usuario):
        self._usuarios[usuario.nombre] = usuario

    # Método para enviar un mensaje entre usuarios registrados
    def enviar(self, mensaje: Mensaje):
        if mensaje.destinatario in self._usuarios:
            self._usuarios[mensaje.destinatario].recibir_mensaje(mensaje)
        if mensaje.remitente in self._usuarios:

            self._usuarios[mensaje.remitente].enviar_mensaje(mensaje)
