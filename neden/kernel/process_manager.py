class ProcessManager:
    def __init__(self, system_state=None):
        self.processes = {}
        self.system_state = system_state

    def log_event(self, level, message):
        if self.system_state:
            self.system_state.log_event(level, message)

    def start_process(self, name):
        if name in self.processes:
            print(f"[WARNING] Proceso '{name}' ya está en ejecución.")
            self.log_event("warning", f"Intento duplicado de iniciar '{name}'.")
            return
        self.processes[name] = "running"
        print(f"[PROCESS] Iniciado proceso '{name}'.")
        self.log_event("info", f"Proceso iniciado: {name}")

    def pause_process(self, name):
        if self.processes.get(name) == "running":
            self.processes[name] = "paused"
            print(f"[PROCESS] Pausado proceso '{name}'.")
            self.log_event("info", f"Proceso pausado: {name}")

    def resume_process(self, name):
        if self.processes.get(name) == "paused":
            self.processes[name] = "running"
            print(f"[PROCESS] Reanudado proceso '{name}'.")
            self.log_event("info", f"Proceso reanudado: {name}")

    def stop_process(self, name):
        if name in self.processes:
            del self.processes[name]
            print(f"[PROCESS] Proceso '{name}' detenido.")
            self.log_event("info", f"Proceso detenido: {name}")

    def list_processes(self):
        return self.processes.copy()

    @property
    def active_processes(self):
        return self.processes.copy()
