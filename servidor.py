from typing import Dict
from .usuario import Usuario
from .mensaje import Mensaje


class ServidorCorreo:
    """Servidor que almacena usuarios (cada servidor representa una máquina/instancia).

    Ahora incluye un nombre identificador para integrarlo en una red de servidores.
    """
    def __init__(self, name: str):
        self.name = name
        self._usuarios: Dict[str, Usuario] = {}

    def registrar_usuario(self, usuario: Usuario):
        """Registra un usuario local en este servidor."""
        self._usuarios[usuario.nombre] = usuario

    def tiene_usuario(self, username: str) -> bool:
        return username in self._usuarios

    def obtener_usuario(self, username: str):
        """Devuelve el objeto Usuario o None si no existe."""
        return self._usuarios.get(username)

    def enviar(self, mensaje: Mensaje):
        """Envía/entrega un mensaje entre usuarios registrados en este servidor.

        Si el destinatario está aquí, lo recibe. También guarda el mensaje en la carpeta "enviados"
        del remitente si el remitente también está registrado localmente.
        """
        # entregar al destinatario si está en este servidor
        if mensaje.destinatario in self._usuarios:
            self._usuarios[mensaje.destinatario].recibir_mensaje(mensaje)
        # guardar en enviados del remitente si está en este servidor
        if mensaje.remitente in self._usuarios:
            self._usuarios[mensaje.remitente].enviar_mensaje(mensaje)
