import cv2
import os
import numpy as np
from api.tools import Tools as t
import shutil
class FileToVideoVector:
    def __init__(self, workdir):
        self.workdir = workdir

    def run(self, src, dst):
        filename = 'video_vector.npy'
        vector_path = os.path.join(self.workdir, dst, filename)
        if os.path.isfile(vector_path):
            return vector_path
        folder_path = os.path.dirname(vector_path)
        # try:
        t.create_folder(folder_path)
        
        tmp_video_path = os.path.join(self.workdir, dst, os.path.basename(src))
        shutil.copy(src, tmp_video_path)
        video_vector = self.compute_vector(tmp_video_path)
        # self.save_distances(video_vector, vector_path)
        # return vector_path
        # except Exception as e:
        #     print(folder_path, e)
        #     return None
        return vector_path
    
    def compute_vector(self, src):
        cap = cv2.VideoCapture(src)

        vector = []
        timecode = 0
        while True:
            timecode +=1

            if timecode %1000 == 0:
                print(timecode)
            ret, frame = cap.read()
            if not ret: break
        return None


