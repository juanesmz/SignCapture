from customtkinter import CTkFrame, CTkImage, CTkButton
from PIL import Image

class LanguageButton(CTkFrame):
    def __init__(self,parent, language_function):
        super().__init__(parent)
        self.configure(fg_color='#949494')
        self.language_function = language_function

        # Cargar imágenes
        self.spain_flag = CTkImage(light_image=Image.open("assets/images/es.png"), size=(30, 20))
        self.usa_flag = CTkImage(light_image=Image.open("assets/images/en.png"), size=(30, 20))

        self.setup_ui()
    
    def setup_ui(self):

        CTkButton(self, 
                  image=self.usa_flag, 
                  text="", 
                  width=30, 
                  height=20, 
                  command=lambda: self.language_function("en")).grid(row=0, column=0, padx=10, pady=10)

        CTkButton(self, 
                  image=self.spain_flag, 
                  text="", 
                  width=30, 
                  height=20, 
                  command=lambda: self.language_function("es")).grid(row=0, column=1, padx=10, pady=10)