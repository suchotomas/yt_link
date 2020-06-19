import time
import numpy as np
import json
from names import Names as n
def load_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data



def save_json(path, data):
    with open(path, 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

class MatchByDuration:



    @staticmethod
    def get_duration_lists(json_path):
        data = load_json(json_path)

        youtube_list = []
        export_list = []
        for record in data:
            if record[n.DST].split('/', 1)[0] == n.EXPORT:



    @staticmethod
    def match_by_duration(self, a, b):
        match_start_time = time.time()
        out = {}
        for ida in range(len(a)):
            out[ida] = Match(ida)
            out[ida].adur = a[ida]

        for idb in range(len(b)):
            if b[idb] == 0:
                continue
            for ida in range(len(a)):
                if a[ida] == 0:
                    continue
                diff = abs(a[ida] - b[idb])
                if not len(out[ida].diff) or diff < out[ida].diff[-1]:
                    out[ida].diff.append(diff)
                    out[ida].idb.append(idb)
                    out[ida].bdur = b[idb]

        diffs = [o.diff[-1] for _, o in out.items() if len(o.diff)]
        print('median', np.median(diffs))
        cnt = 0
        for _, match in out.items():
            if not len(match.diff):
                continue
            if match.diff[-1] < 1000:
                cnt += 1
        print('matched (less than 1s) {}/{} in {:.02f} sec'.format(cnt, len(out), time.time() - match_start_time))
        return out


class Match:
    def __init__(self, ida):
        self.ida = ida
        self.idb = []
        self.diff = []
        self.adur = None
        self.bdur = None

