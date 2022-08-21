import pytube
from tkinter import *
from tkinter.ttk import Combobox
from functions import *

video_settings = {
    "url": "",
    "res": ""
}


class App(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.brief_text = Label(parent, text="Insert the video URL and then select a resolution").place(x=20, y=10)
        self.url_input_box = Entry(parent)
        self.url_input_box.place(x=20, y=30, width=400)
        self.input_error_mssg = Label(parent, text="You must insert an URL", bg="red", fg="white")
        self.confirm_url_btn = Button(parent, text="Confirm URL", command=self.get_video_url, justify="center")
        self.confirm_url_btn.place(x=20, y=50)
        self.only_audio_btn = Button(parent, text="Only audio", justify="center", width=11)
        self.combo_res = Combobox(parent, state="readonly", values=[])
        self.select_res = Label(parent, text="Choose one resolution", bg="red", fg="white")
        self.download_button = Button(parent, text="Download", bg="green", fg="white", command=self.get_res)
        self.done_label = Label(parent, text="Done!", bg="green", fg="white", justify="center", width=71, height=10)

    def get_video_url(self):
        url = self.url_input_box.get()
        if len(url) == 0:
            url = ""
            self.input_error_mssg.place(x=100, y=50)
        else:
            video_settings["url"] = url
            self.input_error_mssg.place_forget()
            # self.confirm_url_btn.place_forget()
            self.only_audio_btn.config(command=self.download_audio_only)
            self.only_audio_btn.place(x=20, y=50)
            self.combo_res.config(values=set_available_resolutions(video_settings["url"]))
            self.combo_res.place(x=20, y=75)
            self.download_button.place(x=100, y=50)

    def get_res(self):
        res = self.combo_res.get()
        if len(res) == 0:
            res = ""
            self.select_res.place(x=170, y=75)
        else:
            self.select_res.place_forget()
            video_settings["res"] = res
            download()
            self.done_label.place(x=0, y=150)

    def download_audio_only(self):
        pytube.YouTube(video_settings["url"]).streams.get_audio_only().download()
        export_audio_mp3()
        self.done_label.place(x=0, y=150)


def set_available_resolutions(url):
    res = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
    video = pytube.YouTube(url)
    max_res = video.streams.filter(mime_type="video/mp4", progressive=False).order_by("resolution").last().resolution
    return res[:res.index(max_res) + 1]


def run():
    root = Tk()
    root.title("YouTube downloader 2.0 now with GUI")
    root.config(width=500, height=300)
    app = App(root)
    root.mainloop()


def download_both_files():
    video = pytube.YouTube(video_settings["url"])
    video.streams.get_audio_only().download(filename_prefix="audio")
    try:
        video = video.streams.filter(res=video_settings["res"], mime_type="video/mp4").first()
        video.download(filename_prefix="video")
    except AttributeError as err:
        print("Something went wrong downloading the video:(")
        raise RuntimeError from err


def download():
    download_both_files()
    audio_file = get_audio_file()
    video_file = get_video_file()
    convert_into_one(audio_file, video_file)
    delete_files(audio_file, video_file)


def main():
    run()


if __name__ == "__main__":
    main()
