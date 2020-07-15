import time
import os
import json
from names import Names as n
import time,os, cv2, json
import numpy as np
from tqdm import tqdm
from api.tools import Tools as t
from timeout import timeout

class CreateProcessPool:

    def __init__(self, youtube_path, exports_path, workdir, test_len=0, ss=0):
        self.timestamp = time.time()
        self.youtube_path = youtube_path
        self.exports_path = exports_path
        self.test_len = test_len
        self.run_from = ss
        self.workdir = workdir
    def run(self):

        self.yt_list =t.load_json(self.youtube_path)
        self.ex_list =t.load_json(self.exports_path)
        self.youtube_to_process, self.export_to_process  = [],[]
        print('==> prepare_in_out_list')
        self.prepare_in_out()




        self.youtube_to_process_path = os.path.join(self.workdir, 'youtube_to_process.json')
        self.export_to_process_path = os.path.join(self.workdir, 'export_to_process.json')

        # print('==> read youtube durations')
        # self.read_durations(self.youtube_to_process)
        # t.save_json(self.youtube_to_process_path, self.youtube_to_process)

        print('==> read export durations')
        self.read_durations(self.export_to_process)
        t.save_json(self.export_to_process_path, self.export_to_process)

        return self.youtube_to_process_path, self.export_to_process_path




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
            self.export_to_process.append(self.record(path, out_path))
        for path in self.yt_list:
            basename = os.path.basename(path)
            name, _ = os.path.splitext(basename)
            out_path = os.path.join(n.YOUTUBE, name)
            self.youtube_to_process.append(self.record(path, out_path))




    def read_durations(self, data):
        for idx in tqdm(range(len(data)), ascii=True, desc='ffprobe on {} files'.format(len(data))):
            record = data[idx]
            try:
                duration = t.get_duration(record[n.SRC])
                data[idx][n.DURATION] = duration * 1000
            except Exception as e:
                print(record, e)


class CreateImages:
    def __init__(self):
        pass
    def process(self, youtube_path, exports_path, workdir):

        yt_list = t.load_json(youtube_path)
        ex_list = t.load_json(exports_path)
        self.test_len = 0
        self.run_from = 41609
        self.timestamp=  time.time()
        self.list_to_process = yt_list + ex_list



        self.err_file = os.path.join(workdir, 'errors.json')


        run_to = self.run_from + self.test_len if self.test_len != 0 else len(self.list_to_process)


        errors = []
        for idx in tqdm(range(run_to), ascii=True, desc='process {} links'.format(run_to)):
            if idx < self.run_from:
                continue
            record = self.list_to_process[idx]
            path, out_path_rel = record['src'], record['dst']
            out_path = t.create_folder(os.path.join(workdir, out_path_rel))



            name = 'image.png'
            name_info = 'info.json'
            out = os.path.join(out_path, name)
            out_info = os.path.join(out_path, name_info)
            if os.path.isfile(out):
                continue

            try:
                # print(f_idx)
                frame, info = self.get_full_frame(path)
                info['src']=path
                # np.save(out, frame)
                cv2.imwrite(out, frame)
                with open(out_info, 'w') as outfile:
                    json.dump(info, outfile, indent=4)

            except Exception as e:
                err = '{}: {}'.format(path, e)
                print(err)
                errors.append(err)

            # print(info)
        if len(errors):
            with open(self.err_file, 'w') as outfile:
                json.dump(errors, outfile, indent=4)

    @timeout(10)
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
                frame = np.zeros((360, 640, 3), dtype=np.uint8)
            else:
                frame = cv2.resize(frame, (640, 360))

            frames[idx] = frame

        info = {'duration': duration,
                'timecodes': np.ndarray.tolist(timecodes),
                'fps': '{}'.format(fps),
                'frame_count': '{}'.format(frame_count),
                'rets': rets,

                'timestamp': self.timestamp
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

# '''/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process_no_dur.json
# /mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process_no_dur.json'''
# yt_list = '/mnt/data/palpatine/SAMPLES/YT_LINK/REF/workdir/youtube_to_process.json'
# ex_list = '/mnt/data/palpatine/SAMPLES/YT_LINK/REF/workdir/export_to_process.json'
# workdir = '/mnt/data/palpatine/SAMPLES/YT_LINK/REF/workdir'

# yt_list = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process_no_dur.json'
# ex_list = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process_no_dur.json'
# workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'
