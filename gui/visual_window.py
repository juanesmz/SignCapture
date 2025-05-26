import cv2
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkImage, CTkOptionMenu
from PIL import Image
import json
import numpy as np

class VisualWindow(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color='#949494')
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.current_frame = 0

        with open('assets/datos.json', 'r', encoding='utf-8') as archivo:
            self.datos = json.load(archivo)

        # Cargar imágenes
        self.logo = CTkImage(light_image=Image.open("assets/images/logo.png"), size=(450*100//130, 100))
        self.logo2 = CTkImage(light_image=Image.open("assets/images/logo2.png"), size=(769*250//317, 250))
        self.return_btn = CTkImage(light_image=Image.open("assets/images/previous.png"), size=(70, 70))
        self.close_btn = CTkImage(light_image=Image.open("assets/images/close.png"), size=(70, 70))
        self.img = Image.fromarray(np.zeros((300, 533, 3), dtype=np.uint8))
        
        self.setup_ui()

        self.frames = [i for i in self.datos[self.signer_box.get()][self.categorie_box.get()][self.sign_box.get()][self.video_box.get()]['rep_0']]
    
    def setup_ui(self):
        #Imagenes
        self.container_img = CTkFrame(self, fg_color='#636363', border_color='#000000', border_width=2)
        self.container_img.grid(row=0, column=0, rowspan=2, sticky='NS', padx=10, pady=10)
        #self.container_img.grid_rowconfigure(0, weight=1)

        CTkLabel(self.container_img, image=self.logo, text='').grid(row=2, column=0, pady=10)
        CTkLabel(self.container_img, image=self.logo2, text='').grid(row=1, column=0, padx=30, pady=100)
        CTkButton(self.container_img, 
                  image=self.return_btn, 
                  command=self.return_menu, 
                  fg_color='transparent',
                  hover_color='#4a4a4a',
                  text='', 
                  width=75,
                  height=75,
                  corner_radius=10).grid(row=0, column=0, padx=10, pady=10, sticky='NW')

        self.container_1 = CTkFrame(self, fg_color='#636363', border_color='#000000', border_width=2)
        self.container_1.grid(row=0, column=1, sticky='EWNS', padx=10, pady=10)
        self.container_1.grid_columnconfigure(0, weight=1)
        self.container_1.grid_rowconfigure(0, weight=1)
        self.container_1.grid_rowconfigure(3, weight=1)

        '''----------------Escoger seña----------------'''
        
        self.container_sel_sign = CTkFrame(self.container_1, fg_color='#DAE3F3', border_color='#172C51', border_width=2)
        self.container_sel_sign.grid(row=0, column=0, sticky='EW', pady=10, padx = 10,)
        self.container_sel_sign.grid_columnconfigure(0, weight=1)
        self.container_sel_sign.grid_columnconfigure(2, weight=1)


        CTkLabel(self.container_sel_sign, 
                 text=self.controller.language_manager.get_text("visual_window", "sel_sign_label"), 
                 font=("Arial", 30), 
                 text_color='#000000').grid(row=0, column=0, pady=10, padx = 10, columnspan = 3, sticky='W')

        self.signer_box = CTkOptionMenu(self.container_sel_sign, 
                                        values = [signer for signer in self.datos], 
                                        command= self.update_options,
                                        font=("Arial", 20))
        
        self.signer_box.grid(row = 1, column = 0, padx=5, pady=10)

        self.categorie_box = CTkOptionMenu(self.container_sel_sign, 
                                           values = [signer for signer in self.datos[self.signer_box.get()]], 
                                           command= self.update_options,
                                           font=("Arial", 20))
        self.categorie_box.grid(row = 1, column = 1, padx=5, pady=10)

        self.sign_box = CTkOptionMenu(self.container_sel_sign, 
                                      values = [signer for signer in self.datos[self.signer_box.get()][self.categorie_box.get()]], 
                                      command= self.update_options,
                                      font=("Arial", 20))
        self.sign_box.grid(row = 1, column = 2, padx=5, pady=10)

        '''-------------Escoger video de la seña-------------'''

        self.container_sel_vid = CTkFrame(self.container_1, fg_color='#DAE3F3', border_color='#172C51', border_width=2)
        self.container_sel_vid.grid(row=1, column=0, sticky='EW', pady=10, padx = 10,)
        self.container_sel_vid.grid_columnconfigure(0, weight=1)
        self.container_sel_vid.grid_columnconfigure(1, weight=1)

        CTkLabel(self.container_sel_vid, 
                 text=self.controller.language_manager.get_text("visual_window", "sel_vid_label"), 
                 font=("Arial", 30), 
                 text_color='#000000').grid(row=0, column=0, pady=10, padx = 10, columnspan=2, sticky='W')

        self.video_box = CTkOptionMenu(self.container_sel_vid, 
                                       values = [signer for signer in self.datos[self.signer_box.get()][self.categorie_box.get()][self.sign_box.get()]], 
                                       command= self.update_options,
                                       font=("Arial", 20))
        self.video_box.grid(row = 1, column = 0, padx=5, pady=10)

        self.rept_box = CTkOptionMenu(self.container_sel_vid, 
                                       values = [signer for signer in self.datos[self.signer_box.get()][self.categorie_box.get()][self.sign_box.get()][self.video_box.get()]], 
                                       command= self.update_options,
                                       font=("Arial", 20))
        self.rept_box.grid(row = 1, column = 1, padx=5, pady=10)

        '''------------Contenedor del video---------------'''

        self.video_frame = CTkLabel(self.container_1, text='', image=CTkImage(light_image=self.img, size=(533, 300)))
        self.video_frame.grid(row = 2, column = 0, padx=5, pady=5)

        self.play_btn = CTkButton(self.container_1, text=self.controller.language_manager.get_text("visual_window", "play_btn"), command=self.play_video, font=("Arial", 25))
        self.play_btn. grid(row = 3, column = 0, padx=5, pady=5)
    
    def update_options(self, _=None):

        self.categorie_box.configure(values = [signer for signer in self.datos[self.signer_box.get()]])
        self.sign_box.configure(values = [signer for signer in self.datos[self.signer_box.get()][self.categorie_box.get()]])
        self.video_box.configure(values=[signer for signer in self.datos[self.signer_box.get()][self.categorie_box.get()][self.sign_box.get()]])
        self.rept_box.configure(values = [signer for signer in self.datos[self.signer_box.get()][self.categorie_box.get()][self.sign_box.get()][self.video_box.get()]])
        self.frames = [i for i in self.datos[self.signer_box.get()][self.categorie_box.get()][self.sign_box.get()][self.video_box.get()]['rep_0']]
            
    def play_video(self):
        if self.current_frame < len(self.frames):
            img = np.zeros((300, 533, 3), dtype=np.uint8)

            for body_part, color in zip(['pose', 'r_hand', 'l_hand'], [(0, 255, 255), (204, 255, 0), (255, 0, 255)]):
                x = [int(i*533) for i in self.datos[self.signer_box.get()][self.categorie_box.get()][self.sign_box.get()][self.video_box.get()][self.rept_box.get()][self.frames[self.current_frame]][body_part]['x']]
                y = [int(i*300) for i in self.datos[self.signer_box.get()][self.categorie_box.get()][self.sign_box.get()][self.video_box.get()][self.rept_box.get()][self.frames[self.current_frame]][body_part]['y']]
                for x_i, y_i in zip(x, y): cv2.circle(img, (x_i, y_i), 2, color,1)
            self.video_frame.configure(image=CTkImage(light_image=Image.fromarray(img), size=(533, 300)))
            self.current_frame += 1
            self.after(40, self.play_video)
        else:
            self.current_frame = 0

    def return_menu(self):
        self.controller.show_menu_window()
