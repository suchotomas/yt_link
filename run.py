from preprocess import CreateProcessPool
from match_by_duration import MatchByDuration
import time
import argparse
import os
import json
import numpy as np
from tqdm import tqdm
import cv2
from api.tools import Tools as t
from names import Names as n


# parser = argparse.ArgumentParser()
# parser.add_argument('-w', type=str, required=True, help='workdir')
# parser.add_argument('-y', type=str, required=True, help='json youtube_list_path')
# parser.add_argument('-e', type=str, required=True, help='json exports_list_path')
# parser.add_argument('-t', type=int, required=False, default=0, help='test_len')
# parser.add_argument('-ss', type=int, required=False, default=0, help='from')
# args = parser.parse_args()
#
# yt_list = args.y
# exports_list = args.e
# test_len = args.t
# workdir = args.workdir

exports_list_path = '/mnt/data/palpatine/DATASETS/YT_LINK/HARD_COPY/exports.json'
yt_list_path = '/mnt/data/palpatine/DATASETS/YT_LINK/HARD_COPY/youtube.json'
workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'


# exports_list = '/mnt/data/palpatine/SAMPLES/YT_LINK/REF/list_exports_test.json'
# yt_list = '/mnt/data/palpatine/SAMPLES/YT_LINK/REF/list_youtube_test.json'
# exports_list = '/mnt/data/palpatine/SAMPLES/YT_LINK/REF/list_exports.json'
# yt_list = '/mnt/data/palpatine/SAMPLES/YT_LINK/REF/list_youtube.json'
#
# workdir = '/mnt/data/palpatine/SAMPLES/YT_LINK/REF/workdir'
test_len = 0
ss = 0

workdir = t.create_folder(workdir)
t_start = time.time()
print('\nCREATE PROCESS POOL AND IMAGES')
vl = CreateProcessPool(youtube_path=yt_list_path, exports_path=exports_list_path, workdir=workdir, test_len=test_len, ss=ss)
vl.run()
print('\nMATCH BY DURATION')
m = MatchByDuration(youtube_path=vl.youtube_to_process_path, export_path=vl.export_to_process_path, workdir=workdir)
m.get_duration_lists()

print('done in {:.02f} s'.format(time.time() - t_start))