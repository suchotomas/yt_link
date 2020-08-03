import os, time
from api.tools import Tools as t
from file_to_mfcc import FileToMFCC
from file_to_video_vector import FileToVideoVector
from api.offset_calc import OffsetCalc
from tqdm import tqdm
# from match_by_duration import MatchByDuration
import random
import shutil

MIN_CORR_SCORE = 0
a_filename = 'distances.npy'
v_filename = 'video_vector.npy'

OVERWRITE_A = False
OVERWRITE_V = False

y = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json')
e = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json')
workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'

part_num = 5
print('part_num', part_num)
whole_list = y + e

# random.shuffle(whole_list)
step = len(whole_list) // 6
parts = []

for idx in range(6):
    from_to = [idx*step, (idx+1)*step-1]
    if idx == 5:
        from_to[-1] = len(whole_list)
    parts.append(from_to)

process_list = whole_list[parts[part_num][0]: parts[part_num][1]]
file2mfcc = FileToMFCC(workdir)
done = 0
for idx in tqdm(range(len(process_list)), ascii=True, desc='process {} lines'.format(len(process_list))):
    try:
        id_key = process_list[idx]['dst']

        info = t.load_json(os.path.join(workdir, id_key, 'info.json'))
        src = t.get_src_path(info['src'])

        # if os.path.isfile(src):
        #     print('OK', src)
        # else:
        #     print('ERR', src)
        tmp_src = os.path.join(workdir, id_key, os.path.basename(src))
        if idx % 100 == 0:
            print('{} -> {}'.format(src, tmp_src))
        # shutil.copyfile(src, tmp_src)
        a_path = os.path.join(workdir, id_key, 'distances.npy')
        if os.path.isfile(a_path):
            done += 1
            continue

        # a_path = file2mfcc.run(tmp_src, os.path.join(workdir, id_key, 'distances.npy'))
        # if os.path.isfile(tmp_src):
        #     if 'jabba' not in tmp_src:
        #         # pass
        #         os.remove(tmp_src)
        #     else:
        #         raise('ERROR - jabba in src_tmp')
        # if a_path is not None:
        #     done+=1
    except Exception as e:
        print(e)
print('done {}/{}'.format(done, len(process_list)))


