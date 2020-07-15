from api.tools import Tools as t
import csv

path = '/mnt/data/palpatine/SAMPLES/YT_LINK/Vimeo migration - DONE - data-3_2019-Veronika.csv'

yt_path = '/mnt/data/palpatine/DATASETS/YT_LINK/REF/sources_youtube.json'
ex_path = '/mnt/data/palpatine/DATASETS/YT_LINK/REF/sources_exports.json'
youtube_entire_video_list = '/mnt/data/palpatine/SAMPLES/YT_LINK/youtube_listdir_video.json'
youtube_entire_video_list = t.load_json(youtube_entire_video_list)
file=open( path, "r")
reader = csv.reader(file)
youtube_list = []
exports_list = []
for line in reader:
    export, yt_link=line[3],line[2]
    if len(export.split('/')) == 1:
        continue
    if not len(export) or not len(yt_link):
        continue

    if 'vimeo' in yt_link.lower():
        # print(output)
        continue
    else:
        yt_id = yt_link.rsplit('/')[-1]

    yt_video_path = None
    for video in youtube_entire_video_list:
        if yt_id in video:
            yt_video_path= video


    if yt_video_path is None:
        continue

    # print(line)



    export = '/jabba/' + export
    if export[-1] == ' ':
        export = export[:-1]
    # yt = '/jabba/youtube/videos_youtube/' + yt
    youtube_list.append(yt_video_path)
    exports_list.append(export)

t.save_json(yt_path, youtube_list)
t.save_json(ex_path, exports_list)

