from api.tools import Tools as t

#########
path = '100_id_list.txt'
yt_to_process = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json')
yt_to_process_100 = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process_100.json'

file1 = open(path, 'r')
lines = file1.read().splitlines()
id_list = []
unknown = 0

dct_yt_list = {}
for item in yt_to_process:
    dct_yt_list[item['dst']] = item

y100 = []
for line in lines:
    key = 'youtube/'+ line.split(',')[-1]
    if key not in dct_yt_list:
        unknown +=1
    else:
        dct_yt_list[key]['year']=line.split(',')[-2]
        dct_yt_list[key]['id']=line.split(',')[0]
        y100.append(dct_yt_list[key])
print('unknown', unknown)
print('new', len(y100))
t.save_json(yt_to_process_100, y100)