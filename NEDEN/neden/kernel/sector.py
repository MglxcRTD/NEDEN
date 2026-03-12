# kernel/sector.py

class Sector:
    def __init__(self, name, description="", status="standby"):
        self.name = name  # Nombre identificativo del sector (p. ej. "Forest", "Desert")
        self.description = description  # Texto descriptivo del sector
        self.status = status  # Estado del sector: "standby", "online", "locked", etc.
        self.towers = {i: "inactive" for i in range(1, 11)} # 10 Torres/Nodos por sector

    def activate(self):
        self.status = "online"
        print(f"[SECTOR] Sector '{self.name}' activado.")

    def deactivate(self):
        self.status = "standby"
        print(f"[SECTOR] Sector '{self.name}' desactivado.")

    def lock(self):
        self.status = "locked"
        print(f"[SECTOR] Sector '{self.name}' bloqueado.")

    def unlock(self):
        self.status = "online"
        print(f"[SECTOR] Sector '{self.name}' desbloqueado.")

    def set_tower_status(self, tower_id, status):
        if tower_id in self.towers:
            self.towers[tower_id] = status

    def __str__(self):
        return f"Sector(name='{self.name}', status='{self.status}', description='{self.description}')"
