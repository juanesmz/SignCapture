from customtkinter import CTkFrame, CTkImage, CTkLabel, CTkButton, CTkLabel
from PIL import Image
from gui.components.language_button import LanguageButton

class MenuWindow(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color='#949494')
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Cargar imágenes
        self.logo = CTkImage(light_image=Image.open("assets/images/logo.png"), size=(450*100//130, 100))
        self.logo2 = CTkImage(light_image=Image.open("assets/images/logo2.png"), size=(769*250//317, 250))
        self.close_btn = CTkImage(light_image=Image.open("assets/images/close.png"), size=(70, 70))

        self.setup_ui()

    def setup_ui(self):
        
        #Imagenes
        self.container_img = CTkFrame(self, fg_color='#636363', border_color='#000000', border_width=2)
        self.container_img.grid(row=0, column=0, sticky='NS', padx=10, pady=10)
        self.container_img.grid_rowconfigure(0, weight=1)

        CTkLabel(self.container_img, image=self.logo, text='').grid(row=2, column=0, pady=10)
        CTkLabel(self.container_img, image=self.logo2, text='').grid(row=1, column=0, padx=30, pady=100)
        LanguageButton(self.container_img, self.change_language).grid(row=0, column=0, pady=10)
        CTkButton(self.container_img, 
                  image=self.close_btn, 
                  command=self.close_app, 
                  fg_color='transparent',
                  hover_color='#4a4a4a',
                  text='', 
                  width=75,
                  height=75,
                  corner_radius=10).grid(row=0, column=0, padx=10, pady=10, sticky='NW')
        
        self.container_btn = CTkFrame(self, fg_color='#636363', border_color='#000000', border_width=2)
        
        self.container_btn.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)

        self.container_btn.grid_rowconfigure(0, weight=1)
        self.container_btn.grid_rowconfigure(3, weight=1)
        self.container_btn.grid_columnconfigure(0, weight=1)

        self.lbl = CTkLabel(self.container_btn, 
                  text=self.controller.language_manager.get_text("menu_window", "title"), 
                  font=("Arial", 30))
        self.lbl.grid(row=0, column=0, sticky='SW', padx=20, pady=30)

        self.btn_1 = CTkButton(self.container_btn, 
                               height=40,
                               text=self.controller.language_manager.get_text("menu_window", "video"), 
                               font=("Arial", 25), 
                               command=self.go_to_startup)
        self.btn_1.grid(row=1, column=0, sticky='NEW', pady=10, padx=80)

        self.btn_2 = CTkButton(self.container_btn, 
                               height=40,
                               text=self.controller.language_manager.get_text("menu_window", "procesar"), 
                               font=("Arial", 25), 
                               command=self.go_to_post)
        self.btn_2.grid(row=2, column=0, sticky='NEW', pady=10, padx=80)

        self.btn_3 = CTkButton(self.container_btn, 
                               height=40,
                               text=self.controller.language_manager.get_text("menu_window", "visualizar"), 
                               font=("Arial", 25), 
                               command=self.go_to_visual)
        self.btn_3.grid(row=3, column=0, sticky='NEW', pady=10, padx=80)

    def go_to_startup(self):
        self.controller.show_startup_window()

    def go_to_post(self):
        self.controller.show_postprocessing_window()
    
    def go_to_visual(self):
        self.controller.show_visual_window()

    def change_language(self, language):
        self.controller.set_language(language)
    
    def update_texts(self):
        self.lbl.configure(text=self.controller.language_manager.get_text("menu_window", "title"))
        self.btn_1.configure(text=self.controller.language_manager.get_text("menu_window", "video"))
        self.btn_2.configure(text=self.controller.language_manager.get_text("menu_window", "procesar"))
        self.btn_3.configure(text=self.controller.language_manager.get_text("menu_window", "visualizar"))

    def close_app(self):
        self.controller.on_close()