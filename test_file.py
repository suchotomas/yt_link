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

path = '100_id_list.txt'
yt_to_process = t.load_pickle('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_mse.pickle')
new_matches = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_100.pickle'

file1 = open(path, 'r') 
lines = file1.read().splitlines()
id_list = []
unknown = 0
matches100 = {}
for line in lines:
    key = 'youtube/'+ line.split(',')[-1]
    if key not in yt_to_process:
        unknown +=1
    matches100[key] = yt_to_process[key]
print('unknown', unknown)
print('new', len(matches100))
t.save_pickle(new_matches, matches100)

