#GRUPO 40 - COMISION 2 - PROFESORES : AMBROSSIO DIEGO - BIANCO ANGEL LEONARDO
#INTEGRANTES : YAPURA TOMAS - TOMYYAPURA9@GMAIL.COM
               GIULIANA CRISTALDO - GIULIANACRISTALDO16@GMAIL.COM
               AARON LARA - CHUKYDCLAZADA@HOTMAIL.COM

# Proyecto_Correcciones — Correciones y versión funcional

Este directorio contiene una copia corregida y verificada del paquete `mod_mail` y artefactos de prueba. Está pensada para presentar las correcciones solicitadas para el trabajo académico sin modificar el código original.

Resumen de las correcciones realizadas

- Completadas e implementadas las clases principales:
  - `Mensaje` — modelo de mensaje con metadatos y propiedad `urgente`.
  - `Carpeta` — almacena mensajes y soporta una cola de prioridad para mensajes urgentes (usa `heapq`).
  - `Usuario` — administra un árbol de carpetas (raíz, bandeja_entrada, enviados) y operaciones de búsqueda/movimiento.
  - `ServidorCorreo` — servidor simple que registra usuarios y entrega mensajes localmente.
- Implementada la modelación de la red de servidores con la clase `Network` (grafo) y envío entre servidores usando BFS.
- Añadidos tests unitarios con `pytest` que cubren prioridad en carpetas, envío local y envío a través de la red.
- Añadido un demo sencillo `Cuarta_entrega_tomy_demo.py` que muestra un envío entre usuarios.

Estructura de este directorio

```
Proyecto_Correcciones/
├─ mod_mail/
│  ├─ __init__.py
│  ├─ mensaje.py
│  ├─ carpeta.py
│  ├─ icorreo.py
│  ├─ usuario.py
│  ├─ servidor.py
│  └─ network.py
├─ Cuarta_entrega_tomy_demo.py
└─ tests/
   └─ test_mod_mail.py
```

Requisitos

- Python 3.10+ (probado con 3.13 en el entorno de desarrollo)
- `pytest` para ejecutar tests

Instalación y ejecución (PowerShell)

1) Abrir PowerShell y situarse en este directorio:

```powershell
Set-Location "c:\Users\Aitro\OneDrive\Escritorio\Aaron\Programacion\Codigos py\Estructura_De_Datos\Tp_1.py\Avance_Tp\Proyecto_Correcciones"
```

2) (Opcional) Crear y activar un entorno virtual:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Instalar dependencias mínimas:

```powershell
py -3 -m pip install --upgrade pip
py -3 -m pip install pytest
```

4) Ejecutar el demo:

```powershell
py -3 .\Cuarta_entrega_tomy_demo.py
```

Salida esperada: se imprimirá la lista de mensajes en la bandeja de entrada del destinatario.

Ejecutar tests

```powershell
py -3 -m pytest -q
```

Deberías ver algo como:

```
3 passed in 0.0Xs
```

Verificación completa

- El demo y los tests han sido ejecutados localmente en este entorno y pasaron.
- Si quieres comprobar en una máquina limpia: clona el repositorio, instala `pytest` y ejecuta `pytest` y el demo como se indica arriba.

Notas importantes

- No se modificó el árbol original del proyecto: los archivos originales se conservaron tal como estaban en la carpeta raíz del trabajo. Esta carpeta `Proyecto_Correcciones` contiene la versión corregida y lista para revisión.
- Si quieres que aplique las correcciones directamente sobre los archivos originales o que prepare un `pull request`/branch con los cambios, dímelo y lo preparo (haré backup antes de sobrescribir).

Qué entrego con esto

- Código corregido y listo para ejecutar (`mod_mail` con Network y prioridad en Carpeta).
- Demo de uso (`Cuarta_entrega_tomy_demo.py`).
- Tests unitarios (`tests/test_mod_mail.py`) que demuestran el comportamiento correcto.



