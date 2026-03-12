# kernel/sector5.py

from kernel.system_state import SystemState
from kernel.process_manager import ProcessManager
from kernel.auth import AuthModule
from kernel.sector import Sector  # Importamos la nueva clase Sector

class Sector5Kernel:
    def __init__(self, system_state, process_manager, auth_module):
        self.system_state = system_state
        self.process_manager = process_manager
        self.auth = auth_module 
        self.sectors = {}  # Diccionario para almacenar sectores por nombre

    def add_sector(self, sector):
        if sector.name in self.sectors:
            print(f"[WARNING] El sector '{sector.name}' ya existe.")
        else:
            self.sectors[sector.name] = sector
            print(f"[INFO] Sector '{sector.name}' añadido al sistema.")

    def activate_sector(self, sector_name):
        sector = self.sectors.get(sector_name)
        if sector:
            sector.activate()
            self.system_state.update_sector(sector_name)
        else:
            print(f"[ERROR] Sector '{sector_name}' no encontrado.")

    def deactivate_sector(self, sector_name):
        sector = self.sectors.get(sector_name)
        if sector:
            sector.deactivate()
            # Opcional: actualizar estado del sistema si el sector activo se desactiva
            if self.system_state.active_sector == sector_name:
                self.system_state.update_sector(None)
        else:
            print(f"[ERROR] Sector '{sector_name}' no encontrado.")

    def list_sectors(self):
        if not self.sectors:
            print("[INFO] No hay sectores registrados.")
            return
        print("=== Sectores disponibles ===")
        for sector in self.sectors.values():
            print(f"- {sector.name} (Estado: {sector.status}) - {sector.description}")

    def report(self):
        status = self.system_state.get_status()
        print("=== Reporte del sistema ===")
        print(f"Sector activo: {status['active_sector']}")
        print(f"Carga del sistema: {status['system_load']}")
        print(f"Conexiones activas: {status['connections']}")
        print("Últimos eventos:")
        for event in status["event_log"]:
            print(f" - {event}")
