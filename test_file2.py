from api.tools import Tools as t
from api.tools import Match
import numpy as np
import cv2
import os
import time
path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_100.pickle'
workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'

matches = t.load_pickle(path)

def show_pair (ida, idb):
    a_path = os.path.join(workdir, ida, 'image.png')

    b_path = os.path.join(workdir, idb, 'image.png')
    A = cv2.imread(a_path)
    B = cv2.imread(b_path)
    C =np.array(np.abs(np.array(A, dtype=np.int16) - np.array(B, dtype=np.int16)), dtype=np.uint8)

    res = (640,360)
    A = cv2.resize(A, res)
    B = cv2.resize(B, res)
    C = cv2.resize(C, res)

    cv2.imshow('youtube',A)
    cv2.imshow('exports',B)
    cv2.imshow('diff',C)
    cv2.waitKey(1)
    time.sleep(0.2)


ok  = 0
nomse = 0
multiple_mse = 0
for idx, (ida, match) in enumerate(matches.items()):
    ida_info_path = os.path.join(workdir, ida, 'info.json')
    if not os.path.isfile(ida_info_path):
        print('cannot find', ida_info_path)
        continue
    ida_info = t.load_json(ida_info_path)
    if len(match.idb) == 1:
        idb_info_path =os.path.join(workdir, match.idb[0], 'info.json')
        idb_info = t.load_json(idb_info_path)
        print(ida_info['src'], idb_info['src'])
        # print()
    elif len(match.idb) > 1:
        multiple_mse +=1
        for idb in match.idb:
            idb_info_path =os.path.join(workdir, idb, 'info.json')
            idb_info = t.load_json(idb_info_path)
            print(ida_info['src'], idb_info['src'])
            print(ida, idb)
            show_pair(ida, idb)




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
print('no mse', nomse)
print('multiple mse', multiple_mse)
