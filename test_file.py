# from api import mfcc_api
# path = "/jabba/youtube/videos_youtube/zyP1iKkEIfI.mkv"
# # import subprocess as sp
# import numpy as np
# import ffmpeg
# from ffmpeg import Error

# # input = ffmpeg.input(path)
# # audio = input.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
# # print(len(audio))

# def _inv_list(self, coef):
#     icoef = []
#     for i in range(len(coef[0])):
#         icoef.append([coef[a][i] for a in range(len(coef))])

#     return np.asarray(icoef)

# def compute_dist(self, wav_path):
#     sig, sr = mfcc_api.load_audio(wav_path, self.sr, mono=True)
#     mfc_coef = mfcc_api.mfcc(sig, sr)
#     distances = np.asarray(self._dist_flow(mfc_coef))
#     return distances

# def _dist_flow(self, coef):
#     icoef = self._inv_list(coef)
#     distances = [self._dist(icoef[a], icoef[a + 1]) for a in range(len(icoef) - 1)]
#     return distances
# def _dist(self, coefs1, coefs2):
#     coefs1 = coefs1[1:12]
#     coefs2 = coefs2[1:12]
#     return np.linalg.norm(coefs1 - coefs2)
# def extract_audio(filename):
#         try:
#             out, err = (
#                 ffmpeg
#                 .input(filename)
#                 .output('-', format='f32le', acodec='pcm_f32le', ac=1, ar='16000')
#                 .run(cmd='ffmpeg', capture_stdout=True, capture_stderr=True)
#             )
#         except Error as err:
#             print(err.stderr)
#             raise
        
#         return np.frombuffer(out, np.float32)
# audio = extract_audio(path)
# mfcc = mfcc_api.mfcc(sig=audio, sr=16000)
# distances = np.asarray(_dist_flow(mfcc))


# print(len(audio))
# print(len(mfcc))
import time
import random
import numpy as np
from api.tools import Tools as t
# def _inv_list(coef):
#         icoef = []
#         for i in range(len(coef[0])):
#             icoef.append([coef[a][i] for a in range(len(coef))])

#         return np.asarray(icoef)
        
# aaa = np.random.randint(123, size=(1200000, 20))
# # print(aaa)
# t0 = time.time()

# aaa_1 = _inv_list(aaa)
# print(time.time()-t0)
# t1 = time.time()
# aaa=aaa.T
# print(time.time()-t1)
# print(np.array_equal(aaa, aaa_1))
# import os
# yp = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json'
# ep = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json'

# yl = t.load_json(yp)
# el = t.load_json(ep)

# total_size = 0
# whole_list = el

# whole_duration = 0
# for idx, line in enumerate(whole_list):
#     if idx % 1000 == 0:
#         print(idx)
#     if line['duration'] is not None:
#         total_size += line['duration']
# print(total_size/1000/3600)


# ##########
# path = '100_id_list.txt'
# yt_to_process = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json')
# yt_to_process_100 = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process_100.json'
#
# file1 = open(path, 'r')
# lines = file1.read().splitlines()
# id_list = []
# unknown = 0
#
# dct_yt_list = {}
# for item in yt_to_process:
#     dct_yt_list[item['dst']] = item
#
# y100 = []
# for line in lines:
#     key = 'youtube/'+ line.split(',')[-1]
#     if key not in dct_yt_list:
#         unknown +=1
#     else:
#         y100.append(dct_yt_list[key])
# print('unknown', unknown)
# print('new', len(y100))
# # t.save_json(yt_to_process_100, y100)

#
# exports_list = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json')
#
# for
import os
from tqdm import tqdm

DISCS = ['ongoing', 'incoming', 'data-1', 'data-2', 'data-3']

workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'
all_sources = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json')# + t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json')
none_info =0
cannot_find = 0
for idx in tqdm(range(len(all_sources)), ascii=True, desc='process {} lines'.format(len(all_sources))):
    item = all_sources[idx]
    info_path = os.path.join(workdir, item['dst'], 'info.json')
    info = t.load_json(info_path)
    if info is None:
        none_info += 1
    else:
        src = info['src']
        if os.path.isfile(src):
            continue
        saved = False
        for disc in DISCS:
            src_split = src.split('/')
            if src_split[2] == disc:
                continue
            src_split[2] = disc
            new_src = '/'.join(src_split)
            if os.path.isfile(new_src):
                print('{} -> {}'.format(src, new_src))
                info['src'] = new_src
                t.save_json(info_path, data=info)
                saved = True
                break
        if not saved:
            cannot_find += 1

print('none_info', none_info)
print('cannot_find', cannot_find)

