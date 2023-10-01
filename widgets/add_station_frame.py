from typing import Union

import customtkinter


class AddStationFrame(customtkinter.CTkToplevel):
    def __init__(self, parent: any, command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.parent = parent
        # self.grid_columnconfigure(0, weight=1)

        # Toplevel widget
        self.title("Add Station")

        # sets the geometry of toplevel
        self.geometry("500x200")
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top

        self._user_input = None

        self.station_form_frame = customtkinter.CTkFrame(self, width=300)
        self.station_form_frame.grid(row=0, column=0, pady=5, sticky="new")

        # create main entry and button
        self.station_name = customtkinter.CTkEntry(self.station_form_frame, width=300, placeholder_text="Name")
        self.station_name.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="new")

        self.station_url = customtkinter.CTkEntry(self.station_form_frame, placeholder_text="URL")
        self.station_url.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="new")

        self.save_btn = customtkinter.CTkButton(self.station_form_frame, text="Save",
                                                command=self._save_input)
        self.save_btn.grid(row=2, column=0, padx=10, pady=5, sticky="new")

        self.cancel_btn = customtkinter.CTkButton(self.station_form_frame, text="Cancel",
                                                  command=self._cancel)
        self.cancel_btn.grid(row=2, column=1, padx=10, pady=5, sticky="new")

        self.wait_window()

    def _save_input(self):
        print('save')
        self._user_input = {"name": self.station_name.get(), "url": self.station_url.get()}
        self.grab_release()
        self.destroy()

    def _cancel(self):
        self.grab_release()
        self.destroy()

    def get_input(self):
        return self._user_input
