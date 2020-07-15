import subprocess
import shlex
import json
import os
import pickle
class Tools:

    # @staticmethod
    # def get_ffprobe(file_path):
    #
    #     cmd = 'ffprobe -v quiet -print_format json -show_format -show_streams "' + file_path + '"'
    #     cmd = 'ffmpeg -y -i "'+file_path+'" -map 0:v:0 -c copy -progress - -f null - '
    #     cmd =' ffmpeg -y -i "'+file_path+'"   grep Duration'
    #     cmd = 'ffmpeg -i /mnt/data/palpatine/SAMPLES/YT_LINK/REF/HC6C3HxnBXQ.mkv -map 0:v:0 -c copy -f null -'
    #
    #     args = shlex.split(cmd)
    #     ffprobe_output = subprocess.check_output(args).decode('utf-8')
    #
    #     ffprobe_json = json.loads(ffprobe_output)
    #     ffprobe_streams = ffprobe_json['streams']
    #     ffprobe_final = {}
    #     for d in ffprobe_streams:
    #         [ffprobe_final.update({d['codec_type'] + ':' + str(key): value}) for key, value in d.items() if
    #          'codec_type' in d]
    #     return ffprobe_final

    @staticmethod
    def get_duration(path):
        cmd = 'ffprobe -v quiet -show_entries format=duration -hide_banner -of default=noprint_wrappers=1:nokey=1 "' + path +'"'
        args = shlex.split(cmd)
        return float(subprocess.check_output(args).decode('utf-8'))

    @staticmethod
    def create_folder(folder_path):
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            return folder_path

    @staticmethod
    def load_json(path):
        if not os.path.isfile(path):
            return None
        with open(path, 'r') as f:
            data  = json.load(f)
        return data

    @staticmethod
    def save_json(path, data):
        with open(path, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)

    @staticmethod
    def load_pickle(path):
        # open a file, where you stored the pickled data
        file = open(path, 'rb')
        # dump information to that file
        data = pickle.load(file)

        # close the file
        file.close()
        return data

    @staticmethod
    def save_pickle(path, data):
        with open(path, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def get_offset(peak,dist1, dist2, dur1, dur2):
        full_dur = (dur1 + dur2)
        return (((peak) / (len(dist1)+len(dist2)-1)) * full_dur) - dur2

class Match:
    def __init__(self, ida):
        self.ida = ida
        self.idb = []
        self.diff = []
        self.adur = None
        self.mse = None

# path = '/mnt/data/palpatine/SAMPLES/YT_LINK/REF/HC6C3HxnBXQ.mkv'
# # cmd = 'ffmpeg -i /mnt/data/palpatine/SAMPLES/YT_LINK/REF/HC6C3HxnBXQ.mkv -map 0:v:0 -c copy -f null -'
#
# args = shlex.split(cmd)
# ffprobe_output = subprocess.check_output(args).decode('utf-8')
# # ff = Tools.get_ffprobe(path)
#
# print(ffprobe_output)