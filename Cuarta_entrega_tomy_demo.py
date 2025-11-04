from mod_mail.mensaje import Mensaje
from mod_mail.usuario import Usuario
from mod_mail.servidor import ServidorCorreo


def main():
    servidor = ServidorCorreo("server1")

    # Crear usuarios
    aaron = Usuario("aaron")
    tomas = Usuario("tomas")

    servidor.registrar_usuario(aaron)
    servidor.registrar_usuario(tomas)

    # Enviar un mensaje de aaron a tomas
    m = Mensaje(remitente="aaron", destinatario="tomas", contenido="Hola Tomás, ¿cómo estás?", info_extra=("urgente",))
    servidor.enviar(m)

    # Listar mensajes en la bandeja de Tomás
    inbox_tomas = tomas.listar_mensajes("bandeja_entrada")
    print("Mensajes en la bandeja de Tomás:")
    for msg in inbox_tomas:
        print(f"- De: {msg.remitente} -> {msg.contenido}")


if __name__ == "__main__":
    main()
