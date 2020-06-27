import pytube
import pathlib
from collections import OrderedDict

class YouTubeDownloader:
    audio_bitrate = OrderedDict()
    res_dict = OrderedDict()
    choose_bitrate = 3
    yt_obj = None
    res_itag = None
    bitrate_itag = None

    def __init__(self, link):
        self.try_get_youtube_object_by_link(link)

    def download_video(self) -> None:
        massage_start = """
        -----------------------Start downloading-----------------------
        After completing the video will be placed in "Downloads" directory
        Wait for completing massage c:
        """
        massage_start_done = """

        -------------------------------Done-------------------------------
        """
        path = pathlib.Path.home() / 'downloads'
        stream = self.yt_obj.streams.get_by_itag(int(self.res_itag))
        print(massage_start)
        stream.download(output_path=path)
        if self.bitrate_itag:
            stream_audio = self.yt_obj.streams.get_by_itag(self.bitrate_itag)
            stream_audio.download(output_path=path,
                                  filename=(stream_audio.title + 'audio'))
        print(massage_start_done)
        exit()

    def ask_about_resolution(self) -> str:
        itag = input('Key:')
        while itag not in self.res_dict:
            print('Enter a proper key: ')
            itag = input("Key: ")
        self.res_itag = itag


    def ask_about_bitrate(self) -> str:
        if self.choose_bitrate == 1:
            itag = input('Key:')
            while itag not in self.audio_bitrate:
                print('Enter a proper key: ')
                itag = input("Key: ")
            self.bitrate_itag = itag
        elif self.choose_bitrate == 2:
            self.bitrate_itag = None
        else:
            self.bitrate_itag = next(iter(self.audio_bitrate))

    def print_streams(self):
        for i in self.yt_obj.streams:
            print(i)

    def get_available_resolutions(self) -> dict:
        video_only = 'video only'
        mixed = 'audio/video'
        d3 = 'audio/video 3D'
        audio = 'audio'
        quality_dict = {
            '22': ('720p', 'mp4', mixed),
            '37': ('1080p', 'mp4', mixed),
            '38': ('3072p', 'mp4', mixed),
            '44': ('480p', 'webm', mixed),
            '45': ('720p', 'webm', mixed),
            '46': ('1080p', 'webm', mixed),
            '83': ('480p', 'mp4', d3),
            '84': ('720p', 'mp4', d3),
            '85': ('1080p', 'mp4', d3),
            '101': ('480p', 'webm', d3),
            '102': ('720p', 'webm', d3),
            '135': ('480p', 'mp4', video_only),
            '136': ('720p', 'mp4', video_only),
            '137': ('1080p', 'mp4', video_only),
            '139': ('48k', 'm4a', audio),
            '140': ('128k', 'm4a', audio),
            '141': ('256k', 'm4a', audio),
            '171': ('128k', 'webm', audio),
            '249': ('50k', 'webm', audio),
            '250': ('70k', 'webm', audio),
            '251': ('160k', 'webm', audio),
            '264': ('1440p', 'mp4', video_only),
            '266': ('2160p60', 'mp4', video_only),
            '298': ('720p60', 'mp4', video_only),
            '299': ('1080p60', 'mp4', video_only),
            '244': ('480p', 'webm', video_only),
            '247': ('720p', 'webm', video_only),
            '248': ('1080p', 'webm', video_only),
            '271': ('1440p', 'webm', video_only),
            '313': ('2160p', 'webm', video_only),
            '333': ('480p60', 'webm', video_only),
            '334': ('720p60', 'webm', video_only),
            '335': ('1080p60', 'webm', video_only),
            '336': ('1440p60', 'webm', video_only),
            '337': ('2160p60', 'webm', video_only),
        }
        res = iter(quality_dict.keys())
        while True:
            try:
                item = next(res)
                quality = self.yt_obj.streams.get_by_itag(item)
                if quality:
                    self.res_dict[item] = quality_dict[item]
            except StopIteration:
                break

    def try_get_youtube_object_by_link(self, link: str):
        while True:
            try:
                self.yt_obj = pytube.YouTube(link)
                break
            except:
                print('Incorrect link, try another one')
                link = input('Youtube video link: ').strip()

    def print_available_resolutions(self) -> None:
        print()
        for key in self.res_dict:
            if 'k' in self.res_dict[key][0]:
                self.audio_bitrate[key] = self.res_dict[key]
                continue
            data = self.res_dict[key][2]

            print(f'Key: "{key}" \n-----Quality: {self.res_dict[key][0]} \n-----Format: {self.res_dict[key][1]} {data}')
            print()


    def print_audio_bitrate(self):
        if int(self.res_itag) < 132:
            self.choose_bitrate = 2
            return
        print()
        print('''
        You chose the video without a sound track, it will be loaded
        automaticaly but you can choose it yourself
        ''')
        x = input('Choose ? (y/n): ')
        print()
        if x.lower() == 'y':
            self.choose_bitrate = 1
            for key in self.audio_bitrate:
                print(f'Key: "{key}" \n-----Bitrate: {self.audio_bitrate[key][0]} \n-----Format: {self.audio_bitrate[key][1]} audio')
                print()

    def print_length(self):
        length = self.yt_obj.length
        print()
        print(f"Video length: {int(length)//60}:{int(length)%60}")

    def print_title(self):
        print()
        print(f"Video name: {self.yt_obj.streams.get_by_itag(self.res_itag).title}")

    def print_author(self):
        print()
        print(f"Author: {self.yt_obj.author}")


link = input('Youtube video link: ').strip()
youtube_download = YouTubeDownloader(link)

youtube_download.get_available_resolutions()

youtube_download.print_available_resolutions()
youtube_download.ask_about_resolution()

youtube_download.print_title()
youtube_download.print_length()
youtube_download.print_author()

youtube_download.print_audio_bitrate()
youtube_download.ask_about_bitrate()

youtube_download.download_video()
