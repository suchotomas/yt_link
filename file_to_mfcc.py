import numpy as np
import time
import os, json
from api.tools import Tools as t
from api import mfcc_api
import scipy.signal
from tqdm import tqdm
import ffmpeg
from ffmpeg import Error
from timeout import timeout
import random

youtube_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json'
exports_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json'
workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'


class FileToMFCC:

    def __init__(self,workdir, sr=16000, max_length=1200):

        self.workdir = workdir
        self.sr = sr
        # self.max_length = max_length
        # self.abs_dist_path =t.create_folder(os.path.join(workdir, 'distances'))
        self.youtube_list = t.load_json(youtube_path)
        self.exports_list = t.load_json(exports_path)

    def run_all(self):
        files_to_process = self.youtube_list + self.exports_list
        random.shuffle(files_to_process)
        
        # for file in files_to_process:
        for idx in tqdm(range(len(files_to_process)), ascii=True, desc='process {} files'.format(len(files_to_process))):
            file = files_to_process[idx]
            src = file['src']
            dst = file['dst']
            self.run(src, dst)

    def run(self, src, distances_path):
        
        folder_path = os.path.dirname(distances_path)
        try:
            t.create_folder(folder_path)
            distances = self.compute_dist(src)
            if distances is None:
                return None
            t.save_array(distances, distances_path)
            return distances_path
        except Exception as e:
            print(folder_path, e)
            return None


    def extract_audio(self, filename):
            try:
                out, err = (
                    ffmpeg
                    .input(filename)
                    .output('-', format='f32le', acodec='pcm_f32le', ac=1, ar=self.sr)
                    .run(cmd='ffmpeg', capture_stdout=True, capture_stderr=True)
                )
                return np.frombuffer(out, np.float32)
            except Error as err:
                print(err.stderr)
                # raise
                return None


    def _inv_list(self, coef):
        icoef = []
        for i in range(len(coef[0])):
            icoef.append([coef[a][i] for a in range(len(coef))])

        return np.asarray(icoef)

    @timeout(120)
    def compute_dist(self, src):
        # sig, sr = mfcc_api.load_audio(src, self.sr, mono=True)
        sig = self.extract_audio(src)
        if sig is None:
            return None
        mfc_coef = mfcc_api.mfcc(sig, self.sr)
        distances = np.asarray(self._dist_flow(mfc_coef))
        return distances

    def _dist_flow(self, coef):
        # icoef = self._inv_list(coef)
        icoef = coef.T
        distances = [self._dist(icoef[a], icoef[a + 1]) for a in range(len(icoef) - 1)]
        return distances
    def _dist(self, coefs1, coefs2):
        coefs1 = coefs1[1:12]
        coefs2 = coefs2[1:12]
        return np.linalg.norm(coefs1 - coefs2)

    # def save_distances(self, distances, filename):
    #     np.save(filename, distances)

# w = FileToMFCC(workdir)
# # t0 = time.time()
# w.run_all()

# print(time.time()-t0)