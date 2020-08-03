# from __future__ import print_function, division
# import time
# import librosa
# import librosa.display
# from pylab import *
import time
# from content_align.scripts.dtw import dtw
# from numpy.linalg import norm
# import ffmpeg
import numpy as np
# import matplotlib.pyplot as plt
import scipy
from scipy import signal
from operator import itemgetter
# from content_loader.scripts import mfcc_api
# from palpatine.database import Database
# from pymediainfo import MediaInfo
import os
# import exiftool
# et = exiftool.ExifTool()
# from scipy.signal import filtfilt
input_dir = "/mnt/data/palpatine/sync/minerva/SOURCE/cam1/"
output_dir = "/mnt/data/palpatine/sync/minerva/SOURCE/cam1_audio/"

'''
save wav to separated CH: ffmpeg -i stereo.wav -map_channel 0.0.0 left.wav -map_channel 0.0.1 right.wav
loading: 7.0355963706970215 s
2x mfcc: 0.301804780960083 s
dtw: 215.60368132591248 s
dist = 99.17

groupovani video podle slozek -> podle abecedy:
    v databazi ulozit soubory z jedne slozky jako jednu grupu..? 

'''
class OffsetCalc:
    def __init__(self, win_size=40, plot=False):
        self.win_size = win_size
        self.plot = plot

    def calculate(self, dist1_path, dur1, dist2_path, dur2, plot=False, plot_done=False):
        t0 = time.time()
        self.dist1_path = dist1_path
        self.dist2_path = dist2_path
        self.lowest_score = 1.9 # peak must be higher than median of the signal * the coeficient
        self.peak_value_limit = 300000 # correlated peak must be higher than this value
        reverse_offset = False
        dist1 = np.load(dist1_path)
        dist2 = np.load(dist2_path)
        corr_len = len(dist1)+len(dist2)-1
        dur_len = dur1+dur2
    
        corr =  self.correlate(dist1, dist2)
        # print('len corr = ',len(corr))
        # print('len dist1 + dist2', (len(dist1)+len(dist2)))
        # #
        # # Logger.pr('find peak by windowing with window size {}'.format(self.win_size))
        # if plot:
        #     print()
        # if self.plot or plot:
        #     self.plot_all(dist1, dist2, corr, diff_array)
        peak, score, diff_array = self.find_peak(corr, self.win_size)
        # print('peak, score', peak, score)
        # offset_in_samples, score = self._correlate_in_segmets(dist1, dist2)

        # Logger.pr('peak at {} with {}'.format(peak, corr[peak]))
        if peak is None:
            return None, None

        offset = self.get_offset(peak, dist1, dist2, dur1, dur2)
        # offset = offset_in_samples / corr_len * dur_len


        # Logger.pr('offset: {}'.format(offset))
        # Logger.pr('computation time: {}'.format(time.time()-t0))

        # if plot_done:
        #     self.plot_all(dist1, dist2, corr, diff_array)



        return offset, score

    def _correlate_in_segmets(self, dist1, dist2):
        ref, segments, splitters, reverse_offset = self._get_inputs(dist1, dist2)

        peak_correction = 0
        offsets = []
        for idx, segment in enumerate(segments):
            peak, score = self._get_peak_from_pair(ref, segment)
            if peak is not None:
                peak += peak_correction
                offset = peak - len(ref)
                if reverse_offset:
                    offset = - offset
                offsets.append((idx, offset,score))
            peak_correction += segment.size


        if len(offsets) == 0:
            return None, None
        print(offsets)
        idx, best_offset, best_score = sorted(offsets, key=itemgetter(2), reverse=True)[0]
        return best_offset, best_score

    def _get_peak_from_pair(self, dist1, dist2):
        corr = self.correlate(dist1, dist2)

        # Logger.pr('find peak by windowing with window size {}'.format(self.win_size))
        peak, score, diff_array = self.find_peak(corr, self.win_size)

        return peak, score


    def _get_inputs(self, dist1, dist2):
        '''
        longer distance is segmented by length of shorter one. Each segment is compared to shorter one

        :param dist1:
        :param dist2:
        :return: out1, segmented out2, if distances switched

        '''
        dist1_len = len(dist1)
        dist2_len = len(dist2)
        if dist1_len > dist2_len:
            reversed_order = True
        else:
            reversed_order = False

        if not reversed_order:
            ref = dist1
            segmented =dist2
            splitters = self._get_splitters(dist2, len(dist1))
        else:
            ref = dist2
            segmented = dist1
            splitters = self._get_splitters(dist1, len(dist2))
        segments = np.split(segmented, splitters)

        return ref, segments, splitters, reversed_order

    @staticmethod
    def _get_splitters(dist, segment_length):
        whole_len = len(dist)
        count = whole_len // segment_length # the last segment can be up to 2 * higher
        splitters = [segment_length * idx for idx in range(count) if idx !=0]
        return splitters

    def correlate(self,distances1, distances2):
        return scipy.signal.correlate(distances1, distances2)

    def find_peak(self,corr, win_size):


        diff_array = np.zeros(len(corr), dtype=int)
        step = int(win_size / 2)
        for x in range(0, len(corr) - win_size, step):
            local_peak_idx = np.argmax(corr[x:x + win_size]) + x

            ab = (corr[x] + corr[x + win_size]) / 2

            diff_corr_ab = abs(corr[local_peak_idx] - ab)

            diff_array[local_peak_idx] = diff_corr_ab

        nonzero_diff = []
        local_peaks_idx = np.nonzero(diff_array)

        for local_peak_idx in local_peaks_idx[0]:
            nonzero_diff.append(diff_array[local_peak_idx])


        sorted_diff_array = np.argsort(diff_array)
        last5 = sorted_diff_array[-6:-1]

        peak = sorted_diff_array[-1]
        second_peak = sorted_diff_array[-2]
        # if echo < range of 5 values, skip that and use other value as second one
        for value in reversed(last5):
            if abs(peak-value)>4:
                second_peak = value
                break

        peak_value = diff_array[peak]
        second_value = diff_array[second_peak]
        score = peak_value/second_value
        if score < self.lowest_score or peak_value < self.peak_value_limit:
            return None,None, None

        return peak, score, diff_array


    def get_offset(self,peak,dist1, dist2, dur1, dur2):
        full_dur = (dur1 + dur2)
        return (((peak) / (len(dist1)+len(dist2)-1)) * full_dur) - dur2

    def plot_all(self,distances1,distances2,corr,diff_array):
        Logger.pr('PLOT: {} vs. {}'.format(os.path.basename(self.dist1_path), os.path.basename(self.dist2_path)))
        plt.subplot(411)
        plt.plot(range(len(distances1)), distances1, label=self.dist1_path)
        plt.subplot(412)
        plt.plot(range(len(distances2)), distances2, label=self.dist2_path)
        plt.subplot(413)
        plt.plot(range(len(corr)), corr, label='Correlation')
        if diff_array is not None:
            plt.subplot(414)
            plt.plot(range(len(diff_array)), diff_array, label='Local peaks')

        plt.show()

# if __name__ == "__main__": main()
