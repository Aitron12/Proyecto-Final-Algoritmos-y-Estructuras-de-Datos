from abc import ABC, abstractmethod
from mensaje import Mensaje

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
