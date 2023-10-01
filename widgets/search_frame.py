import customtkinter


class SearchFrame(customtkinter.CTkFrame):
    def __init__(self, parent: any, command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command

        self.entry = customtkinter.CTkEntry(self,
                                            placeholder_text="Search Term")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.command)

        self.button = customtkinter.CTkButton(self,
                                              text="Search",
                                              width=90,
                                              command=self.command)
        self.button.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)
