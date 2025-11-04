class Mensaje:
    """Representa un mensaje de correo.

    Atributos principales:
    - remitente, destinatario, contenido
    - info_extra: tupla con metadatos (p. ej. ("importante", "urgente"))

    Se añade la propiedad `urgente` para identificar mensajes de alta prioridad.
    """
    def __init__(self, remitente: str, destinatario: str, contenido: str, info_extra: tuple = ("importante",)):
        # se mantienen los comentarios y la intención de proteger atributos
        self._remitente = remitente
        self._destinatario = destinatario
        self._contenido = contenido
        # info_extra puede incluir la palabra 'urgente' para marcar prioridad
        self._info_extra = info_extra

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

    @property
    def urgente(self) -> bool:
        """True si el mensaje está marcado como urgente en info_extra."""
        return any(str(x).lower() == "urgente" for x in self._info_extra)

    def __repr__(self) -> str:
        return f"Mensaje({self.remitente}->{self.destinatario}: {self.contenido[:30]!r})"
