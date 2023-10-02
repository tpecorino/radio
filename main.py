import os

import customtkinter
import vlc
from PIL import Image

from data import database
from widgets import StationListFrame, AddStationFrame


class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("300x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.title("Radio")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.session = database.get_database_session()
        self.update_view = True
        self.stations = []
        self.current_station = None

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")

        # Frames
        self.station_info_container = customtkinter.CTkFrame(self)
        self.station_info_container.grid(row=0, column=0, columnspan=3, pady=5)

        self.station_btn_frame = customtkinter.CTkFrame(self.station_info_container)
        self.station_btn_frame.grid(row=1, column=0, columnspan=2, sticky="ns")

        self.station_playing_name = customtkinter.CTkLabel(self.station_info_container, text="", anchor="center",
                                                           )
        self.station_playing_name.grid(row=0, column=0, columnspan=2, padx=10, sticky="ew")

        # Images
        self.play_btn_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "play.png")),
                                                   size=(20, 20))

        self.pause_btn_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "pause.png")),
                                                    size=(20, 20))

        self.stop_btn_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "stop.png")),
                                                   size=(20, 20))

        self.add_btn_img = customtkinter.CTkImage(Image.open(os.path.join(image_path, "add.png")),
                                                  size=(20, 20))

        self.stop_btn = customtkinter.CTkButton(self.station_btn_frame, text="", image=self.stop_btn_img, width=40,
                                                command=self.stop_stream)
        self.stop_btn.grid(row=3, column=0, padx=10, pady=5, sticky="new")

        self.play_btn = customtkinter.CTkButton(self.station_btn_frame, text="", image=self.play_btn_img, width=40,
                                                command=self.play_stream)
        self.play_btn.grid(row=3, column=1, padx=10, pady=5, sticky="new")

        self.add_station_btn = customtkinter.CTkButton(self.station_btn_frame, text="", image=self.add_btn_img,
                                                       width=40,
                                                       command=self.open_station_add_dialog)
        self.add_station_btn.grid(row=3, column=2, padx=10, pady=5, sticky="new")

        # create station list frame
        self.station_list_container_frame = customtkinter.CTkFrame(self)
        self.station_list_container_frame.columnconfigure(0, weight=1)
        self.station_list_container_frame.rowconfigure(1, weight=1)
        self.station_list_container_frame.grid(row=1, column=0, columnspan=2, sticky="news")

        self.station_list_frame = StationListFrame(self.station_list_container_frame, width=300,
                                                   command=self.on_list_station_event,
                                                   corner_radius=0)
        self.station_list_frame.grid(row=1, column=0, pady=0, sticky="ns")

        # define VLC instance
        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

        # Define VLC player
        self.player = self.instance.media_player_new()

    def run(self):
        self.load_stations()
        self.mainloop()

    def on_closing(self, event=0):
        self.destroy()

    def play_stream(self):
        if self.current_station is None:
            return

        name = self.current_station.name
        url = self.current_station.url

        if url:
            # Define VLC media
            media = self.instance.media_new(url)

            # Set player media
            self.player.set_media(media)
            self.play_btn.configure(image=self.pause_btn_img, command=self.pause_stream)

            # Play the media
            print('Play')
            self.player.play()
            self.station_playing_name.configure(text=name, anchor="center")

    def pause_stream(self):
        print('Pause')
        self.player.pause()
        self.play_btn.configure(image=self.play_btn_img, command=self.play_stream)

    def stop_stream(self):
        print('Stop')
        self.player.stop()
        self.play_btn.configure(image=self.play_btn_img, command=self.play_stream)

    def mute(self):
        self.player.audio_toggle_mute()

    def load_stations(self):
        self.stations = database.fetch_stations(self.session)
        print(self.stations)
        for station in self.stations:
            print('load', station)
            self.station_list_frame.add_item(station, station.name, self.play_btn_img)

    def on_list_station_event(self, item):
        self.current_station = item
        self.play_stream()
        print(f"label button frame clicked: {item}")

    def open_station_add_dialog(self):
        dialog = AddStationFrame(self)
        station_to_add = dialog.get_input()
        print(station_to_add)

        if station_to_add is not None:
            if station_to_add['name'] and station_to_add['url']:
                database.save_station(self.session, station_to_add)
                self.station_list_frame.add_item(station_to_add, text=station_to_add['name'])


if __name__ == "__main__":
    app = App()
    app.run()
