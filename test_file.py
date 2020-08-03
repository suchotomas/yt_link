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
# import time
# import random
# import numpy as np
# from api.tools import Tools as t
# # def _inv_list(coef):
# #         icoef = []
# #         for i in range(len(coef[0])):
# #             icoef.append([coef[a][i] for a in range(len(coef))])
#
# #         return np.asarray(icoef)
#
# # aaa = np.random.randint(123, size=(1200000, 20))
# # # print(aaa)
# # t0 = time.time()
#
# # aaa_1 = _inv_list(aaa)
# # print(time.time()-t0)
# # t1 = time.time()
# # aaa=aaa.T
# # print(time.time()-t1)
# # print(np.array_equal(aaa, aaa_1))
# # import os
# # yp = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json'
# # ep = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json'
#
# # yl = t.load_json(yp)
# # el = t.load_json(ep)
#
# # total_size = 0
# # whole_list = el
#
# # whole_duration = 0
# # for idx, line in enumerate(whole_list):
# #     if idx % 1000 == 0:
# #         print(idx)
# #     if line['duration'] is not None:
# #         total_size += line['duration']
# # print(total_size/1000/3600)
#
#
# # ##########
# # path = '100_id_list.txt'
# # yt_to_process = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json')
# # yt_to_process_100 = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process_100.json'
# #
# # file1 = open(path, 'r')
# # lines = file1.read().splitlines()
# # id_list = []
# # unknown = 0
# #
# # dct_yt_list = {}
# # for item in yt_to_process:
# #     dct_yt_list[item['dst']] = item
# #
# # y100 = []
# # for line in lines:
# #     key = 'youtube/'+ line.split(',')[-1]
# #     if key not in dct_yt_list:
# #         unknown +=1
# #     else:
# #         y100.append(dct_yt_list[key])
# # print('unknown', unknown)
# # print('new', len(y100))
# # # t.save_json(yt_to_process_100, y100)
#
# #
# # exports_list = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json')
# #
# # for
# ########################################
# # import os
# # from tqdm import tqdm
#
# # DISCS = ['ongoing', 'incoming', 'data-1', 'data-2', 'data-3']
#
# # workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'
# # all_sources = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json')# + t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json')
# # none_info =0
# # cannot_find = 0
# # for idx in tqdm(range(len(all_sources)), ascii=True, desc='process {} lines'.format(len(all_sources))):
# #     item = all_sources[idx]
# #     info_path = os.path.join(workdir, item['dst'], 'info.json')
# #     info = t.load_json(info_path)
# #     if info is None:
# #         none_info += 1
# #     else:
# #         src = info['src']
# #         if os.path.isfile(src):
# #             continue
# #         saved = False
# #         for disc in DISCS:
# #             src_split = src.split('/')
# #             if src_split[2] == disc:
# #                 continue
# #             src_split[2] = disc
# #             new_src = '/'.join(src_split)
# #             if os.path.isfile(new_src):
# #                 print('{} -> {}'.format(src, new_src))
# #                 info['src'] = new_src
# #                 t.save_json(info_path, data=info)
# #                 saved = True
# #                 break
# #         if not saved:
# #             cannot_find += 1
#
# # print('none_info', none_info)
# # print('cannot_find', cannot_find)


###################################################################################################################
# import os, time
# from api.tools import Tools as t
# from file_to_mfcc import FileToMFCC
# from file_to_video_vector import FileToVideoVector
# from api.offset_calc import OffsetCalc
# from tqdm import tqdm
# import random
# import shutil
#
# offset_calc = OffsetCalc()
#
# # idy, ide = 'youtube/KmuV4I1D6xQ','export/1877/EXPORT/D2-D6_Seaside_Ballroom/D6_Andrej'
# # workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'
#
# idy, ide = 'a','b'
# workdir = '/mnt/data/palpatine/SAMPLES/YT_LINK/sample'
#
# a_filename = 'distances.npy'
# v_filename = 'video_vector.npy'
#
# OVERWRITE_A = False
# OVERWRITE_V = False
#
# def get_tmp_src(id_key,src):
#
#     tmp_path = os.path.join(workdir, id_key, os.path.basename(src))
#
#     return tmp_path
#
#
# def get_vectors(id_key, info):
#     print(id_key)
#     src_tmp = get_tmp_src(id_key, info['src'])
#     a_path = os.path.join(workdir, id_key, a_filename)
#     run_audio = not os.path.isfile(a_path) or OVERWRITE_A
#
#     v_path = os.path.join(workdir, id_key, v_filename)
#     run_video = not os.path.isfile(v_path) or OVERWRITE_V
#
#     if run_audio or run_video:
#         if not os.path.isfile(src_tmp):
#             t_copy = time.time()
#             print('copy', src_tmp)
#             shutil.copyfile(info['src'], src_tmp)
#             print('... {:0.2f}', time.time() - t_copy)
#
#     if run_audio:
#         print('a_path')
#         t_a = time.time()
#         a_path = file2mfcc.run(src_tmp, a_path)
#         t2 = time.time()
#         print('... {:0.2f}', time.time() - t_a)
#
#     if run_video:
#         print('v_path')
#         t_v = time.time()
#         v_path = file2video_vector.run(src_tmp, v_path)
#         t3 = time.time()
#         print('... {:0.2f}', time.time() - t_v)
#
#     # if os.path.isfile(src_tmp):
#     #     if 'jabba' not in src_tmp:
#     #         os.remove(src_tmp)
#     #     else:
#     #         raise('ERROR - jabba in src_tmp')
#     #         exit(1)
#     return a_path, v_path
#
#
# y_info = t.load_json(os.path.join(workdir, idy, 'info.json'))
# e_info = t.load_json(os.path.join(workdir, ide, 'info.json'))
#
# print(ide, idy)
# file2mfcc = FileToMFCC(workdir)
# file2video_vector = FileToVideoVector(workdir)
#
#
# y_a_path, y_v_path = get_vectors(idy, y_info)
# e_a_path, e_v_path = get_vectors(ide, e_info)
#
#
# print(offset_calc.calculate(y_a_path, y_info['duration'], e_a_path, e_info['duration']))
# print(offset_calc.calculate(y_v_path, y_info['duration'], e_v_path, e_info['duration']))
# print()

####################################################################################################################

## popular list to process
# import os, time
# from api.tools import Tools as t
# from file_to_mfcc import FileToMFCC
# from file_to_video_vector import FileToVideoVector
# from api.offset_calc import OffsetCalc
# from tqdm import tqdm
# import random
# import shutil
#
# y_popular_id_list = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/100_popular_from_2017.json')
# y_list = t.load_json('/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json')
#
#
# all_youtube_dict_by_id = {}
#
# for item in y_list:
#     y_id = item['src'].split('/')[-1].split('.')[0]
#     all_youtube_dict_by_id[y_id]=item
#
#
# new_list_to_process = []
# ok = 0
# for y_id_pop in y_popular_id_list:
#     if y_id_pop in all_youtube_dict_by_id:
#         ok += 1
#
#         new_list_to_process.append(all_youtube_dict_by_id[y_id_pop])
# print('{}/{}'.format(ok, len(y_popular_id_list)))
# t.save_json('/mnt/data/palpatine/DATASETS/YT_LINK/100_popular_from_2017_to_process.json', new_list_to_process)

###################################################################################################################3

from api.tools import Tools as t
from tqdm import tqdm
import os
y = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json'
e = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json'
workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'
all = t.load_json(e) + t.load_json(y)

video_exts = ['.MP4', '.WEBM', '.MKV', '.MOV']
cnt = 0
sizes = 0
for idx in tqdm(range(len(all)), ascii=True, desc='process {} lines'.format(len(all))):
    item = all[idx]
    dst = item['dst']
    folderpath = os.path.join(workdir, dst)
    listdir = os.listdir(folderpath)
    # for name in listdir:
    #     sizes += os.path.getsize(os.path.join(folderpath, name))
    if 'info.json' not in listdir:
        cnt += 1
        print(folderpath)
    # videos = [os.path.join(folderpath, name) for name in listdir if os.path.splitext(name)[1].upper() in video_exts]
    # for video in videos:
    #     print('DELETE',video)
        # input()
        # os.remove(video)


    # if len(videos):
    #     cnt +=1
    #     print(videos)
# print(sizes/1024/1024/1024)
print(cnt,len(all))