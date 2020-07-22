import time
import numpy as np
import json
from names import Names as n
import os, pickle
from tqdm import tqdm
from api.tools import Tools as t
from api.tools import Match, MatchItem
import threading
from threading import Thread, RLock

LOCK = RLock()


# DIFF_LIMIT = 1000 # = 1 sec
class MatchByDuration:
    def __init__(self, workdir, export_path, youtube_path, diff_limit, threaded=True):
        self.workdir = workdir
        self.export_path = export_path
        self.youtube_path = youtube_path
        self.diff_limit = diff_limit
        self.output_matches_path = os.path.join(self.workdir, 'matches.pickle')
        print(self.output_matches_path)
        self.thread = Thread(target=self.get_duration_lists, args=())
        self.thread.daemon = True


    def get_duration_lists(self):
        self.export_list = t.load_json(self.export_path)
        self.youtube_list = t.load_json(self.youtube_path)

        export_durations = np.zeros(len(self.export_list))
        youtube_durations = np.zeros(len(self.youtube_list))

        for idx in range(export_durations.shape[0]):
            export_durations[idx] = self.export_list[idx][n.DURATION]

        for idx in range(youtube_durations.shape[0]):
            youtube_durations[idx] = self.youtube_list[idx][n.DURATION]


        match_start_time = time.time()
        out = {}
        for idx_a in range(len(youtube_durations)):
            ida = self.youtube_list[idx_a]['dst']
            out[ida] = Match(ida)
            out[ida].adur = youtube_durations[idx_a]

        matches_list = self.match_by_duration(out,youtube_durations, export_durations)
        
        # diffs = [o.diff[-1] for _, o in out.items() if len(o.diff)]
        # print('median', np.median(diffs))
        cnt = 0
        # for _, match in out.items():
        #     if len(match.diff):
        #         cnt += 1
        # print('matched (less than 1s) {}/{} in {:.02f} sec'.format(cnt, len(out), time.time() - match_start_time))


        with open(self.output_matches_path, 'wb') as handle:
            pickle.dump(matches_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return self.output_matches_path

    def match_by_durations_multithreaded(self,out, a, b):
        ## process durations
        total_lenght = b.shape[0]
        num_of_proc = 6
        steps_1 = np.arange(0, total_lenght, total_lenght // num_of_proc)
        steps = []

        for idx in range(len(steps_1) - 1):
            if idx == len(steps_1) - 2:
                _to = total_lenght - 1
            else:
                _to = steps_1[idx + 1]
            _from = steps_1[idx]
            steps.append((_from, _to))
        thread_list = []
        for idx_b in range(len(b)):
            # Instantiates the thread
            # (i) does not make a sequence, so (i,)

            t = Thread(target=self.__fill_diff, args=(out, a, b,idx_b, self.export_list, self.youtube_list, self.diff_limit))
            # Sticks the thread in a list so that it remains accessible
            thread_list.append(t)

        # Starts threads
        for thread in thread_list:
            thread.start()

        # This blocks the calling thread until the thread whose join() method is called is terminated.
        # From http://docs.python.org/2/library/threading.html#thread-objects
        for thread in thread_list:
            thread.join()

    def match_by_duration(self,out, a, b):
        for idx_b in tqdm(range(len(b)), ascii=True, desc='process {} lines'.format(len(b))):
            self.__fill_diff(out, a,b,idx_b, self.export_list, self.youtube_list, self.diff_limit)
        return out

    @staticmethod
    def __fill_diff_in_part(out, a,b, from_to,  export_list, youtube_list, diff_limit):
        for idx_b in range(from_to[0], from_to[1]):
            # print(idx_b)
            MatchByDuration.__fill_diff(out, a, b, idx_b, export_list, youtube_list, diff_limit)

    @staticmethod
    def __fill_diff(out, a, b, idx_b, export_list, youtube_list, diff_limit):
            # print(idx_b)
            if b[idx_b] == 0:
                return
            idb = export_list[idx_b]['dst']
            for idx_a in range(len(a)):
                if a[idx_a] == 0:
                    return
                ida = youtube_list[idx_a]['dst']

                diff = abs(a[idx_a] - b[idx_b])
                if diff < diff_limit:

                    out[ida].idb_items[idb] = MatchItem(idb)
                    out[ida].idb_items[idb].diff = int(diff)
                    # while LOCK:
                        # out[ida].diff.append(diff)
                        # out[ida].idb.append(idb)
        # return out



#
export_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json'
youtube_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process_100.json'
workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'
m = MatchByDuration(export_path=export_path, youtube_path=youtube_path, workdir=workdir, diff_limit=1000)
m.get_duration_lists()