# gui/startup_window.py
import customtkinter as ctk
from tkinter import filedialog, messagebox, BooleanVar
from PIL import Image
import threading
from gui.components.spinbox import Spinbox
import cv2
import os
import shutil

class StartupWindow(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color='#949494')
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)  # Expande la columna 0
        for i in range(4):  # Expande las filas 0 a 3
            self.grid_rowconfigure(i, weight=1)

        self.logo = ctk.CTkImage(light_image=Image.open("assets/images/logo.png"), size=(450*100//130, 100))
        self.logo2 = ctk.CTkImage(light_image=Image.open("assets/images/logo2.png"), size=(769*250//317, 250))
        self.search_icon = ctk.CTkImage(light_image=Image.open("assets/images/search.png"), size=(30, 30))
        self.return_btn = ctk.CTkImage(light_image=Image.open("assets/images/previous.png"), size=(70, 70))

        # Configuración de la ventana
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario."""
        #Imagenes
        self.container_img = ctk.CTkFrame(self, fg_color='#636363', border_color='#000000', border_width=2)
        self.container_img.grid(row=0, column=0, rowspan=4, sticky='NSEW', padx=30, pady=20)
        self.container_img.grid_rowconfigure(0, weight=1)
        
        ctk.CTkLabel(self.container_img, image=self.logo, text='').grid(row=1, column=0, pady=10)
        ctk.CTkLabel(self.container_img, image=self.logo2, text='').grid(row=0, column=0, padx=30, pady=100)
        ctk.CTkButton(self.container_img, 
                  image=self.return_btn, 
                  command=self.return_menu, 
                  fg_color='transparent',
                  hover_color='#4a4a4a',
                  text='', 
                  width=75,
                  height=75,
                  corner_radius=10).grid(row=0, column=0, padx=10, pady=10, sticky='NW')


        # Contenedores
        self.container_1 = ctk.CTkFrame(self, fg_color='#DAE3F3', border_color='#172C51', border_width=2)
        self.container_1.grid(row=0, column=1, sticky='EW', padx=30, pady=20)
        self.container_1.grid_columnconfigure(0, weight=1)

        self.container_2 = ctk.CTkFrame(self, fg_color='#DAE3F3', border_color='#172C51', border_width=2)
        self.container_2.grid(row=1, column=1, sticky='EW', padx=30, pady=20)

        self.container_3 = ctk.CTkFrame(self, fg_color='#DAE3F3', border_color='#172C51', border_width=2) # gris claro    
        self.container_3.grid(row=2, column=1, sticky='EW', padx=30, pady=20)
        
        # Contenedor 1
        self.title_label = ctk.CTkLabel(self.container_1, 
                                        text=self.controller.language_manager.get_text("startup_window", "title_c1"),
                                        font=("Arial", 30), 
                                        text_color='#000000')
        self.title_label.grid(row=0, column=0, sticky='W', padx=10, pady=10)
        self.camera_var = ctk.StringVar()
        self.camera_dropdown = ctk.CTkComboBox(self.container_1, 
                                               variable=self.camera_var, 
                                               state="readonly", 
                                               font=("Arial", 25),
                                               fg_color='#dcd9d8',
                                               text_color='#000000')
        self.camera_dropdown.grid(row=1, column=0, sticky='EW', pady=10, padx=10)
        self.load_cameras()

        # Contenedor 2
        self.title_label2_1 = ctk.CTkLabel(self.container_2,
                                         text=self.controller.language_manager.get_text("startup_window", "title_c2_1"), 
                                         font=("Arial", 30), 
                                         wraplength=550, 
                                         text_color='#000000')
        self.title_label2_1.grid(row=0, column=0, columnspan=3, sticky='W', padx=10, pady=10)

        self.list_class = os.listdir('assets/videos')
        self.checkbox_value = [BooleanVar(value=True) for _ in range(len(self.list_class))]
        self.check_buttons = [ctk.CTkCheckBox(self.container_2, text=text, variable=self.checkbox_value[i], font=("Arial", 25), text_color='#000000') for i, text in enumerate(self.list_class)]
        
        for i in range(1 + len(self.list_class) // 2):
            for j in range(2):
                if i * 2 + j <= len(self.list_class) - 1:
                    self.check_buttons[i * 2 + j].grid(row=i + 1, column=j, sticky='W', padx=10, pady=5)
        
        self.title_label2_2 = ctk.CTkLabel(self.container_2, 
                                         text=self.controller.language_manager.get_text("startup_window", "title_c2_2"), 
                                         font=("Arial", 30), 
                                         wraplength=550, 
                                         text_color='#000000')
        self.title_label2_2.grid(row=i+2, column=0, columnspan=2, sticky='W', padx=10, pady=10)
        self.spinbox = Spinbox(self.container_2, from_=1, to=10, default_value=3)
        self.spinbox.grid(column = 2, row=i+2, padx=5)

        # Contenedor 3
        self.title_label3 = ctk.CTkLabel(self.container_3, 
                                         text=self.controller.language_manager.get_text("startup_window", "title_c3"), 
                                         font=("Arial", 30), 
                                         text_color='#000000')
        self.title_label3.grid(row=0, column=0, columnspan=2, padx= 10, pady=10)
        self.dest_folder_var = ctk.StringVar(value='C:/Users/Lenovo-PC/Videos/DataSet')
        self.l1 = ctk.CTkLabel(self.container_3, 
                               text=self.dest_folder_var.get(), 
                               font=("Arial", 25), 
                               wraplength=350, 
                               fg_color='#dcd9d8',
                               corner_radius=6, 
                               text_color='#000000')
        self.l1.grid(row=1, column=0, padx= 5, pady=10)
        self.btn_search = ctk.CTkButton(self.container_3, 
                                        text=self.controller.language_manager.get_text("startup_window", "search_button"), 
                                        command=self.select_destination, 
                                        font=("Arial", 25), 
                                        text_color='#b6d5ea',
                                        image=self.search_icon)
        self.btn_search.grid(row=1, column=1, padx=10, pady=10, stick='NS')

        # Botón para continuar a la ventana principal
        self.continue_button = ctk.CTkButton(self, 
                                             text=self.controller.language_manager.get_text("startup_window", "continue_button"), 
                                             command=self.continue_to_main,
                                             font=("Arial", 25), 
                                             text_color='#b6d5ea')
        self.continue_button.grid(row=3, column=1, pady=15)

    def continue_to_main(self):
        self.create_experiment()
        mascara = [self.checkbox_value[i].get() for i in range(len(self.checkbox_value))]
        self.resultado = ["assets/videos/" + elemento for elemento, incluir in zip(self.list_class, mascara) if incluir]
        
        self.controller.show_main_window(self.resultado, self.dest_folder_var.get(), int(self.camera_var.get()[-1]), self.spinbox.get())
    
    def load_cameras(self):

        dispositivos = []
        i = 0

        while True:
            event = threading.Event()
            thread = threading.Thread(target=self.open_camera, args=(event, i))
            thread.start()
            event.wait(1)  # Espera hasta 1 segundo

            if event.is_set():
                break
            else:
                dispositivos.append(f'{self.controller.language_manager.get_text("startup_window", "dropdown_cam")} {i}')

            i += 1
        
        self.camera_dropdown.configure(values=dispositivos)
        #self.camera_dropdown.set(dispositivos[0])
    
    def open_camera(self, event, cap_index):
        """Intenta abrir una cámara y notifica si tuvo éxito"""
        cap = cv2.VideoCapture(cap_index)
        event.set()
    
    def select_destination(self):
        folder = filedialog.askdirectory(initialdir='C:/Users/Lenovo-PC/Vídeos/DataSet')
        if folder and not folder.startswith(os.getcwd()):
            self.dest_folder_var.set(folder)
            self.l1.configure(text=self.dest_folder_var.get())
        else:
            messagebox.showerror("Error", "La carpeta de destino no puede estar dentro del directorio del proyecto.")
    
    def create_experiment(self):
        dir_videos = 'assets/videos'
        per_dir = len(os.listdir(self.dest_folder_var.get()))
        os.mkdir(self.dest_folder_var.get() + f'/{str(per_dir + 1)}')
        
        for type_sgn in os.listdir(dir_videos):
            os.mkdir(self.dest_folder_var.get() + f'/{str(per_dir + 1)}/{type_sgn}')
            for class_sgn in os.listdir(f'{dir_videos}/{type_sgn}'):
                os.mkdir(self.dest_folder_var.get() + f'/{str(per_dir + 1)}/{type_sgn}/{class_sgn.split(".")[0]}')

    def return_menu(self):
        self.controller.show_menu_window()