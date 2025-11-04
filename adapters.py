from collections import deque
from typing import List, Optional, Tuple, Dict
import heapq

class Mensaje:
    def __init__(self, remitente: str, destinatario: str, contenido: str, info_extra: tuple = ("importante",)):
        self._remitente = remitente
        self._destinatario = destinatario
        self._contenido = contenido
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
        return any(str(x).lower() == "urgente" for x in self._info_extra)

    def __repr__(self) -> str:
        return f"Mensaje({self.remitente}->{self.destinatario}: {self.contenido[:30]!r})"


class Carpeta:
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._mensajes: List[Mensaje] = []
        self._subcarpetas: List['Carpeta'] = []
        self._urgent_heap: List[Tuple[int, int, Mensaje]] = []
        self._counter = 0

    @property
    def nombre(self):
        return self._nombre

    def agregar_mensaje(self, mensaje: Mensaje):
        self._mensajes.append(mensaje)
        if mensaje.urgente:
            heapq.heappush(self._urgent_heap, (0, self._counter, mensaje))
            self._counter += 1

    def listar_mensajes(self) -> List[Mensaje]:
        return list(self._mensajes)

    def listar_mensajes_priorizados(self) -> List[Mensaje]:
        urgentes = [item[2] for item in sorted(self._urgent_heap)]
        normales = [m for m in self._mensajes if not m.urgente]
        return urgentes + normales

    def pop_mensaje_urgente(self) -> Optional[Mensaje]:
        if not self._urgent_heap:
            return None
        _, _, mensaje = heapq.heappop(self._urgent_heap)
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
            carpeta_destino.agregar_mensaje(mensaje)

    def buscar_mensajes(self, texto: str) -> List[Mensaje]:
        encontrados = [m for m in self._mensajes if texto in m.contenido or texto in m.remitente]
        for sub in self._subcarpetas:
            encontrados.extend(sub.buscar_mensajes(texto))
        return encontrados


class ICorreo:
    def enviar_mensaje(self, mensaje: Mensaje):
        raise NotImplementedError()

    def recibir_mensaje(self, mensaje: Mensaje):
        raise NotImplementedError()

    def listar_mensajes(self, carpeta: str):
        raise NotImplementedError()


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

    def _buscar_carpeta(self, nombre: str, carpeta: Optional[Carpeta] = None) -> Optional[Carpeta]:
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

    def listar_mensajes_priorizados(self, carpeta: str):
        c = self._buscar_carpeta(carpeta)
        return c.listar_mensajes_priorizados() if c else []

    def mover_mensaje(self, mensaje: Mensaje, origen: str, destino: str):
        origen_carpeta = self._buscar_carpeta(origen)
        destino_carpeta = self._buscar_carpeta(destino)
        if origen_carpeta and destino_carpeta:
            origen_carpeta.mover_mensaje(mensaje, destino_carpeta)

    def buscar_mensajes(self, texto: str):
        return self._raiz.buscar_mensajes(texto)


class ServidorCorreo:
    def __init__(self, name: str):
        self.name = name
        self._usuarios: Dict[str, Usuario] = {}

    def registrar_usuario(self, usuario: Usuario):
        self._usuarios[usuario.nombre] = usuario

    def tiene_usuario(self, nombre: str) -> bool:
        return nombre in self._usuarios

    def obtener_usuario(self, nombre: str) -> Optional[Usuario]:
        return self._usuarios.get(nombre)

    def enviar(self, mensaje: Mensaje):
        if mensaje.destinatario in self._usuarios:
            self._usuarios[mensaje.destinatario].recibir_mensaje(mensaje)
        if mensaje.remitente in self._usuarios:
            self._usuarios[mensaje.remitente].enviar_mensaje(mensaje)


class Network:
    def __init__(self):
        self._adj: Dict[str, set] = {}
        self._servers: Dict[str, ServidorCorreo] = {}

    def add_server(self, server: ServidorCorreo):
        self._servers[server.name] = server
        self._adj.setdefault(server.name, set())

    def connect(self, name_a: str, name_b: str):
        self._adj.setdefault(name_a, set()).add(name_b)
        self._adj.setdefault(name_b, set()).add(name_a)

    def find_path_bfs(self, start: str, predicate):
        if start not in self._servers:
            return None
        visited = set()
        q = deque([(start, [start])])
        while q:
            current_name, path = q.popleft()
            if current_name in visited:
                continue
            visited.add(current_name)
            server = self._servers.get(current_name)
            if server and predicate(server):
                return path
            for neighbor in self._adj.get(current_name, []):
                if neighbor not in visited:
                    q.append((neighbor, path + [neighbor]))
        return None

    def send_message(self, origin_server_name: str, mensaje: Mensaje) -> bool:
        def predicate(s: ServidorCorreo):
            return s.tiene_usuario(mensaje.destinatario)

        path = self.find_path_bfs(origin_server_name, predicate)
        if not path:
            return False
        dest_name = path[-1]
        dest_server = self._servers.get(dest_name)
        if dest_server:
            dest_server.enviar(mensaje)
            return True
        return False
