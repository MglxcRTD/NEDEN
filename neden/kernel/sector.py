# kernel/sector.py

class Sector:
    def __init__(self, name, description="", status="inactive"):
        self.name = name  # Nombre identificativo del sector (p. ej. "Forest", "Desert")
        self.description = description  # Texto descriptivo del sector
        self.status = status  # Estado del sector: "inactive", "active", "locked", etc.

    def activate(self):
        self.status = "active"
        print(f"[SECTOR] Sector '{self.name}' activado.")

    def deactivate(self):
        self.status = "inactive"
        print(f"[SECTOR] Sector '{self.name}' desactivado.")

    def lock(self):
        self.status = "locked"
        print(f"[SECTOR] Sector '{self.name}' bloqueado.")

    def unlock(self):
        self.status = "active"
        print(f"[SECTOR] Sector '{self.name}' desbloqueado.")

    def __str__(self):
        return f"Sector(name='{self.name}', status='{self.status}', description='{self.description}')"
