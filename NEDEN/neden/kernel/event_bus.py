# kernel/event_bus.py

class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        """Permite a un módulo escuchar un tipo de evento específico."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def emit(self, event_type, data=None):
        """Lanza un evento para que todos los suscriptores reaccionen."""
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(data)