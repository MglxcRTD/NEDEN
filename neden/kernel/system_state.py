class SystemState:
    def __init__(self):
        self.active_sector = None
        self.system_load = 0.0
        self.connections = []
        self.event_log = []

    def update_sector(self, sector):
        self.active_sector = sector  # Puede ser str o None
        if sector:
            self.log_event("INFO", f"Sector activo cambiado a {sector}")
        else:
            self.log_event("INFO", "Sector activo desactivado (None)")

    def add_connection(self, user):
        self.connections.append(user)
        self.log_event("SECURITY", f"Conexión establecida con '{user}'")

    def log_event(self, level, message):
        event = f"[{level}] {message}"
        self.event_log.append(event)
        print(event)

    def get_status(self):
        return {
            "active_sector": self.active_sector,
            "system_load": self.system_load,
            "connections": self.connections.copy(),
            "event_log": self.event_log[-5:]  # últimos 5 eventos
        }
