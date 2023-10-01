import os

import customtkinter
import vlc
from PIL import Image

from data import database
from widgets import StationListFrame


class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("500x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.session = database.get_database_session()
        self.update_view = True
        self.stations = []

        # Frames
        self.station_form_frame = customtkinter.CTkFrame(self)
        self.station_form_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="new")

        self.station_list_container_frame = customtkinter.CTkFrame(self)
        self.station_list_container_frame.columnconfigure(0, weight=1)
        self.station_list_container_frame.rowconfigure(1, weight=1)
        self.station_list_container_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="news")

        # create main entry and button
        self.station_name = customtkinter.CTkEntry(self.station_form_frame, placeholder_text="Name")
        self.station_name.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="new")

        self.station_url = customtkinter.CTkEntry(self.station_form_frame, placeholder_text="URL")
        self.station_url.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="new")

        self.play_btn = customtkinter.CTkButton(self.station_form_frame, text="Play",
                                                command=self.play_stream)
        self.play_btn.grid(row=3, column=0, padx=10, pady=5, sticky="new")

        self.pause_btn = customtkinter.CTkButton(self.station_form_frame, text="Pause",
                                                 command=self.pause_stream)
        self.pause_btn.grid(row=3, column=1, padx=10, pady=5, sticky="new")

        self.stop_btn = customtkinter.CTkButton(self.station_form_frame, text="Stop",
                                                command=self.stop_stream)
        self.stop_btn.grid(row=3, column=2, padx=10, pady=5, sticky="new")

        # create scrollable label and button frame
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.station_list_frame = StationListFrame(self.station_list_container_frame, width=300,
                                                   command=self.label_button_frame_event,
                                                   corner_radius=0)
        self.station_list_frame.grid(row=1, column=0, pady=0, sticky="news")

        # define VLC instance
        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

        # Define VLC player
        self.player = self.instance.media_player_new()

        # self.button_list = ButtonListFrame(self.graph_list_frame, gen_command=self.play_stream)
        # self.button_list.grid(row=1, column=0, pady=0, sticky="new")

    def run(self):
        self.load_stations()
        self.mainloop()

    def on_closing(self, event=0):
        self.destroy()

    def play_stream(self, station=None):
        if station is None:
            name = self.station_name.get()
            url = self.station_url.get()
        else:
            url = station.url
        # Define VLC media
        media = self.instance.media_new(url)

        # Set player media
        self.player.set_media(media)

        # station = {
        #     "name": name,
        #     "url": url,
        # }
        #
        # database.save_station(self.session, station)

        # Play the media
        print('Play')
        self.player.play()

    def pause_stream(self):
        print('Pause')
        self.player.pause()

    def stop_stream(self):
        print('Stop')
        self.player.stop()

    def load_stations(self):
        self.stations = database.fetch_stations(self.session)
        print(self.stations)
        for station in self.stations:
            print('load', station)
            self.station_list_frame.add_item(station, text=station.name)

    def label_button_frame_event(self, item):
        self.play_stream(item)
        print(f"label button frame clicked: {item}")


if __name__ == "__main__":
    app = App()
    app.run()
