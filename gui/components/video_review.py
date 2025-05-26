import customtkinter as ctk
import cv2
from PIL import Image

class VideoReviewWindow:
    def __init__(self, parent, video_path):
        self.parent = parent
        self.video_path = video_path
        self.result = None

        # Crear ventana de revisión
        self.window = ctk.CTkToplevel(parent, fg_color='#949494')
        self.window.title("Revisión del Video")
        self.window.geometry("500x300")
        self.window.attributes('-topmost', True) 
        self.window.focus_force()
        # Etiqueta para mostrar el video
        self.video_label = ctk.CTkLabel(self.window, text="")
        self.video_label.pack(pady=10)

        # Botones de control
        btn_frame = ctk.CTkFrame(self.window)
        btn_frame.pack(pady=10)

        self.accept_btn = ctk.CTkButton(btn_frame, text="Aceptar", command=self.accept_video)
        self.accept_btn.pack(side="left", padx=10)

        self.retake_btn = ctk.CTkButton(btn_frame, text="Repetir", command=self.retake_video)
        self.retake_btn.pack(side="right", padx=10)

        # Iniciar reproducción del video
        self.cap = cv2.VideoCapture(self.video_path)
        self.update_video()

    def update_video(self):
        """Muestra el video en la interfaz."""
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (427, 240))
            img = ctk.CTkImage(light_image=Image.fromarray(frame), size=(427, 240))
            self.video_label.configure(image=img)
            self.video_label.image = img
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reiniciar video cuando termina
        self.window.after(33, self.update_video)

    def accept_video(self):
        """Cierra la ventana y confirma la grabación."""
        self.result = True
        self.cap.release()
        self.window.destroy()
        

    def retake_video(self):
        """Elimina el video y permite grabar nuevamente."""
        self.result = False
        self.cap.release()
        self.window.destroy()
    def show(self):
        self.window.wait_window()  # Espera hasta que la ventana se cierre
        return self.result  # Devuelve el resultado (True o False)
        