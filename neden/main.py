from kernel.sector5 import Sector5Kernel
from kernel.system_state import SystemState
from kernel.process_manager import ProcessManager
from kernel.auth import AuthModule

# Inicialización de los módulos
state = SystemState()
pm = ProcessManager()
auth = AuthModule()  # ✅ No le pases lista

# Crear instancia del núcleo
sector5 = Sector5Kernel(state, pm, auth)

# Validar usuario y ejecutar proceso
usuario = "explorer01"
password = "secure123"

if sector5.auth.validate(usuario, password):  # ✅ Añade la contraseña
    print(f"[OK] Acceso concedido a '{usuario}'")
    sector5.process_manager.start_process("AccesoSectorForest")
    print(sector5.process_manager.active_processes)


    print(f"[INFO] Estado del sistema: {sector5.system_state.__dict__}")
else:
    print(f"[ERROR] Acceso denegado para '{usuario}'")
