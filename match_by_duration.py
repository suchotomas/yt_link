import time
import numpy as np
import json
from names import Names as n
import os, pickle
from tqdm import tqdm
from api.tools import Tools as t
from api.tools import Match

DIFF_LIMIT = 100 # = 1 sec
class MatchByDuration:
    def __init__(self, workdir, export_path, youtube_path):
        self.workdir = workdir
        self.export_path = export_path
        self.youtube_path = youtube_path
        self.output_matches_path = os.path.join(self.workdir, 'matches.pickle')
        print(self.output_matches_path)


    def get_duration_lists(self):
        self.export_list = t.load_json(self.export_path)
        self.youtube_list = t.load_json(self.youtube_path)

        export_durations = np.zeros(len(self.export_list))
        youtube_durations = np.zeros(len(self.youtube_list))

        for idx in range(export_durations.shape[0]):
            export_durations[idx] = self.export_list[idx][n.DURATION]

        for idx in range(youtube_durations.shape[0]):
            youtube_durations[idx] = self.youtube_list[idx][n.DURATION]

        matches_list = self.match_by_duration(youtube_durations, export_durations)
        
        
        with open(self.output_matches_path, 'wb') as handle:
            pickle.dump(matches_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return self.output_matches_path



    def match_by_duration(self, a, b):
        match_start_time = time.time()
        out = {}
        for idx_a in range(len(a)):
            ida = self.youtube_list[idx_a]['dst']
            out[ida] = Match(ida)
            out[ida].adur = a[idx_a]

        # for idb in range(len(b)):
        for idx_b in tqdm(range(len(b)), ascii=True, desc='process {} lines'.format(len(b))):
            if b[idx_b] == 0:
                continue
            idb = self.export_list[idx_b]['dst']
            for idx_a in range(len(a)):
                if a[idx_a] == 0:
                    continue
                ida = self.youtube_list[idx_a]['dst']

                diff = abs(a[idx_a] - b[idx_b])
                if diff < DIFF_LIMIT:
                    out[ida].diff.append(diff)
                    out[ida].idb.append(idb)
                    
        # for ida, match in out.items():
        #     print('{}->{}: {}'.format(ida, match.idb[-1], match.diff[-1]))

        diffs = [o.diff[-1] for _, o in out.items() if len(o.diff)]
        print('median', np.median(diffs))
        cnt = 0
        for _, match in out.items():
            if len(match.diff):
                cnt += 1
        print('matched (less than 1s) {}/{} in {:.02f} sec'.format(cnt, len(out), time.time() - match_start_time))
        return out





# export_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json'
# youtube_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json'
# workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'
# m = MatchByDuration(export_path=export_path, youtube_path=youtube_path, workdir=workdir)
# m.get_duration_lists()