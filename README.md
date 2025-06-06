# NEDEN - Consola Interactiva

Esta es una consola interactiva para el proyecto NEDEN, inspirada en el terminal de Jeremy de Código Lyoko.

## Requisitos

- Python 3.x
- Estructura del proyecto:

neden/
│
├── kernel/
│ ├── auth.py
│ ├── process_manager.py
│ ├── sector5.py
│ └── system_state.py
├── console.py
└── README.md

perl
Copiar
Editar

## Cómo ejecutar la consola

Desde la raíz del proyecto, abre la terminal y ejecuta:

```bash
python console.py
Comandos disponibles
login <usuario> <contraseña>: Inicia sesión con un usuario válido.

status: Muestra el estado actual del sistema.

start <proceso>: Inicia un proceso.

stop <proceso>: Detiene un proceso.

enter <sector>: Cambia el sector activo.

help: Muestra esta ayuda.

exit: Sale de la consola.

Usuarios por defecto
Usuario: explorer01

Contraseña: secure123

Usuario: admin01

Contraseña: rootaccess

Próximos pasos
Añadir roles y permisos para comandos.

Mejorar la interfaz de la consola.

Añadir más comandos y funcionalidades.

¡Disfruta explorando NEDEN!
