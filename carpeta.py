from typing import List, Optional, Tuple
import heapq
from .mensaje import Mensaje


class Carpeta:
    """Carpeta que almacena mensajes y puede contener subcarpetas.

    Implementa una cola de prioridad para mensajes urgentes usando heapq.
    - _mensajes: lista de todos los mensajes (orden de llegada)
    - _urgent_heap: heap con tuplas (priority, count, mensaje) donde priority menor => mayor prioridad
    """
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._mensajes: List[Mensaje] = []
        self._subcarpetas: List['Carpeta'] = []
        self._urgent_heap: List[Tuple[int, int, Mensaje]] = []
        self._counter = 0  # para ordenar mensajes con la misma prioridad

    @property
    def nombre(self):
        return self._nombre

    def agregar_mensaje(self, mensaje: Mensaje):
        """Agrega un mensaje a la carpeta. Si es urgente, también lo encola en la heap de prioridad."""
        # Guardamos en la lista normal
        self._mensajes.append(mensaje)
        # Si el mensaje está marcado como 'urgente', lo agregamos a la cola priorizada
        if mensaje.urgente:
            # prioridad 0 para urgente; counter para estabilidad
            heapq.heappush(self._urgent_heap, (0, self._counter, mensaje))
            self._counter += 1

    def listar_mensajes(self) -> List[Mensaje]:
        """Devuelve los mensajes en el orden de llegada (sin alterar la cola priorizada)."""
        return list(self._mensajes)

    def listar_mensajes_priorizados(self) -> List[Mensaje]:
        """Devuelve una lista en la que los mensajes urgentes aparecen primero (sin consumir la heap)."""
        urgentes = [item[2] for item in sorted(self._urgent_heap)]
        normales = [m for m in self._mensajes if not m.urgente]
        return urgentes + normales

    def pop_mensaje_urgente(self) -> Optional[Mensaje]:
        """Extrae y devuelve el siguiente mensaje urgente de mayor prioridad, si existe."""
        if not self._urgent_heap:
            return None
        _, _, mensaje = heapq.heappop(self._urgent_heap)
        # También eliminar de la lista regular si está presente
        try:
            self._mensajes.remove(mensaje)
        except ValueError:
            pass
        return mensaje

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
            # si estaba en la heap priorizada, no intentamos eliminarlo ahí por simplicidad
            carpeta_destino.agregar_mensaje(mensaje)

    def buscar_mensajes(self, texto: str) -> List[Mensaje]:
        encontrados = [m for m in self._mensajes if texto in m.contenido or texto in m.remitente]
        for sub in self._subcarpetas:
            encontrados.extend(sub.buscar_mensajes(texto))
        return encontrados
