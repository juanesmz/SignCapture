import tkinter as tk
from customtkinter import CTkFrame, CTkEntry, CTkButton

class Spinbox(CTkFrame):
    def __init__(self, parent, from_=0, to=100, default_value=0, **kwargs):
        super().__init__(parent, **kwargs)

        # Variables
        self.from_ = from_
        self.to = to
        self.value = tk.IntVar(value=default_value)
        self.configure(fg_color='#DAE3F3', border_color='#172C51')

        # Entrada para mostrar el valor
        self.entry = CTkEntry(self, textvariable=self.value, width=50, justify="center", font=("Arial", 25), fg_color='#dcd9d8',corner_radius=6, text_color='#000000')
        self.entry.grid(row=0, column=1, padx=5, pady=5)

        # Botón para aumentar el valor
        self.increase_button = CTkButton(self, text="▲", width=20, font=("Arial", 25), command=self.increase)
        self.increase_button.grid(row=0, column=2, padx=(0, 5), pady=5)

        # Botón para reducir el valor
        self.decrease_button = CTkButton(self, text="▼", width=20, font=("Arial", 25), command=self.decrease)
        self.decrease_button.grid(row=0, column=0, padx=(5, 0), pady=5)

    def increase(self):
        """Aumenta el valor en 1, sin exceder el límite superior."""
        current_value = self.value.get()
        if current_value < self.to:
            self.value.set(current_value + 1)

    def decrease(self):
        """Reduce el valor en 1, sin exceder el límite inferior."""
        current_value = self.value.get()
        if current_value > self.from_:
            self.value.set(current_value - 1)

    def get(self):
        """Devuelve el valor actual."""
        return self.value.get()