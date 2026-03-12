# kernel/process_manager.py

class ProcessManager:
    def __init__(self, system_state=None):
        self.processes = {}  # Estructura: {nombre: {"status": str, "load": float}}
        self.system_state = system_state
        self.MAX_CAPACITY = 100.0  # Carga máxima permitida (100%)

    def log_event(self, level, message):
        if self.system_state:
            self.system_state.log_event(level, message)

    def _get_current_load(self):
        """Calcula la carga total actual de todos los procesos en ejecución."""
        return sum(p["load"] for p in self.processes.values() if p["status"] == "running")

    def start_process(self, name, load_impact=10.0):
        """Inicia un proceso si hay recursos disponibles."""
        if name in self.processes:
            print(f"[WARNING] Proceso '{name}' ya existe.")
            return

        current_load = self._get_current_load()
        if current_load + load_impact > self.MAX_CAPACITY:
            print(f"[ERROR] Recursos insuficientes para '{name}'. Carga actual: {current_load}%")
            self.log_event("CRITICAL", f"Fallo de recursos al iniciar {name}")
            return

        self.processes[name] = {"status": "running", "load": load_impact}
        self._sync_load()
        
        print(f"[PROCESS] '{name}' iniciado (Consumo: {load_impact}%).")
        self.log_event("INFO", f"Proceso iniciado: {name} ({load_impact}%)")

    def pause_process(self, name):
        """Pausa un proceso y libera su carga de CPU."""
        if self.processes.get(name, {}).get("status") == "running":
            self.processes[name]["status"] = "paused"
            self._sync_load()
            print(f"[PROCESS] '{name}' pausado. Recursos liberados.")
            self.log_event("INFO", f"Proceso pausado: {name}")

    def resume_process(self, name):
        """Reanuda un proceso si hay capacidad tras haber sido pausado."""
        if self.processes.get(name, {}).get("status") == "paused":
            load_impact = self.processes[name]["load"]
            if self._get_current_load() + load_impact > self.MAX_CAPACITY:
                print(f"[ERROR] Imposible reanudar '{name}': Sobrecarga de CPU.")
                return
            
            self.processes[name]["status"] = "running"
            self._sync_load()
            print(f"[PROCESS] '{name}' reanudado.")
            self.log_event("INFO", f"Proceso reanudado: {name}")

    def stop_process(self, name):
        """Detiene un proceso y lo elimina de la tabla de procesos."""
        if name in self.processes:
            del self.processes[name]
            self._sync_load()
            print(f"[PROCESS] Proceso '{name}' detenido.")
            self.log_event("INFO", f"Proceso detenido: {name}")

    def _sync_load(self):
        """Actualiza la carga en el SystemState global."""
        if self.system_state:
            self.system_state.system_load = self._get_current_load()

    def list_processes(self):
        """Devuelve una copia amigable de los procesos para la consola."""
        return self.processes.copy()

    @property
    def active_processes(self):
        """Devuelve solo los procesos que están en ejecución."""
        return {n: p for n, p in self.processes.items() if p["status"] == "running"}