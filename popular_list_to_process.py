from api.tools import Tools as t

y_popular_id_list = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/100_popular_from_2017.json')
y_list = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json')


all_youtube_dict_by_id = {}

for item in y_list:
    y_id = item['src'].split('/')[-1].split('.')[0]
    all_youtube_dict_by_id[y_id]=item


new_list_to_process = []
ok = 0
for y_id_pop in y_popular_id_list:
    if y_id_pop in all_youtube_dict_by_id:
        ok += 1

        new_list_to_process.append(all_youtube_dict_by_id[y_id_pop])
print('{}/{}'.format(ok, len(y_popular_id_list)))
t.save_json('/mnt/data/palpatine/DATASETS/YT_LINK/100_popular_from_2017_to_process.json', new_list_to_process)
