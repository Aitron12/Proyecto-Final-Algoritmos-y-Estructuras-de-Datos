# Clase que representa un mensaje de correo
class Mensaje:
    def __init__(self, remitente: str, destinatario: str, contenido: str):
        self._remitente = remitente
        self._destinatario = destinatario
        self._contenido = contenido
        self._info_extra = ("importante", "urgente")

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
