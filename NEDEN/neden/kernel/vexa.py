# kernel/vexa.py
import random

class VexaAI:
    """
    V.E.X.A. (Virtual Entropy Xeno Algorithm)
    Una IA autónoma que busca consumir recursos del sistema generando
    entidades hostiles (monstruos de datos).
    """
    def __init__(self, event_bus, process_manager):
        self.event_bus = event_bus
        self.pm = process_manager
        self.aggression_level = 0.0
        self.active = True
        
        # Suscribirse a eventos para reaccionar
        self.event_bus.subscribe("SECTOR_CHANGED", self._on_sector_activity)
        self.event_bus.subscribe("VEXA_TICK", self._decide_action)

    def _on_sector_activity(self, data):
        """Si el usuario entra en un sector, VEXA se interesa."""
        if data.get("status") == "online":
            self.aggression_level += 0.2
            # Silencioso, no imprime spam en consola, solo aumenta amenaza interna

    def _decide_action(self, _=None):
        """Ciclo de decisión de la IA (llamado periódicamente)."""
        if not self.active:
            return

        # Probabilidad de ataque basada en agresión y carga actual
        chance = random.random()
        if chance < (0.1 + self.aggression_level):
            self._initiate_attack()

    def _initiate_attack(self):
        # 1. Seleccionar Sector y Torre
        # Necesitamos acceso a los sectores del sistema, lo simulamos o pedimos al evento
        # Para simplificar, generamos un evento de ataque que el kernel procesará
        threats = [
            ("Polymorphic_Worm", 5.0),
            ("Logic_Bomb_Swarm", 15.0),
            ("Null_Pointer_Entity", 25.0),
            ("Recursive_Nightmare", 40.0)
        ]
        
        name, load = random.choice(threats)
        unique_name = f"{name}::{random.randint(1000,9999)}"
        target_tower = random.randint(1, 10)
        
        print(f"\n[ALERTA] V.E.X.A. activando Nodo de Enlace {target_tower}...")
        
        # Emitimos evento de ataque complejo
        self.event_bus.emit("SECURITY_BREACH", {
            "user": "VEXA_NODE_ACTIVATE", 
            "entity": unique_name,
            "tower": target_tower
        })
        
        # Intentar iniciar el proceso malicioso
        current_load = self.pm._get_current_load()
        if current_load + load > self.pm.MAX_CAPACITY:
            pass # Sobrecarga silenciosa
        
        self.pm.processes[unique_name] = {"status": "running", "load": load, "type": "hostile"}
        self.pm._sync_load()

    def neutralize(self):
        self.aggression_level = 0.0
        self.active = False
        print("[V.E.X.A.] Algoritmo neutralizado temporalmente.")