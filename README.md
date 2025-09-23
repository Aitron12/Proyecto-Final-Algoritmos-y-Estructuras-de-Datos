  # Proyecto-Final-Algoritmos-y-Estructuras-de-Datos
#Trabajo integrador propuesto por la materia Estructura de Datos en la Universidad Nacional Guillermo Brown
 Sistema de Correo en Python

Este código pone en practica sistema básico de gestión de correo electrónico utilizando programación orientada a objetos en Python.

## Estructura del código
- **Mensaje:** La clase Mensaje describe un mensaje individual, almacenando el remitente,  destinatario, contenido y una tupla con información adicional. Los atributos son privados y se accede a ellos mediante propiedades, lo que garantiza el encapsulamiento y la protección de los datos.

- **Carpeta:** La clase Carpeta forma una carpeta de mensajes, como la bandeja de entrada o enviados. Utiliza una lista para almacenar los mensajes y ajusta métodos para agregar y listar los mismos.

- **Icorreo** La interfaz ICorreo define los sistema esenciales que debe implementar cualquier clase que gestione correos: enviar, recibir y listar mensajes. Esto asegura que todas las clases derivadas cumplan con la misma estructura y funcionalidad mínima.

- **Usuario:** La clase Usuario representa a un usuario del sistema. Cada usuario tiene un nombre y un diccionario de carpetas, permitiendo organizar los mensajes en diferentes niveles. Implementa los métodos definidos en la interfaz para enviar, recibir y listar mensajes
  
- **ServidorCorreo:** La clase ServidorCorreo ejecuta como el gestor central del sistema, manteniendo un registro de los usuarios y facilitando el envío de mensajes entre ellos. Utiliza un diccionario para almacenar los usuarios registrados y manera para registrar nuevos usuarios y enviar mensajes.

- El diseño sigue los principios de encapsulamiento, reutilización y claridad, facilitando la extensión y el mantenimiento del sistema. Se emplean listas para la gestión de colecciones de mensajes, tuplas para información adicional inmutable y diccionarios para el acceso seguro a carpetas y usuarios.
  
## Cómo usarlo
1. Descarga el código.
2. Ejecuta el archivo principal en Python 3.
3. Modifica o amplía las clases según tus necesidades.

## Más información
- [Documentación de clases abstractas en Python](https://docs.python.org/3/library/abc.html)
- [Listas en Python](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
