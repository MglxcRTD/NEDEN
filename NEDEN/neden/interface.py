# neden/interface.py
import sys
import math
import random

try:
    import customtkinter as ctk
except ImportError:
    print("[ERROR SISTEMA] Falta la librería visual 'customtkinter'.")
    print("Ejecuta este comando para instalarla: pip install customtkinter")
    sys.exit(1)

import threading
import time
from kernel.sector5 import Sector5Kernel
from kernel.system_state import SystemState
from kernel.process_manager import ProcessManager
from kernel.auth import AuthModule
from kernel.sector import Sector

# Configuración Visual "Aether"
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")  # Acentos azules

class NedenDashboard(ctk.CTk):
    def __init__(self, kernel):
        super().__init__()
        self.kernel = kernel
        self.title("NEDEN OS - TERMINAL SUPERORDENADOR")
        self.geometry("1200x800")
        
        # Paleta de Colores Inspirada en los laboratorios y el mundo virtual
        self.color_primary = "#0099FF"   # Azul Escáner
        self.color_danger = "#FF2A2A"    # Rojo X.A.N.A
        self.color_bg = "#F5F5FA"        # Blanco laboratorio
        self.color_grid = "#D0D5E0"      # Gris suave para estructuras
        self.configure(fg_color=self.color_bg)

        self._setup_ui()
        self._start_update_loop()

    def _setup_ui(self):
        # Layout de rejilla
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Panel Lateral (Sidebar) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#E1E6EE")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="NEDEN\nSYSTEM", font=ctk.CTkFont(family="Impact", size=28), text_color=self.color_primary)
        self.logo.pack(padx=20, pady=20)

        self.btn_scan = ctk.CTkButton(self.sidebar, text="VIRTUALIZAR SCAN", fg_color=self.color_primary, command=self.scan_action)
        self.btn_scan.pack(padx=20, pady=10)
        
        self.btn_purge = ctk.CTkButton(self.sidebar, text="CÓDIGO: LYOKO (PURGA)", fg_color=self.color_danger, command=self.purge_action)
        self.btn_purge.pack(padx=20, pady=10)

        # --- Área Principal ---
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Cabecera de Estado
        self.status_frame = ctk.CTkFrame(self.main_area, fg_color="white")
        self.status_frame.pack(fill="x", pady=(0, 20))
        
        self.lbl_sector = ctk.CTkLabel(self.status_frame, text="SECTOR ACTIVO: ...", font=("Arial", 14, "bold"), text_color="#333")
        self.lbl_sector.pack(side="left", padx=20, pady=10)
        
        self.lbl_load = ctk.CTkLabel(self.status_frame, text="INTEGRIDAD DATOS: 100%", font=("Arial", 14, "bold"), text_color="#333")
        self.lbl_load.pack(side="right", padx=20, pady=10)

        # --- VISOR 3D (Simulado con Canvas) ---
        # Reemplazamos la lista por un "Holomapa" táctico
        self.map_container = ctk.CTkFrame(self.main_area, fg_color="#000510") # Fondo negro digital para contraste del radar
        self.map_container.pack(fill="both", expand=True, pady=10)
        
        self.canvas = ctk.CTkCanvas(self.map_container, bg="#050A15", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Overlay de texto
        self.overlay_label = ctk.CTkLabel(self.map_container, text="VISOR TÁCTICO - TIEMPO REAL", text_color="white", bg_color="#050A15", font=("Courier", 12))
        self.overlay_label.place(x=15, y=15)
        
        # Consola de Logs
        self.log_box = ctk.CTkTextbox(self.main_area, height=120, font=("Consolas", 11), fg_color="white", text_color="black", border_width=2, border_color="#E0E0E0")
        self.log_box.pack(fill="x")
        self.log_box.insert("0.0", "--- INICIALIZANDO INTERFAZ AETHER ---\n")
        
        # Variables para animación
        self.angle = 0.0

    def scan_action(self):
        self.log_msg("Iniciando escaneo heurístico...")
        # Simulamos un evento que VEXA podría escuchar
        self.kernel.event_bus.emit("SECTOR_CHANGED", {"name": "GUI_SCAN", "status": "active"})

    def purge_action(self):
        self.log_msg("!!! INICIANDO PURGA DE PROCESOS HOSTILES !!!")
        to_kill = []
        for name, data in self.kernel.process_manager.processes.items():
            if data.get("type") == "hostile":
                to_kill.append(name)
        
        for name in to_kill:
            self.kernel.process_manager.stop_process(name)
            self.log_msg(f"Entidad {name} eliminada.")

    def log_msg(self, msg):
        self.log_box.insert("end", f"> {msg}\n")
        self.log_box.see("end")

    def update_ui(self):
        # Actualizar datos del Kernel
        status = self.kernel.system_state.get_status()
        
        # Actualizar Etiquetas
        sec = status['active_sector'] if status['active_sector'] else "VIRTUALIZACIÓN STANDBY"
        self.lbl_sector.configure(text=f"SECTOR: {sec}")
        
        load = status['system_load']
        self.lbl_load.configure(text=f"CARGA DEL NÚCLEO: {load}%")
        if load > 80: self.lbl_load.configure(text_color=self.color_danger)
        else: self.lbl_load.configure(text_color="#333")

        # Renderizar Holomapa
        self.draw_holomap()

        # Tick de VEXA para que la simulación avance
        self.kernel.tick()

    def draw_holomap(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx, cy = w/2, h/2
        
        self.angle += 0.02 # Rotación constante
        
        # Dibujar Grid (Efecto suelo 3D "Virtual")
        for i in range(-5, 6):
            offset = i * 40
            # Líneas azul oscuro muy tecnológicas
            self.canvas.create_line(0, cy + offset, w, cy + offset, fill="#002244", width=1)
            self.canvas.create_line(cx + offset*2, 0, cx - offset*2, h, fill="#002244", width=1)

        # Dibujar Procesos como Entidades
        processes = self.kernel.process_manager.processes
        count = len(processes)
        radius = 160
        idx = 0
        
        for name, proc in processes.items():
            # Posicionamiento radial rotatorio
            theta = (2 * math.pi * idx / (count if count > 0 else 1)) + self.angle
            px = cx + radius * math.cos(theta)
            py = cy + radius * math.sin(theta) * 0.5 # Perspectiva achatada
            
            is_hostile = proc.get("type") == "hostile"
            size = 15 + (proc['load'] / 2)
            
            if is_hostile:
                # MONSTRUO: Rombo Rojo con el Ojo
                pts = [px, py-size, px+size, py, px, py+size, px-size, py]
                self.canvas.create_polygon(pts, fill=self.color_danger, outline="white", width=2)
                self.canvas.create_text(px, py-size-10, text=name, fill="#FF5555", font=("Courier", 10, "bold"))
                # Rayo de ataque al núcleo
                self.canvas.create_line(px, py, cx, cy, fill="red", dash=(4,2), width=2)
            else:
                # DATA: Cubo Azul
                self.canvas.create_rectangle(px-size/2, py-size/2, px+size/2, py+size/2, outline=self.color_primary, width=2)
                self.canvas.create_text(px, py+size+10, text=name, fill="#00AAFF", font=("Arial", 9))
            
            idx += 1
            
        # Núcleo Central (Torre)
        self.canvas.create_oval(cx-25, cy-25, cx+25, cy+25, fill="white", outline=self.color_primary, width=4)
        self.canvas.create_text(cx, cy+40, text="CORE", fill="white", font=("Arial", 8))

    def _start_update_loop(self):
        def loop():
            while True:
                time.sleep(1)
                self.after(0, self.update_ui)

        t = threading.Thread(target=loop, daemon=True)
        t.start()

if __name__ == "__main__":
    # Setup Kernel
    state = SystemState()
    pm = ProcessManager(system_state=state)
    auth = AuthModule()
    sector5 = Sector5Kernel(state, pm, auth)

    # Login automático para GUI
    sector5.auth.validate("admin01", "rootaccess")
    sector5.system_state.add_connection("admin01_gui")

    # Arrancar GUI
    app = NedenDashboard(sector5)
    app.mainloop()