import os, time, datetime, argparse
def read_event(dir):

    counter = 0
    total_cnt = 0
    for root, dirs, files in os.walk(dir):
        for name in files:
            if name == 'run.log':
                filename = os.path.join(root, name)
                print(filename)
            # modified_time = os.path.getmtime(filename)
            # if modified_time > from_time:
            #     # print(filename, time.ctime(modified_time))
            #     counter += 1
            total_cnt += 1
    return counter, total_cnt

dir1 = '/jabba/incoming/2020_07_12-18-international_conference_on_machine_learning_2020-2635/PROJECT'
dir2 ='/jabba/incoming/2020_07_05-10-acl_2020-2465/PROJECT'
dir3 = '/jabba/incoming/2020_08_26-28-the_23rd_international_conference_on_artificial_intelligence_and-2631/PROJECT'
dirs = [dir1, dir2, dir3]



counter = 0
total_counter = 0
for dir in dirs:
    event_cnt, total_cnt = read_event(dir)
    counter += event_cnt
    total_counter += total_cnt
    print(event_cnt, dir)
print('in total:{}/{}'.format(counter, total_counter))