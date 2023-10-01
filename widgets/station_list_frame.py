import customtkinter


class StationListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, parent, command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, text=None):
        label = customtkinter.CTkLabel(self, text=text, compound="left", padx=5, anchor="w")
        button = customtkinter.CTkButton(self, text="Play", width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(10, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(10, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return
