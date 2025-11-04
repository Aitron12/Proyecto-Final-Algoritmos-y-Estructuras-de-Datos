from collections import deque
from typing import Dict, Set, List, Optional
from .servidor import ServidorCorreo
from .mensaje import Mensaje


class Network:
    """Modela una red de servidores como un grafo no dirigido.

    Permite conectar servidores y enviar mensajes recorriendo la red
    para encontrar el servidor que contiene al destinatario (BFS).
    """

    def __init__(self):
        # adjacency list: server_name -> set(server_name)
        self._adj: Dict[str, Set[str]] = {}
        # mapping name -> ServidorCorreo
        self._servers: Dict[str, ServidorCorreo] = {}

    def add_server(self, server: ServidorCorreo):
        self._servers[server.name] = server
        self._adj.setdefault(server.name, set())

    def connect(self, name_a: str, name_b: str):
        self._adj.setdefault(name_a, set()).add(name_b)
        self._adj.setdefault(name_b, set()).add(name_a)

    def find_path_bfs(self, start: str, predicate) -> Optional[List[str]]:
        """Busca (BFS) el primer servidor que cumpla predicate(server) y devuelve el path de nombres.

        predicate recibe (ServidorCorreo) y devuelve bool.
        """
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
        """Envía mensaje desde origin_server_name buscando el servidor que contiene al destinatario.

        Devuelve True si se entregó, False si no se encontró el destinatario.
        """
        # predicate para encontrar servidor con usuario destino
        def predicate(s: ServidorCorreo):
            return s.tiene_usuario(mensaje.destinatario)

        path = self.find_path_bfs(origin_server_name, predicate)
        if not path:
            return False
        # Simular paso del mensaje por la ruta (podríamos añadir logs/latencias)
        dest_name = path[-1]
        dest_server = self._servers.get(dest_name)
        if dest_server:
            dest_server.enviar(mensaje)
            return True
        return False
