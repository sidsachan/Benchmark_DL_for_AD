import pytube
import os
import json


def downloadVideo(url, rel_path, vid):
    youtube = pytube.YouTube(url)
    video = youtube.streams.get_highest_resolution()
    title = str(video.title)
    save_path = str(os.path.join(rel_path, 'v_' + vid + '.mp4'))
    print(save_path)
    if (os.path.exists(save_path)):
        print(title, ' is already there!!!')
    else:
        print('Downloading', video.title)
        video.download(rel_path, filename='v_' + vid + '.mp4')


def downloadVidYT(name_file, rel_path):
    # return if the video files already present
    if os.path.isdir(rel_path):
        print("Original Video directory already here!!!")
        return
    f = open(name_file, )
    names = json.load(f)
    video_key = names['video_ids']
    for vid in video_key:
        url = 'https://www.youtube.com/watch?v=' + vid
        downloadVideo(url, rel_path, vid)
