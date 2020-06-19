import os
import time
import json
main_images = '/mnt/data/palpatine/SAMPLES/YT_LINK/REF/main_images'
second_images = '/mnt/data/palpatine/SAMPLES/YT_LINK/REF/second_images'
idx = 0
mse_list = []
t_start = time.time()
correct = 0
uncorrect = 0
while idx < 4000:

    a = '{}/{}.png'.format(main_images, idx)
    b = '{}/{}.png'.format(second_images, idx)
    ai = '{}/{}.json'.format(main_images, idx)
    bi = '{}/{}.json'.format(second_images, idx)
    if False not in [os.path.isfile(a), os.path.isfile(b),os.path.isfile(ai), os.path.isfile(bi)]:
        with open(ai, 'r') as f:
            a_info = json.load(f)
        with open(bi, 'r') as f:
            b_info = json.load(f)

        A = cv2.imread(a)
        B = cv2.imread(b)
        mse = ((A - B) ** 2).mean(axis=None)
        mse_list.append((idx, mse))
        dur_diff = abs(a_info['duration'] - b_info['duration'])
        print(idx, mse,dur_diff)
        if mse > 30 and dur_diff > 1000:
            uncorrect +=1
        else:
            correct += 1

    idx +=1

mse_list= sorted(mse_list, key=lambda x: x[1])
print('max', mse_list[-1])
print('min', mse_list[0])
print('median', mse_list[len(mse_list)//2])
print('correct', correct)
print('uncorrect', uncorrect)
print('whole len', idx)
print('whole time', time.time()-t_start)

# mse = ((A - B)**2).mean(axis=ax)

