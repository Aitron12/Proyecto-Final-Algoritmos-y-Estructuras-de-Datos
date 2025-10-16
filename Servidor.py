from usuario import Usuario
from mensaje import Mensaje

class ServidorCorreo:
    def __init__(self):
        self._usuarios = {}

    def registrar_usuario(self, usuario: Usuario):
        self._usuarios[usuario.nombre] = usuario

    def enviar(self, mensaje: Mensaje):
        if mensaje.destinatario in self._usuarios:
            self._usuarios[mensaje.destinatario].recibir_mensaje(mensaje)
        if mensaje.remitente in self._usuarios:
            self._usuarios[mensaje.remitente].enviar_mensaje(mensaje)
