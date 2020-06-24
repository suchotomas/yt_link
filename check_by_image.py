import numpy as np
from api.tools import Tools as t
from api.tools import Match
from match_by_duration import MatchByDuration
import os
import cv2
from tqdm import tqdm

# export_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json'
# youtube_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json'
# workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'


matches_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_mse.pickle'
path_out = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_mse2.pickle'
workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'


class CheckMSE():
    def __init__(self, workdir, matches_path, path_out):
        self.matches = t.load_pickle(matches_path)
        self.workdir = workdir
        self.path_out = path_out

    def run(self):

        done = 0
        counter = 0
        for ida, match in tqdm(self.matches.items(), ascii=True, desc='process {} lines'.format(len(self.matches))):
            counter += 1


            try:
                if len(self.matches[ida].mse):
                    continue
            except:
                self.matches[ida].mse = []
            a_path = os.path.join(self.workdir, match.ida, 'image.png')
            a_info_path = os.path.join(self.workdir, match.ida, 'info.json')
            if not os.path.isfile(a_path) or not os.path.isfile(a_info_path):
                print('cannot read', a_path)
                continue
            A = cv2.imread(a_path)
            A_info = t.load_json(a_info_path)
            if len([ret for ret in A_info['rets'] if not ret]) > 2:
                # print(A_info['rets'])
                continue

            if len(match.diff):
                for idb in match.idb:
                    b_path = os.path.join(self.workdir, idb, 'image.png')
                    b_info_path = os.path.join(self.workdir, idb, 'info.json')
                    if not os.path.isfile(b_path) or not os.path.isfile(b_info_path):
                        print('cannot read', b_path)
                        continue
                    B = cv2.imread(b_path)
                    B_info = t.load_json(b_info_path)
                    if len([ret for ret in B_info['rets'] if not ret]) > 2:
                        # print(B_info['rets'])
                        continue

                    mse = ((A - B) ** 2).mean(axis=None)
                    match.mse.append((idb, mse))
                    done += 1

                    # diffs.append(len(match.diff))

            if counter % 100 == 0:
                print('data_saved')
                t.save_pickle(self.path_out, self.matches)
        t.save_pickle(self.path_out, self.matches)
        print('data_saved')
        print('done {}/{}'.format(done, len(self.matches)))

CheckMSE(workdir, matches_path, path_out).run()
