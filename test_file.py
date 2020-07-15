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
import os
yp = '/mnt/data/palpatine/DATASETS/YT_LINK/20200615_abs_paths/youtube.json'
ep = '/mnt/data/palpatine/DATASETS/YT_LINK/20200615_abs_paths/exports.json'

yl = t.load_json(yp)
el = t.load_json(ep)

total_size = 0
whole_list = yl+el
for idx, path in enumerate(whole_list):
    if idx % 1000 == 0:
        print(idx, len(whole_list))
    try:
        size = os.path.getsize(path)
        total_size += size
    except:
        continue
print(total_size)