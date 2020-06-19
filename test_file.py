# # import numpy as np
# # import cv2 as cv
# # import time
# # from global_modules.common import Common
# # from skimage.measure import compare_ssim
# # from palpatine.names import Names
# # path = '/mnt/data/palpatine/SAMPLES/slideslive-recorder_20200407T172646.662Z_display.mp4'
# # path = '/jabba/shared/_LAB/SlidesCaptureHW/David Assist/programopvani/Sequence 02.mp4'
# # # path = '/jabba/shared/_LAB/SlidesCaptureHW/David Assist/programopvani/Sequence 02.mp4'
# # # path = '/jabba/shared/_LAB/Palpatine/SAMPLES/pomaly_prechod/0-0014.mp4'
# # # path = '/mnt/data/palpatine/SAMPLES/assist_capture.mp4'
# # save_all = False
# # class SlideDetector:
# #
# #     def __init__(self, path):
# #         self.capture = cv.VideoCapture(path)
# #         self.time_gauss = 0
# #         self.time_ssim = 0
# #         self.time_load = 0
# #         self.time_save = 0
# #
# #
# #     def getMSSISM(self, i1, i2):
# #         C1 = 6.5025
# #         C2 = 58.5225
# #         # INITS
# #         I1 = np.float32(i1)  # cannot calculate on one byte large values
# #         I2 = np.float32(i2)
# #         I2_2 = I2 * I2  # I2^2
# #         I1_2 = I1 * I1  # I1^2
# #         I1_I2 = I1 * I2  # I1 * I2
# #         # END INITS
# #
# #         t0 = time.time()
# #         # PRELIMINARY COMPUTING
# #         kernel_size = 7
# #         mu1 = cv.GaussianBlur(I1, (kernel_size, kernel_size), 1.5)
# #         mu2 = cv.GaussianBlur(I2, (kernel_size, kernel_size), 1.5)
# #         mu1_2 = mu1 * mu1
# #         mu2_2 = mu2 * mu2
# #         mu1_mu2 = mu1 * mu2
# #         sigma1_2 = cv.GaussianBlur(I1_2, (kernel_size, kernel_size), 1.5)
# #         sigma1_2 -= mu1_2
# #         sigma2_2 = cv.GaussianBlur(I2_2, (kernel_size, kernel_size), 1.5)
# #         sigma2_2 -= mu2_2
# #         sigma12 = cv.GaussianBlur(I1_I2, (kernel_size, kernel_size), 1.5)
# #         sigma12 -= mu1_mu2
# #         self.time_gauss += time.time() - t0
# #
# #         t1 = 2 * mu1_mu2 + C1
# #         t2 = 2 * sigma12 + C2
# #         t3 = t1 * t2                    # t3 = ((2*mu1_mu2 + C1).*(2*sigma12 + C2))
# #         t1 = mu1_2 + mu2_2 + C1
# #         t2 = sigma1_2 + sigma2_2 + C2
# #         t1 = t1 * t2                    # t1 =((mu1_2 + mu2_2 + C1).*(sigma1_2 + sigma2_2 + C2))
# #
# #         t_ssim0 = time.time()
# #         ssim_map = cv.divide(t3, t1)    # ssim_map =  t3./t1;
# #         mssim = cv.mean(ssim_map)       # mssim = average of ssim map
# #         self.time_ssim += time.time() - t_ssim0
# #         return mssim
# #
# #
# #
# #     def get_mssim(self, frame1, frame2, segm_size, wh):
# #         local_mssim = []
# #
# #         for ii in range(0, wh[1], segm_size):
# #             for jj in range(0, wh[0], segm_size):
# #                 s1 = frame1[ii:ii + segm_size, jj:jj + segm_size]
# #                 s2 = frame2[ii:ii + segm_size, jj:jj + segm_size]
# #
# #                 mssim = self.getMSSISM(s1, s2)
# #                 min_mssim = min(mssim[:-1])
# #                 local_mssim.append(min_mssim)
# #         mssim = min(local_mssim)
# #         return mssim
# #
# #     def _get_frame(self):
# #         t0 = time.time()
# #         ret, frame = self.capture.read()
# #         self.time_load += time.time() - t0
# #         return ret, frame
# #
# #     def run(self):
# #         time_start = time.time()
# #         segm_size = 50
# #         width = 650
# #         height = 350
# #         wh = width, height
# #
# #         timecode = 0
# #         last2_was_cut = False
# #         last3_was_cut = False
# #         last4_was_cut = False
# #
# #         frame_last1 = None
# #         frame_last2 = None
# #         frame_last3 = None
# #         frame_last4 = None
# #
# #         first_slide = True
# #         while True:
# #
# #             timecode += 1
# #             ret, frame = self._get_frame()
# #             if not ret:
# #                 break
# #             frame_full_size = frame.copy()
# #             frame = cv.resize(frame, (width, height))
# #             # frame = cv.blur(frame, (3, 3))
# #
# #             if frame_last1 is None:
# #                 frame_last1 = frame
# #
# #             if timecode % 25 != 0:
# #                 continue
# #
# #
# #             mssim01 = self.get_mssim(frame, frame_last1, segm_size, wh)
# #             mssim02 = 0.
# #             mssim03 = 0.
# #             mssim04 = 0.
# #
# #             threshold = 0.95
# #             corrected = False
# #             if not mssim01 < threshold and last2_was_cut:
# #                 mssim02 = self.get_mssim(frame, frame_last2, segm_size, wh)
# #                 if mssim02 < threshold:
# #                     corrected = True
# #                     threshold = 0.99
# #
# #             is_cut = mssim01 < threshold
# #             # if not is_cut and last3_was_cut:
# #             #     mssim03 = self.get_mssim(frame, frame_last3, segm_size, wh)
# #             #     is_cut = mssim03 < 0.95
# #             # if not is_cut and last4_was_cut:
# #             #     mssim04 = self.get_mssim(frame, frame_last4, segm_size, wh)
# #             #     is_cut = mssim04 < 0.95
# #             timestep = Common.seconds_to_readable_time_underline(timecode/25)
# #             print('{}: ({}) {:.03f}, {:.03f},{:.03f}, {}'.format(timestep, timecode, mssim01,mssim02 - mssim01 if mssim02 > 0 else 0,threshold, is_cut))
# #
# #             # if not is_cut and last2_was_cut or first_slide or save_all:
# #             if is_cut or first_slide:
# #
# #                 # cv.imshow('image', frame)
# #                 tsave0 = time.time()
# #                 cv.imwrite('/mnt/data/palpatine/SAMPLES/slideDetekce/test_jpg4/'+
# #                            timestep + '.jpg', frame_full_size)
# #                 self.time_save += time.time() - tsave0
# #                 # k = cv.waitKey(0)
# #                 # if k == 27:
# #                 #     exit()
# #             first_slide = False
# #
# #
# #             frame_last4 = frame_last3
# #             frame_last3 = frame_last2
# #             frame_last2 = frame_last1
# #             frame_last1 = frame
# #             last4_was_cut = last3_was_cut
# #             last3_was_cut = last2_was_cut
# #             last2_was_cut = is_cut if not corrected else False
# #
# #         print('time_ssim: ', self.time_ssim)
# #         print('time_gauss: ', self.time_gauss)
# #         print('time_load: ', self.time_load)
# #         print('time_save ', self.time_save)
# #         print('whole', time.time() - time_start)
# #         print('fps: ',timecode/ (time.time() - time_start))
# # SlideDetector(path).run()
#
# # import numpy as np
# # buffer_len = 123
# # print(np.arange(0,buffer_len,26))
# # print(np.arange(0, buffer_len, 26//2))
# import shlex
# import subprocess
# import json
# import os
# import magic
#
# # file_path = '/jabba/shared/_LAB/Palpatine/SAMPLES/not_16_9_display.webm'
# file_path = '/mnt/data/palpatine/SAMPLES/slideslive-recorder_20200409T020001.893Z_display.webm'
#
#
# mime = magic.Magic(mime=True)
# aa = str(mime.from_file(file_path)).split('/')
# exit()
#
#
# cmd = 'ffprobe -v quiet -print_format json -show_frames -show_entries frame=width,height,pkt_dts_time -select_streams v:0 "' + file_path + '"'
#
# # cmd = 'ffprobe -v quiet -print_format json -show_format -show_streams "' + file_path + '"'
# args = shlex.split(cmd)
# ffprobe_output = subprocess.check_output(args).decode('utf-8')
# ffprobe_json =  json.loads(ffprobe_output)
# lines = ffprobe_json['frames']
# filepath, _ = os.path.splitext(file_path)
# filename =os.path.basename(file_path)
# final_out_path = '{}/{}.mp4'.format(os.path.dirname(file_path),filename)
#
# parts = []
#
# last_t = 0.
# last_wh = (0,0)
#
# lines_with_timecode = []
# for line in lines:
#     if 'pkt_dts_time'  in line:
#         lines_with_timecode.append(line)
#
#
# for idx, line in enumerate(lines_with_timecode):
#     t, w, h = line['pkt_dts_time'], line['width'], line['height']
#     if (w,h) != last_wh:
#         if idx>0:
#             parts.append((last_t,  t, last_wh))
#         last_t = t
#         last_wh = (w,h)
# if last_t != lines_with_timecode[-1]['pkt_dts_time']:
#     parts.append((last_t, lines_with_timecode[-1]['pkt_dts_time'],(lines_with_timecode[-1]['width'], lines_with_timecode[-1]['height'])))
#
# [print(part) for part in parts]
#
# exit()
# stream_paths = []
# for idx, part in enumerate(parts):
#     # cmd = 'ffmpeg -i "'+ file_path + '"-vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1" -c:a copy '
#     out_path = '{}/{}_part{}.mp4'.format(os.path.dirname(file_path),filename, idx)
#     cmd = 'ffmpeg -nostdin -loglevel info -y  -i "{}" ' \
#           '-vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1" ' \
#           '-c:a aac -b:a 240k -c:v h264 -r 25 -max_muxing_queue_size 10240 "{}"'.format(file_path, out_path)
#     args = shlex.split(cmd)
#     subprocess.check_output(args).decode('utf-8')
#     stream_paths.append(out_path)
#
#
# if len(stream_paths) == 1:
#     input_string = '-i "%s"' % (stream_paths[0])
# else:
#
#     paths = '|'.join(stream_paths)
#     input_string = '-i "concat:%s" ' % (paths)
# cmd = 'ffmpeg -n %s  -c copy "%s"'%(
#                    input_string, final_out_path)
# args = shlex.split(cmd)
# subprocess.check_output(args).decode('utf-8')

# import  time
# print((time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
#
# # import os
# # path = '/jabba/shared/_LAB/Palpatine/tmp/test_path'
# # list_dir  = os.listdir(path)
# # for file in list_dir:
# #     print(os.path.join(path, file))
# #     os.remove(os.path.join(path, file))
# # os.removedirs(path)
#
# from global_modules.common import  Common
# track_name = '/mnt/data/palpatine/PALPATINE_FILES/'
# path = '/mnt/data/palpatine/PALPATINE_FILES/_OTHER_SyxrxR4KPS_v2/0_SyxrxR4KPS_jabba.xml'
#
# # print(Common.abs2rel_path(path, track_name))
# import os
# import shutil
# from autosync.content_loader.copy_files import CopyPool
# from global_modules.common import Common
# from palpatine.logger import Logger
# copy_from = '/mnt/data/palpatine/PALPATINE_FILES/Palpatine_5min_talk_2cam_audio_v32/copy_to_source'
# copy_to = 'jabba/talk/SOURCE/'
# # shutil.copytree(copy_from, copy_to)
#
# data_to_copy = []
# total_size = 0
# for root, directories, filenames in os.walk(copy_from):
#     for filename in filenames:
#         from_path = os.path.join(root, filename)
#         to_path = copy_to + Common.abs2rel_path(from_path, copy_from)
#         data_to_copy.append((0,from_path, to_path))
#
# data_to_copy_with_sizes, whole_size = CopyPool.get_paths_with_sizes(data_to_copy)
# copied = 0
# for idx, (_,from_path, to_path,size) in enumerate(data_to_copy_with_sizes):
#     Logger.pr('copying....')
#     copied += size
#     CopyPool.write_stat_line(Logger, idx, copied, whole_size, to_path, size, len(data_to_copy_with_sizes))
#     # shutil.copyfile(from_path, to_path)
#
# import numpy as np
# from numba import jit
# from detections.scripts.module_scripts import ModuleScripts as ms
# # @jit(nopython=True)
#
# def null_small_parts(array, win_len, mask=None):
#     win_len += 1
#     if mask is not None:
#         start = np.argmax(mask)
#         b = mask[::-1]
#         end = mask.shape[0] - np.argmax(b) - 1
#     else:
#         start = 0
#         end = len(array)
#     for timecode in range(len(array)):
#         half = int(win_len / 2)
#         if timecode - half < start or timecode + half + 1 > end:
#             continue
#         if not array[timecode - half] and not array[timecode + half]:
#             array[timecode - half:timecode + half + 1] = False
#     return array
#
# import time
# path = '/mnt/data/palpatine/PALPATINE_FILES/videa_externisti_20200406T185355Z__composing-task-agnostic-polici__H1ezFREtwH_v11/slides_timeline.npy'
# path = '/mnt/data/palpatine/PALPATINE_FILES/videa_externisti_20200422T230246Z__tbd__PML4DC2020_v4/slides_timeline.npy'
# array = np.load(path)
# array = np.array(array, dtype=np.int)
# ms.fill_gaps(array, 3)
# t0 = time.time()
# videos = ms.null_small_parts(array.copy(), win_len=12)
# t1 = time.time()
# ms.fill_gaps(videos, 10)
# t2=time.time()
# final = np.logical_or(array, videos)
# final = np.array(final, dtype=np.int)
# t3=time.time()
#
#
# print('null', t1-t0)
# print('fill_gaps', t2-t1)
# print('log_or', t3-t2)
#
# start,end = (2664, 2744)
# print(array[start:end])
# print(videos[start:end])
# print(final[start:end])
# from palpatine.names import Names as n
# from global_modules.common import Common

# list_of_known_video_formats = Common.uppercase(['.mp4', '.avi', '.wmv', '.webm', '.mkv', '.mov', '.flv', '.mpg', '.ts', '.m4v','.m4a','.3gp','.3g2'])
# list_of_known_audio_formats = Common.uppercase(['.wav', '.flac', '.wma', '.aac', '.amr'])
#
# wiki_audio = Common.uppercase(n.AUDIO_EXTENSIONS)
# wiki_video = Common.uppercase(n.VIDEO_EXTENSIONS)
#
# v = ['.MP4', '.MTS', '.MOV', '.MXF', '.MPG', '.M2TS']
# print(wiki_video)
# for ext in v:
#     if ext not in wiki_video:
#         print(ext)
#
# exit()
#
# checked_audio = []
# for ext in wiki_audio:
#     if ext not in wiki_video:
#         checked_audio.append(ext)
# print(checked_audio)
# import shlex
# import subprocess
# import json
# from pymediainfo import MediaInfo
# file_path = '/jabba/shared/_LAB/Palpatine/FINAL_TESTS/videa_externisti/SOURCE/HklXn1BKDH/slideslive-recorder_20200409T025833.439Z_user.webm'
# # file_path = '/jabba/shared/_LAB/Palpatine/FINAL_TESTS/videa_externisti/SOURCE/HklXn1BKDH/slideslive-recorder_20200409T025833.441Z_display.webm'
# # cmd = 'ffprobe -v quiet -print_format json -show_streams stream=codec_name -of default=noprint_wrappers=1 "' + file_path + '"'
# # cmd = 'ffprobe -v quiet -print_format json -show_format -show_streams "' + file_path + '"'
# # args = shlex.split(cmd)
# # ffprobe_output = subprocess.check_output(args).decode('utf-8')
# # ffprobe_json = json.loads(ffprobe_output)
# # [print(stream) for stream in ffprobe_json['streams']]
#
# data = MediaInfo.parse(file_path)
# tracks = data.to_data()['tracks']
# streams = []
# for track in tracks:
#     streams.append(track['track_type'].lower())
# # print(streams)
# import os
# def win_path(path, event_path):
#     event_name = os.path.basename(event_path)
#     # print(path)
#     path = path.split(event_path)
#     win_path = 'D:/%s%s' % (event_name, path[1])
#     return win_path
#
#
# def _jabba_path(path_org):
#     try:
#         jabba_name = n.JABBA_NAME
#         path = path_org
#         path = path.split('/', 2)[-1]
#         path = jabba_name + '/' + path
#         path = '//' + path
#     except:
#         path = '/' + path_org
#
#     return path
#
# event_path = '/jabba/incoming/2020_07_12-18-international_conference_on_machine_learning_2020-2635'
# path = '/jabba/incoming/2020_07_12-18-international_conference_on_machine_learning_2020-2635/PROJECT/GRAPHICS/audio_only.png'
#
# print(_jabba_path(path))
# print(win_path(path,event_path))

#
# room_path = '/jabba/shared/_LAB/Palpatine/FINAL_TESTS/videa_externisti/SOURCE/H1ezFREtwH'
# import os
# from global_modules.common import Common
#
# def read_txt_file(path):
#     f = open(path, "r")
#     return f.read()
#
# def load_notes_in_sl_recorder(room_path):
#     whole_text = []
#     room_path_file_list = os.listdir(room_path)
#     room_path_file_list = sorted(room_path_file_list)
#     for filename in room_path_file_list:
#         read=False
#         name, ext = os.path.splitext(filename)
#         filepath = os.path.join(room_path,filename)
#         if ext != '.txt':
#             continue
#         if name == '__links':
#             read = True
#         elif name.split('_')[0] == 'note' and name.split('_')[1].isnumeric():
#             read = True
#
#         if read:
#             text = '{}:\n{}\n'.format(filename, read_txt_file(filepath))
#             whole_text.append(text)
#     return whole_text
# comment = load_notes_in_sl_recorder(room_path)
# [print(c) for c  in comment]


# ref_links = []
# json_path_out = '/mnt/data/palpatine/ref_verca.json'
# path = '/mnt/data/palpatine/SAMPLES/YT_LINK/Vimeo migration - DONE - data-3_2019-Veronika.csv'
# used_exts = {}
# with open(path, 'r') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         id = row[2].rsplit('/', 1)[-1]
#         path = row[3]
#         if len(path) and path[-1] == ' ':
#             path = path[:-1]
#         _,ext = os.path.splitext(path)
#         if ext not in used_exts:
#             used_exts[ext]=0
#         used_exts[ext] += 1
#
#         if len(id) and ext != '':
#             ref_links.append([id, path])
# print(used_exts)
# [print(ii) for ii in ref_links]
#
# with open(json_path_out, 'w') as outfile:
#     json.dump(ref_links, outfile, indent=4)
# import json
# exports_list_path = '/mnt/data/palpatine/SAMPLES/YT_LINK/1592320273.7976253/youtube.json'
# with open(exports_list_path, 'r') as f:
#     exports_list = json.load(f)
#
# print(len(exports_list))
#
# import json
# exports_list_path = '/mnt/data/palpatine/SAMPLES/YT_LINK/ref_list_test.json'
# exports_list_path2 = '/mnt/data/palpatine/SAMPLES/YT_LINK/ref_list_test2.json'
# with open(exports_list_path, 'r') as f:
#     exports_list = json.load(f)
#
# extracted = []
# for yt, export in exports_list:
#    export = '/jabba/' + export
#    extracted.append([yt,export])
# with open(exports_list_path2, 'w') as outfile:
#     json.dump(extracted, outfile, indent=4)
# print(len(extracted))

#
# import cv2
# import numpy as np
# path = '/jabba/data-3/2019_01_01-spolecnost_pro_vyzivu_sestrih_prednasek-1589/EXPORT/01-petrekova.mp4'
# path2 = '/jabba/youtube/videos_youtube/Y-nWqSx0LUs.mp4'
#
# def get_frame(path):
#     cap = cv2.VideoCapture(path)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     duration = int(1000 * (frame_count / fps))
#
#     first_frame = 6
#     last_frame  = frame_count - 6
#
#
#     timecodes = np.arange(6,frame_count-6, frame_count//9)
#     frames = np.zeros((9,360,640,3), dtype=np.int16)
#     for idx, timecode in enumerate(timecodes):
#         cap.set(cv2.CAP_PROP_POS_FRAMES, timecode)
#         ret, frame = cap.read()
#         frame = cv2.resize(frame, (640,360))
#
#         frames[idx] = frame
#
#     a = np.concatenate((frames[0:3]), axis=0)
#     b = np.concatenate((frames[3:6]), axis=0)
#     c = np.concatenate((frames[6:9]), axis=0)
#
#     full_frame = np.concatenate((a,b,c), axis = 1)
#     #
#     # cv2.imshow('frame', full_frame)
#     # cv2.waitKey(0)
#
#     cap.release()
#     return full_frame
#
#
# # frame1 = get_frame(path)
# # frame2 = get_frame(path2)
# # diff_img = abs(frame2-frame1)
# # diff_img[diff_img < 10] = 0
# # diff_img = np.array(diff_img, dtype=np.uint8)
# # cv2.imshow('frame', diff_img)
# # cv2.waitKey(0)


import json
def load_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data



def save_json(path, data):
    with open(path, 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

data = load_json('/mnt/data/palpatine/SAMPLES/YT_LINK/REF/workdir/list_to_process.json')

out = {}
for item in data:
    if item['dst'] in out:
        continue
    out[item['dst']] = item

save_json('/mnt/data/palpatine/SAMPLES/YT_LINK/REF/workdir/list_to_process_new.json', out)