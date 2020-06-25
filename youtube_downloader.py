import pytube

# https://gist.github.com/sidneys/7095afe4da4ae58694d128b1034e01e2 все itag

def download_video(itag: str, yt_obj) -> None:
    stream = yt_obj.streams.get_by_itag(itag)
    print("-----------------------Начинаю загрузку видео-----------------------")
    print("Оно будет лежать в папке \"загрузки\". Ждите сообщения о завершении с:")
    stream.download()
    print("-------------------------------Готово-------------------------------")
    exit()

def ask_about_resolution(res_dict: dict) -> str:
    res = input('Ключ:')
    while res not in res_dict:
        print('Введите корректный ключ')
        res = input("Ключ: ")
    return res

def print_streams(yt_obj):
    for i in yt_obj.streams:
        print(i)

def get_available_resolutions(yt_obj) -> dict:
    # Хотите скачать видео со звуком ?
    video_only = 'video only'
    mixed = 'audio/video'
    d3 = 'audio/video 3D'
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
        '138': ('2160p60', 'mp4', video_only),
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
    output_res = {}
    while True:
        try:
            item = next(res)
            quality = yt_obj.streams.get_by_itag(item)
            if quality:
                output_res[item] = quality_dict[item]
        except StopIteration:
            break
    return output_res

def try_get_youtube_object_by_link(link: str):
    while True:
        try:
            youtube_video = pytube.YouTube(link)
            break
        except:
            print('Некоректная ссылка, попробуйте другую')
            link = input('Ссылка на видео: ').strip()
    return youtube_video

def print_available_resolutions(res_dict):
    print()
    for key in res_dict:
        data = res_dict[key][2]
        if data == 'video only':
            data = 'только видео (без звука)'
        elif data == 'audio/video 3D':
            data = '3d видео (без звука)'
        else:
            data = 'видео'
        print(f'Ключ: "{key}" \n-----Качество: {res_dict[key][0]} \n-----Формат: {res_dict[key][1]} {data}')
        print()

def print_length(yt_obj):
    length = yt_obj.length
    print()
    print(f"Продолдительность: {int(length)//60}:{int(length)%60}")

def print_title(yt_obj):
    print()
    print(f"Название видео: {youtube_video.title}")

def print_author(yt_obj):
    print()
    print(f"Автор: {youtube_video.author}")

link = input('Ссылка на видео: ').strip()

youtube_video = try_get_youtube_object_by_link(link)
print_title(youtube_video)
print_length(youtube_video)
print_author(youtube_video)
#
res_dict = get_available_resolutions(youtube_video)
# https://www.youtube.com/watch?v=Bey4XXJAqS8
print_available_resolutions(res_dict)
#
#
res = ask_about_resolution(res_dict)
#
download_video(res, youtube_video)
