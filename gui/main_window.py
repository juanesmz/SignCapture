# gui/main_window.py
from gui.components.video_review import VideoReviewWindow
import customtkinter as ctk
import cv2
import os
import random
from PIL import Image

class MainWindow(ctk.CTkFrame):
    def __init__(self, parent, controller, video_folder, dest_folder, camera, repeticiones):
        super().__init__(parent)
        self.configure(fg_color='#949494')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.controller = controller
        self.parent = parent
        self.dest_folder = dest_folder
        self.video_play_index = 0
        self.video_list = [sign_class + '/' + file for sign_class in video_folder for file in os.listdir(sign_class)]
        self.videos_random = [elemento for elemento in self.video_list for _ in range(repeticiones)]
        random.shuffle(self.videos_random)
        self.resultado = None
        self.frame_index = 0
        self.frame_count = 0
        self.record = False
        self.logo = ctk.CTkImage(light_image=Image.open("assets/images/logo.png"), size=(450*60//130, 60))
        self.logo2 = ctk.CTkImage(light_image=Image.open("assets/images/logo2.png"), size=(769*150//317, 150))
        self.return_btn = ctk.CTkImage(light_image=Image.open("assets/images/previous.png"), size=(70, 70))

        # Inicializar la cámara
        self.cap = cv2.VideoCapture(camera)
        self.cap2 = cv2.VideoCapture(self.videos_random[self.video_play_index])

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 270)
        
        # Variable para almacenar las propiedades del video
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        Tipo, seña = self.videos_random[self.video_play_index].split('.')[0].split('/')[-2:]
        folder_path = f'{self.dest_folder}/{len(os.listdir(self.dest_folder))}/{Tipo}/{seña}/'
        self.video_path = folder_path + f'{len(os.listdir(folder_path))}.avi'
        # Inicializar el servicio de grabación
        self.recording = False
        self.video_writer = None

        # Configuración de la ventana
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario."""
        self.logo_container = ctk.CTkFrame(self, fg_color='#636363', border_color='#000000', border_width=2)
        self.logo_container.grid(row=0, column=0, columnspan=2, pady=30)

        self.logo_label = ctk.CTkLabel(self.logo_container, text="", image=self.logo)
        self.logo_label.grid(row=0, column=2, padx=10, pady=10, sticky='NE')

        self.logo_label2 = ctk.CTkLabel(self.logo_container, text="", image=self.logo2)
        self.logo_label2.grid(row=0, column=1, padx=10, pady=10) 
        ctk.CTkButton(self.logo_container, 
                  image=self.return_btn, 
                  command=self.go_back, 
                  fg_color='transparent',
                  hover_color='#4a4a4a',
                  text='', 
                  width=75,
                  height=75,
                  corner_radius=10).grid(row=0, column=0, padx=10, pady=10, sticky='NW')

        self.label = ctk.CTkLabel(self, text="")
        self.label.grid(row=1, column=0, padx=10, pady=10)

        self.record_button = ctk.CTkButton(self,
                                           text=self.controller.language_manager.get_text("main_window", "record_btn"), 
                                           command=self.toggle_recording, 
                                           font=('Arial', 25))
        self.record_button.grid(row=2, column=0, padx=40, pady=10)

        # Elemento para el video
        self.label2 = ctk.CTkLabel(self, text="")
        self.label2.grid(row=1, column=1, padx=10, pady=10, sticky='E')

        self.l1 = ctk.CTkLabel(self, 
                               text=f"{self.controller.language_manager.get_text("main_window", "video_label")[0]} 0 {self.controller.language_manager.get_text("main_window", "video_label")[1]} {len(self.videos_random)}: {self.videos_random[0].split('/')[-1].split('.')[0]}", 
                               font=("Arial", 18))
        self.l1.grid(row=2, column=1, padx=5, pady=5)

        # Iniciar la actualización del video
        self.update()

    def update(self):
        """Actualiza el frame de la cámara en la GUI."""
        ret, frame = self.cap.read()
        ret2, frame2 = self.cap2.read()

        if ret:
            if self.record:
                self.video_writer.write(frame)
            if self.frame_count == 1:
            # Mostrar el frame en la GUI a una tasa de 15FPS
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_ctk = ctk.CTkImage(light_image=Image.fromarray(frame), size=(350*16//9, 350))
                self.label.configure(image=img_ctk)
                self.frame_count = 0
            self.frame_count += 1
        
        if ret2:
            self.frame_index+=1
            if self.frame_index<int(self.cap2.get(cv2.CAP_PROP_FRAME_COUNT)) and self.frame_index%4 == 0:
                print(self.frame_index, self.cap2.get(cv2.CAP_PROP_FRAME_COUNT))
                frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
                img = ctk.CTkImage(light_image=Image.fromarray(frame2), size=(350*16//9, 350))
                self.label2.configure(image=img)
            elif self.frame_index == int(self.cap2.get(cv2.CAP_PROP_FRAME_COUNT)):
                self.cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.frame_index = 0
            
            print(self.frame_index)

        if self.resultado:
            self.accept_video()
            self.resultado = None
        elif self.resultado is not None:
            os.remove(self.video_path)
            self.resultado = None
        
        # Llamar a la función de nuevo después de 10 ms
        self.parent.after(1, self.update)
    
    def toggle_recording(self):
        """Alternar entre iniciar y detener la grabación."""
        self.recording = not self.recording

        if self.recording:
            
            self.record_button.configure(text=self.controller.language_manager.get_text("main_window", "stop_btn"))
            Tipo, seña = self.videos_random[self.video_play_index].split('.')[0].split('/')[-2:]
            folder_path = f'{self.dest_folder}/{len(os.listdir(self.dest_folder))}/{Tipo}/{seña}/'
            self.video_path = folder_path + f'{len(os.listdir(folder_path))}.avi'
            self.video_writer = cv2.VideoWriter(self.video_path, cv2.VideoWriter_fourcc(*"XVID"), self.fps, (self.frame_width, self.frame_height))
            self.record = True
        else:
            self.record = False #Detiene la grabación

            if self.video_writer is not None:
                self.video_writer.release()
                self.video_writer = None
            
            self.record_button.configure(text="Grabar")
            self.dialog = VideoReviewWindow(self.parent, self.video_path)
            self.resultado = self.dialog.show()
    def accept_video(self):
        """El usuario aceptó el video, continuar normalmente."""
        self.cap2.release()
        self.video_play_index += 1
        self.cap2 = cv2.VideoCapture(self.videos_random[self.video_play_index])
        self.frame_index = 0
        self.l1.configure(text=f"{self.controller.language_manager.get_text("main_window", "video_label")[0]} {self.video_play_index} {self.controller.language_manager.get_text("main_window", "video_label")[1]} {len(self.videos_random)}: {self.videos_random[self.video_play_index].split('/')[-1].split('.')[0]}", font=("Arial", 18))
        
        print("Video aceptado")

    def go_back(self):
        """Navega de vuelta a la ventana de inicio."""
        self.controller.show_startup_window()

