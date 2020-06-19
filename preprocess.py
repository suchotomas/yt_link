import time
import os
import json
import numpy as np
from tqdm import tqdm
import cv2
from api.tools import Tools
from names import Names as n

class CreateProcessPool:

    def __init__(self, youtube_path, exports_path, workdir, test_len=0, ss=0):
        self.timestamp = time.time()

        self.youtube_path = youtube_path
        self.exports_path = exports_path
        self.test_len = test_len
        self.run_from = ss
        self.workdir = workdir



    def run(self):
        self.yt_list = self.load_json(self.youtube_path)
        self.ex_list = self.load_json(self.exports_path)
        self.youtube_to_process, self.export_to_process  = {},{}
        self.prepare_in_out()

        self.read_durations(self.youtube_to_process)
        self.read_durations(self.export_to_process)


        self.save_json(os.path.join(self.workdir, 'youtube_to_process.json'), self.youtube_to_process)
        self.save_json(os.path.join(self.workdir, 'export_to_process.json'), self.export_to_process)

    @staticmethod
    def load_json(path):
        with open(path, 'r') as f:
            data  = json.load(f)
        return data

    @staticmethod
    def save_json(path, data):
        with open(path, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)

    @staticmethod
    def record(src, dst):
        return {
            n.SRC: src,
            n.DST: dst,
            n.DURATION: None}

    def prepare_in_out(self):
        for path in self.ex_list:
            splitted = path.split('/',4)
            event_id = splitted[3].rsplit('-', 1)[-1]

            name, _ = os.path.splitext(splitted[-1])
            out_path = os.path.join(n.EXPORT, event_id, name)
            self.export_to_process[out_path] = self.record(path, out_path)

        for path in self.yt_list:
            basename = os.path.basename(path)
            name, _ = os.path.splitext(basename)
            out_path = os.path.join(n.YOUTUBE, name)
            self.youtube_to_process[out_path] = self.record(path, out_path)




    def read_durations(self, data):
        for key, record in tqdm(data.items(), ascii=True, desc='process {} records'.format(len(data))):
            try:
                duration = Tools.get_duration(record[n.SRC])
                data[key][n.DURATION] = duration
            except Exception as e:
                print(record, e)



    def process(self):
        # Afilename, _ = os.path.splitext(self.main_list_path)
        # Bfilename, _ = os.path.splitext(self.second_list_path)

        process_list_a = []
        for idx, (in_path, out_path) in enumerate(self.list_to_process):

            if self.test_len !=0 and idx > self.test_len:
                continue

        run_to = self.run_from + self.test_len if self.test_len != 0 else len(self.list_to_process)

        errors = []
        for idx in tqdm(range(run_to), ascii=True, desc='process {} links'.format(run_to)):
            if idx < self.run_from:
                continue
            in_path, out_path = self.list_to_process
            name = '{}.png'.format(self.timestamp)
            name_info = '{}.info'.format(self.timestamp)
            out = os.path.join(out_path, name)
            out_info = os.path.join(out_path, name_info)

            try:
                # print(f_idx)
                frame, info = self.get_full_frame(path)
                # np.save(out, frame)
                cv2.imwrite(out, frame)
                with open(out_inf, 'w') as outfile:
                    json.dump(info, outfile, indent=4)

            except Exception as e:
                err=(f_idx, path, e)
                print(err)
                errors.append(err)

            # print(info)
        if len(errors):

            with open(self.err_file, 'w') as outfile:
                json.dump(errors, outfile, indent=4)



    def get_full_frame(self, path):

        cap = cv2.VideoCapture(path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = int(1000 * (frame_count / fps))
        timecodes = np.linspace(6, frame_count - 6, 9, dtype=np.int)
        frames = np.zeros((9, 360, 640, 3), dtype=np.uint8)
        rets = []
        for idx, timecode in enumerate(timecodes):
            cap.set(cv2.CAP_PROP_POS_FRAMES, timecode)
            ret, frame = cap.read()
            rets.append(ret)
            if not ret:
                frame = np.zeros((360,640,3), dtype=np.uint8)
            else:
                frame = cv2.resize(frame, (640, 360))

            frames[idx] = frame

        info = {'duration': duration,
                'timecodes': np.ndarray.tolist(timecodes),
                'fps': '{}'.format(fps),
                'frame_count': '{}'.format(frame_count),
                'rets':rets,
                'timestamp':self.timestamp
                }
        a = np.concatenate((frames[0:3]), axis=0)
        b = np.concatenate((frames[3:6]), axis=0)
        c = np.concatenate((frames[6:9]), axis=0)


        full_frame = np.concatenate((a, b, c), axis=1)
        #
        # cv2.imshow('frame', full_frame)
        # cv2.waitKey(0)

        cap.release()

        return full_frame, info

    def run_list(self, video_list, img_dir=None, get_images=False):
        dur_len = len(video_list) if self.test_len is None else self.test_len
        durations = np.zeros(dur_len, dtype=np.int)
        for idx in tqdm(range(dur_len), ascii=True, desc='checks {} links'.format(dur_len)):
            path = video_list[idx]
            cap = cv2.VideoCapture(path)
            try:
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                duration = int(1000*(frame_count/fps))

            except:
                duration = 0
            durations[idx] = duration

            cap.release()
        return durations


class Match:
    def __init__(self, ida):
        self.ida = ida
        self.idb = []
        self.diff = []
        self.adur = None
        self.bdur = None
