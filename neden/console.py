import sys

try:
    import readline  # Autocompletado en Unix/macOS
except ImportError:
    readline = None  # No disponible en Windows

from kernel.sector5 import Sector5Kernel
from kernel.system_state import SystemState
from kernel.process_manager import ProcessManager
from kernel.auth import AuthModule

def main():
    state = SystemState()
    pm = ProcessManager(system_state=state)
    auth = AuthModule()
    sector5 = Sector5Kernel(state, pm, auth)

    logged_in_user = None

    COMMANDS = [
        "help", "login", "logout", "status", "start", "stop",
        "pause", "resume", "enter", "list", "exit"
    ]

    if readline:
        def completer(text, state):
            options = [cmd for cmd in COMMANDS if cmd.startswith(text)]
            if state < len(options):
                return options[state] + " "
            else:
                return None

        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

    print("=== Bienvenido a la consola NEDEN ===")
    print("Escribe 'help' para ver los comandos disponibles.")

    while True:
        prompt = f"NEDEN[{logged_in_user if logged_in_user else 'guest'}]> "
        try:
            cmd = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo de la consola NEDEN...")
            break

        if not cmd:
            continue

        parts = cmd.split()
        command = parts[0].lower()

        if command == "help":
            print("""
Comandos disponibles:
  login <usuario> <contraseña> - Iniciar sesión
  logout - Cerrar sesión actual
  status - Mostrar estado del sistema
  start <proceso> - Iniciar un proceso
  stop <proceso> - Detener un proceso
  pause <proceso> - Pausar un proceso
  resume <proceso> - Reanudar un proceso
  list - Listar procesos activos
  enter <sector> - Cambiar sector activo
  help - Mostrar esta ayuda
  exit - Salir de la consola
            """)

        elif command == "login":
            if logged_in_user:
                print(f"[ERROR] Ya hay un usuario logueado: '{logged_in_user}'. Haz logout primero.")
                continue
            if len(parts) != 3:
                print("Uso: login <usuario> <contraseña>")
                continue
            username, password = parts[1], parts[2]
            if sector5.auth.validate(username, password):
                logged_in_user = username
                sector5.system_state.add_connection(username)
                print(f"[OK] Usuario '{username}' logueado correctamente.")
            else:
                print("[ERROR] Credenciales incorrectas.")

        elif command == "logout":
            if not logged_in_user:
                print("[ERROR] No hay ningún usuario logueado.")
            else:
                print(f"[INFO] Usuario '{logged_in_user}' ha cerrado sesión.")
                logged_in_user = None

        elif command == "status":
            if not logged_in_user:
                print("[ERROR] Debes iniciar sesión primero.")
                continue
            sector5.report()

        elif command == "start":
            if not logged_in_user:
                print("[ERROR] Debes iniciar sesión primero.")
                continue
            if len(parts) != 2:
                print("Uso: start <proceso>")
                continue
            process_name = parts[1]
            sector5.process_manager.start_process(process_name)

        elif command == "stop":
            if not logged_in_user:
                print("[ERROR] Debes iniciar sesión primero.")
                continue
            if len(parts) != 2:
                print("Uso: stop <proceso>")
                continue
            process_name = parts[1]
            sector5.process_manager.stop_process(process_name)

        elif command == "pause":
            if not logged_in_user:
                print("[ERROR] Debes iniciar sesión primero.")
                continue
            if len(parts) != 2:
                print("Uso: pause <proceso>")
                continue
            process_name = parts[1]
            sector5.process_manager.pause_process(process_name)

        elif command == "resume":
            if not logged_in_user:
                print("[ERROR] Debes iniciar sesión primero.")
                continue
            if len(parts) != 2:
                print("Uso: resume <proceso>")
                continue
            process_name = parts[1]
            sector5.process_manager.resume_process(process_name)

        elif command == "list":
            if not logged_in_user:
                print("[ERROR] Debes iniciar sesión primero.")
                continue
            processes = sector5.process_manager.list_processes()
            if not processes:
                print("[INFO] No hay procesos activos.")
            else:
                print("[INFO] Procesos activos:")
                for p, status in processes.items():
                    print(f"  - {p}: {status}")

        elif command == "enter":
            if not logged_in_user:
                print("[ERROR] Debes iniciar sesión primero.")
                continue
            if len(parts) != 2:
                print("Uso: enter <sector>")
                continue
            sector = parts[1]
            sector5.system_state.update_sector(sector)

        elif command == "exit":
            print("Saliendo de la consola NEDEN...")
            break

        else:
            print(f"[ERROR] Comando desconocido: {command}")

if __name__ == "__main__":
    main()
