import cv2, time
import os
import numpy as np
from api.tools import Tools as t
import shutil

MATRIX_RESOLUTION = (9*5, 16*5)

class FileToVideoVector:
    def __init__(self, workdir):
        self.workdir = workdir

    def run(self, src, vector_path):
        
        folder_path = os.path.dirname(vector_path)
        # try:
        t.create_folder(folder_path)
        
        # tmp_video_path = os.path.join(self.workdir, dst, os.path.basename(src))
        # shutil.copy(src, tmp_video_path)
        video_vector = self.compute_vector(src)
        t.save_array(video_vector, vector_path)
        # return vector_path
        # except Exception as e:
        #     print(folder_path, e)
        #     return None
        return vector_path
    
    def compute_vector(self, src):
        cap = cv2.VideoCapture(src)
        frame_cnt = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        vector = []
        timecode = 0
        last_matrix = np.zeros((*MATRIX_RESOLUTION,3))
        timeline = np.zeros(int(frame_cnt+1), dtype=np.float64)
        t_start = time.time()
        print_step = 1000
        
        while timecode <= frame_cnt:
            timecode +=1

            if timecode %print_step == 0:
                t1 = time.time()
                duration_of_done = t1-t_start
                duration_per_frame = duration_of_done/timecode
                rest = duration_per_frame * (frame_cnt - timecode)
                comp_speed = (timecode / duration_of_done + .5) / 25
                print('[{}/{}] - {:0.2f} sec left, {:0.1f}x real-time'.format(timecode, frame_cnt, rest, comp_speed))
                
            ret, frame = cap.read()
            if not ret: 
                if timecode <= frame_cnt:
                    matrix = np.zeros((*MATRIX_RESOLUTION, 3))
                else:
                    break
            else:
                matrix = cv2.resize(frame, (MATRIX_RESOLUTION[1], MATRIX_RESOLUTION[0]))

            # timeline.append(matrix)
            timeline[timecode] = np.linalg.norm(matrix)
        cap.release()
        return timeline


