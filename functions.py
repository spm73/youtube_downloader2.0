from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import os


def get_audio_file():
    audio_file = list(filter(lambda file: file[:5] == 'audio', os.listdir(os.getcwd())))
    return str(audio_file[0])


def get_video_file():
    video_file = list(filter(lambda file: file[:5] == 'video', os.listdir(os.getcwd())))
    return str(video_file[0])


def convert_into_one(audio_file, video_file):
    audio = AudioFileClip(audio_file)
    video = VideoFileClip(video_file)
    final_clip = video.set_audio(audio)
    name = video_file[5:]
    final_clip.write_videofile(name)


def delete_files(audio_file, video_file):
    os.remove(audio_file)
    os.remove(video_file)


def export_audio_mp3():
    file_name = list(filter(lambda file: file[-4:] == '.mp4', os.listdir(os.getcwd())))
    AudioFileClip(file_name[0]).write_audiofile(str(file_name[0]) + ".mp3")
    os.remove(file_name[0])


def main():
    pass


if __name__ == '__main__':
    main()
