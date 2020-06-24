import pytube


def download_video(res):
    res = res + 'p'
    stream = youtube_video.streams.get_by_resolution(res)
    print("-----------------------Начинаю загрузку видео-----------------------")
    print("Оно будет лежать в загрузки. Ждите сообщения о завершении с:")
    stream.download()
    print("-------------------------------Готово-------------------------------")
    exit()

def ask_about_resolution(quality_list):
    res = input('')
    while res not in [x[:-1] for x in quality_list]:
        print('Введите коректое качество (без буквы "р")')
        res = input("Качество: ")
    return res

def get_available_resolutions():
    # Хотите скачать видео со звуком ?
    quality_list = []
    res = iter(['360p','480p', '720p', '1080p'])
    while True:
        try:
            item = next(res)
            quality = youtube_video.streams.get_by_resolution(item)
            if quality:
                quality_list.append(item)
        except StopIteration:
            break
    return quality_list

link = input('Ссылка на видео: ').strip()
youtube_video = pytube.YouTube(link)
print(f"Название видео: {youtube_video.title}")
length = youtube_video.length
print(f"Продолдительность: {int(length)//60}:{int(length)%60}")
print(f"Автор: {youtube_video.author}")

quality_list = get_available_resolutions()

print(f"Доступные разрешения: {' '.join(quality_list)}")
print("В каком скачивать?: ", end='')

res = ask_about_resolution(quality_list)

download_video(res)
