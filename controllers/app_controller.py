# controllers/app_controller.py
import customtkinter as ctk
from gui.startup_window import StartupWindow
from gui.main_window import MainWindow
from gui.menu_window import MenuWindow
from gui.postprocessing_window import PostprocessingWindow
from gui.visual_window import VisualWindow
from utils.language_manager import LanguageManager
from tkinter import messagebox 
from PIL import Image

class AppController:
    def __init__(self):
        self.root = ctk.CTk()
        
        # Configuración de pantalla completa
        self.root.state('zoomed')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.current_window = None
        self.loading_window = None
        self.language_manager = LanguageManager()       

        self.loading_image = ctk.CTkImage(light_image=Image.open("assets/images/loading.png"), size=(200, 200))

    def show_loading(self):
        """Muestra una ventana de carga simplificada"""
        if self.loading_window:
            try:
                self.loading_window.destroy()
            except:
                pass
            
        self.loading_window = ctk.CTkFrame(self.root, fg_color="gray20", corner_radius=0)
        self.loading_window.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.loading_window.lift()
        
        # Contenido de carga centrado
        content_frame = ctk.CTkFrame(self.loading_window, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(content_frame, image=self.loading_image, text="").pack(pady=10)
        ctk.CTkLabel(content_frame, 
                    text=self.language_manager.get_text("loading_screen", "title"),
                    font=("Arial", 16)).pack(pady=10)
        
        self.root.update()

    def hide_loading(self):
        """Oculta la ventana de carga de manera segura"""
        if self.loading_window:
            try:
                self.loading_window.destroy()
            except:
                pass
            self.loading_window = None
            self.root.update()

    def _safe_window_change(self, window_class, *args, **kwargs):
        """Cambia de ventana de manera segura con pantalla de carga"""
        self.show_loading()
        self.root.update()
        
        # Destruir ventana actual si existe
        if self.current_window:
            self.current_window.destroy()

        # Crear nueva ventana
        self.current_window = window_class(self.root, self, *args, **kwargs)
        self.current_window.grid(row=0, column=0, sticky='nsew')
        
        '''if hasattr(self.current_window, 'update_texts'):
            self.current_window.update_texts()'''

        self.hide_loading()

    def show_menu_window(self):
        """Muestra la ventana de menú"""
        self._safe_window_change(MenuWindow)

    def show_startup_window(self):
        """Muestra la ventana de inicio"""
        self._safe_window_change(StartupWindow)

    def show_main_window(self, video_folder, dest_folder, camera, repeticiones):
        """Muestra la ventana principal"""
        self._safe_window_change(MainWindow, video_folder, dest_folder, camera, repeticiones)

    def show_postprocessing_window(self):
        """Muestra la ventana de postprocesamiento"""
        self._safe_window_change(PostprocessingWindow)

    def show_visual_window(self):
        """Muestra la ventana visual"""
        self._safe_window_change(VisualWindow)

    def set_language(self, language):
        """Cambia el idioma"""
        self.language_manager.set_language(language)
        if self.current_window and hasattr(self.current_window, 'update_texts'):
            self.current_window.update_texts()

    def run(self):
        """Inicia la aplicación"""
        self.show_menu_window()
        self.root.mainloop()
    
    def on_close(self):
        """Maneja el cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Seguro que quieres salir?"):
            self.root.destroy()