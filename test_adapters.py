import pytest
from adapters import Mensaje, Carpeta, Usuario, ServidorCorreo, Network


def test_prioridad_carpeta():
    c = Carpeta("test")
    m1 = Mensaje("a", "b", "normal", info_extra=("info",))
    m2 = Mensaje("a", "b", "urgente", info_extra=("urgente",))
    m3 = Mensaje("a", "b", "otro urgente", info_extra=("urgente", "importante"))

    c.agregar_mensaje(m1)
    c.agregar_mensaje(m2)
    c.agregar_mensaje(m3)

    priorizados = c.listar_mensajes_priorizados()
    assert priorizados[0].urgente
    assert priorizados[1].urgente
    assert any(not m.urgente for m in priorizados[2:])

    popped = c.pop_mensaje_urgente()
    assert popped.urgente


def test_envio_local_servidor():
    s = ServidorCorreo("s1")
    u1 = Usuario("alice")
    u2 = Usuario("bob")
    s.registrar_usuario(u1)
    s.registrar_usuario(u2)

    m = Mensaje("alice", "bob", "hola")
    s.enviar(m)

    inbox = u2.listar_mensajes("bandeja_entrada")
    assert any(msg.contenido == "hola" for msg in inbox)


def test_network_send_bfs():
    s1 = ServidorCorreo("s1")
    s2 = ServidorCorreo("s2")
    s3 = ServidorCorreo("s3")

    alice = Usuario("alice")
    carlos = Usuario("carlos")
    s1.registrar_usuario(alice)
    s3.registrar_usuario(carlos)

    net = Network()
    net.add_server(s1)
    net.add_server(s2)
    net.add_server(s3)
    net.connect("s1", "s2")
    net.connect("s2", "s3")

    msg = Mensaje("alice", "carlos", "hola desde s1")
    delivered = net.send_message("s1", msg)
    assert delivered
    inbox = s3.obtener_usuario("carlos").listar_mensajes("bandeja_entrada")
    assert any(m.contenido == "hola desde s1" for m in inbox)
