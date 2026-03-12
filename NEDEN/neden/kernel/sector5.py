# kernel/sector5.py

from kernel.system_state import SystemState
from kernel.process_manager import ProcessManager
from kernel.auth import AuthModule
from kernel.sector import Sector 
from kernel.fs import Directory, File
from kernel.event_bus import EventBus  # <--- Nuevo módulo
from kernel.vexa import VexaAI        # <--- V.E.X.A

class Sector5Kernel:
    def __init__(self, system_state, process_manager, auth_module):
        self.system_state = system_state
        self.process_manager = process_manager
        self.auth = auth_module 
        self.sectors = {}
        
        # --- Comunicación y Eventos ---
        self.event_bus = EventBus()
        self._setup_internal_events()

        # --- Inteligencia Artificial ---
        self.vexa = VexaAI(self.event_bus, self.process_manager)

        # --- Inicialización del VFS ---
        self.root = Directory("/")
        self.current_dir = self.root
        self._build_initial_fs()

    def _setup_internal_events(self):
        """Define reacciones automáticas a eventos del sistema."""
        # Si ocurre una alerta de seguridad, el kernel puede responder
        self.event_bus.subscribe("SECURITY_BREACH", self._on_security_breach)
        # Si un proceso crítico falla
        self.event_bus.subscribe("PROCESS_CRASH", self._on_process_crash)

    def tick(self):
        """Simula el paso del tiempo para la IA."""
        self.event_bus.emit("VEXA_TICK")

    def _on_security_breach(self, data):
        user = data.get("user", "unknown")
        entity = data.get("entity", "unknown")
        tower_id = data.get("tower")
        
        print(f"\a[ALERTA NÚCLEO] INTRUSIÓN DETECTADA. Vector: {entity}")
        self.system_state.log_event("KERNEL_ACTION", f"Protocolo de defensa contra {entity or user}")
        
        # Si hay una torre involucrada y un sector activo, marcamos la torre como corrupta
        if tower_id and self.system_state.active_sector:
            active_sec_name = self.system_state.active_sector
            if active_sec_name in self.sectors:
                self.sectors[active_sec_name].set_tower_status(tower_id, "corrupted")

    def _on_process_crash(self, data):
        proc_name = data.get("name")
        print(f"[RECOVERY] Intentando reiniciar proceso crítico: {proc_name}")
        # Aquí el kernel podría decidir reiniciar el proceso automáticamente
        self.process_manager.start_process(proc_name, load_impact=20.0)

    def _build_initial_fs(self):
        """Crea la estructura de directorios base."""
        bin_dir = Directory("bin", self.root)
        sys_dir = Directory("sys", self.root)
        home_dir = Directory("home", self.root)
        sectors_dir = Directory("sectors", self.root)

        self.root.add_node(bin_dir)
        self.root.add_node(sys_dir)
        self.root.add_node(home_dir)
        self.root.add_node(sectors_dir)

        readme = File("README.txt", "Sistema NEDEN v0.1\nBus de Eventos: Activo.", home_dir)
        home_dir.add_node(readme)

    # --- Gestión de Sectores ---

    def add_sector(self, sector):
        if sector.name in self.sectors:
            print(f"[WARNING] El sector '{sector.name}' ya existe.")
        else:
            self.sectors[sector.name] = sector
            sector_mount = Directory(sector.name, self.root.children["sectors"])
            self.root.children["sectors"].add_node(sector_mount)
            print(f"[INFO] Sector '{sector.name}' añadido y montado en /sectors/{sector.name}")

    def activate_sector(self, sector_name):
        sector = self.sectors.get(sector_name)
        if sector:
            sector.activate()
            self.system_state.update_sector(sector_name)
            # Emitimos un evento de que un sector ha cambiado
            self.event_bus.emit("SECTOR_CHANGED", {"name": sector_name, "status": "online"})
        else:
            print(f"[ERROR] Sector '{sector_name}' no encontrado.")

    def deactivate_sector(self, sector_name):
        sector = self.sectors.get(sector_name)
        if sector:
            sector.deactivate()
            if self.system_state.active_sector == sector_name:
                self.system_state.update_sector(None)
            self.event_bus.emit("SECTOR_CHANGED", {"name": sector_name, "status": "standby"})
        else:
            print(f"[ERROR] Sector '{sector_name}' no encontrado.")

    # --- Comandos del VFS ---

    def list_dir(self):
        print(f" Contenido de {self.current_dir.name}:")
        if not self.current_dir.children:
            print("  (vacio)")
            return
        for name, node in self.current_dir.children.items():
            type_label = "[DIR]" if isinstance(node, Directory) else "[FILE]"
            print(f"  {type_label} {name}")

    def change_dir(self, path):
        if path == "..":
            if self.current_dir.parent:
                self.current_dir = self.current_dir.parent
            return
        
        if path in self.current_dir.children:
            target = self.current_dir.children[path]
            if isinstance(target, Directory):
                self.current_dir = target
            else:
                print(f"[ERROR] '{path}' no es un directorio.")
        else:
            print(f"[ERROR] No se encuentra el directorio: {path}")

    def make_dir(self, name):
        if name in self.current_dir.children:
            print(f"[ERROR] '{name}' ya existe.")
            return
        new_dir = Directory(name, parent=self.current_dir)
        self.current_dir.add_node(new_dir)
        print(f"[FS] Directorio '{name}' creado.")

    def touch_file(self, name, content=""):
        if name in self.current_dir.children:
            # Actualizar timestamp (simulado)
            print(f"[FS] Archivo '{name}' actualizado.")
            return
        new_file = File(name, content, parent=self.current_dir)
        self.current_dir.add_node(new_file)
        print(f"[FS] Archivo '{name}' creado.")

    def remove_item(self, name):
        if name not in self.current_dir.children:
            print(f"[ERROR] '{name}' no encontrado.")
            return
        
        item = self.current_dir.children[name]
        if isinstance(item, Directory) and item.children:
            print(f"[ERROR] El directorio '{name}' no está vacío.")
            return
            
        self.current_dir.remove_node(name)
        print(f"[FS] '{name}' eliminado.")

    def read_file(self, filename):
        if filename in self.current_dir.children:
            target = self.current_dir.children[filename]
            if isinstance(target, File):
                print(f"--- {filename} ---\n{target.content}\n--- EOF ---")
            else:
                print(f"[ERROR] '{filename}' es un directorio.")
        else:
            print(f"[ERROR] Archivo '{filename}' no encontrado.")

    # --- Utilidades y Control ---

    def check_access(self, username, required_role):
        if self.auth.has_permission(username, required_role):
            return True
        
        print(f"[SECURITY] Acceso Denegado para '{username}'.")
        self.system_state.log_event("SECURITY_ALERT", f"Intento no autorizado por '{username}'")
        
        # Disparamos un evento IPC para que el núcleo lo gestione
        self.event_bus.emit("SECURITY_BREACH", {"user": username, "required": required_role})
        return False

    def report(self):
        status = self.system_state.get_status()
        print("=== Reporte del sistema ===")
        print(f"Directorio actual: {self.current_dir.name}")
        print(f"Sector activo: {status['active_sector']}")
        print(f"Carga del sistema: {status['system_load']}%")
        print(f"Conexiones activas: {status['connections']}")
        print("Últimos eventos:")
        for event in status["event_log"]:
            print(f" - {event}")