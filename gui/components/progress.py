from customtkinter import CTkToplevel, CTkProgressBar



class ProgrssBar:
    def __init__(self, parent, video_path):
        self.parent = parent
        self.video_path = video_path
        self.result = None

        # Crear ventana de revisión
        self.window = CTkToplevel(parent)
        self.window.title("Progreso del postprocesamiento")
        self.window.geometry("500x300")
        self.window.attributes('-topmost', True) 
        self.window.focus_force()

        # Crear una barra de progreso
        self.progressbar = CTkProgressBar(self.window, orientation="horizontal", mode="determinate")
        self.progressbar.pack(pady=40, padx=20, fill="x")
        self.progressbar.set(0)
        