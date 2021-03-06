from api.tools import Tools as t
from api.tools import Match
import numpy as np
import cv2
import os
import time
import collections
# path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_100_offsets.pickle'
path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_popular_from2017.pickle'

workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'

# idy, idb = 'youtube/dpe-IrmhfPY','export/Kriticke_mysleni/EXPORT/05'
# idy, idb = 'youtube/PPEgY50n4Yc','export/ZeroWaste/EXPORT/6'
#


def show_pair (ida, idb):
    a_path = os.path.join(workdir, ida, 'image.png')

    b_path = os.path.join(workdir, idb, 'image.png')
    A = cv2.imread(a_path)
    B = cv2.imread(b_path)
    C = np.array(np.abs(np.array(A, dtype=np.int16) - np.array(B, dtype=np.int16)), dtype=np.uint8)

    res = (640,360)
    A = cv2.resize(A, res)
    B = cv2.resize(B, res)
    C = cv2.resize(C, res)

    cv2.imshow('youtube', A)
    cv2.imshow('exports', B)
    cv2.imshow('diff',C)
    cv2.waitKey(0)
    time.sleep(0.2)

matches = t.load_pickle(path)
ok  = 0
nomse = 0
multiple_mse = 0
deleted = 0
to_delete = []

# youtube_to_process_with_year = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process_100.json')
dct_yt_list = {}
# for item in youtube_to_process_with_year:
#     dct_yt_list[item['dst']] = item



years = {}
for idx, (ida, match) in enumerate(matches.items()):
    ida_info_path = os.path.join(workdir, ida, 'info.json')
    if not os.path.isfile(ida_info_path):
        print('cannot find', ida_info_path)
        continue
    ida_info = t.load_json(ida_info_path)

    # offset_found = False
    for idb, match_item in match.idb_items.items():
        # idb_info_path = os.path.join(workdir, idb, 'info.json')
        # idb_info = t.load_json(idb_info_path)

        if match_item.offset is None:
            to_delete.append((ida, idb))
        else:
            # print()
            # print([ida, idb])
            # offset_found = True
            ok +=1
    # if not offset_found:

        # print('https://slideslive.com/{} https://www.youtube.com/watch?v={}'.format(dct_yt_list[ida]['id'], ida.split('/')[-1]))
        # print('https://www.youtube.com/watch?v={}'.format(ida.split('/')[-1]))
    # year = dct_yt_list[ida]['year']
    # if year not in years:
    #     years[year] = 0
    # years[year] += 1
# years = collections.OrderedDict(sorted(years.items()))
# print(years)

for ida, idb in to_delete:
    del matches[ida].idb_items[idb]
    deleted +=1




    # try:
    #     true_mse = []
    #     for mse in match.mse:
    #         if 10< mse[1] <15:
    #             # idb_info_path =os.path.join(workdir, mse[0], 'info.json')
    #             # idb_info = t.load_json(idb_info_path)


    #             true_mse.append(mse)
    #         if len(match.mse) > 1:
    #             for mse in match.mse:
    #                 show_pair(ida, mse[0])

    #     if len(true_mse) == 1:
    #         ok +=1
    #         # if ok%500 == 0:
    #         #     show_pair(ida, true_mse[0][0])

    #     elif len(true_mse) > 1:
    #         multiple_mse +=1


    # except:
    #     nomse+=1
print('{}/{}'.format(ok, len(matches)))
# t.save_pickle(path_out, matches)
print(deleted)
