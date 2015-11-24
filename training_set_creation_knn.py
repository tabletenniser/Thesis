try:
    import Image
except ImportError:
    from PIL import Image
from PIL import ImageEnhance
from sklearn import datasets, svm, metrics
import numpy as np
# import pytesseract
import time
import argparse
import os
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

TRAINING_SET_PATH = 'training_set'
TRAINING_SET_SET_PATH = 'training_set_set'
BEST_OF=7
TOP_LEFT_X=377  #362/6 for 720p, 182 for 360p
TOP_LEFT_Y=595  #590 for 720p, 295/6 for 360p
DELTA_X=24      #35 for 720p, 15/8 for 360p
DELTA_Y=24      #28 for 720p, 12/4 for 360p
# yellow scoreboard
# TOP_LEFT_X=365  #362 for 720p, 182 for 360p
# TOP_LEFT_Y=605  #590 for 720p, 295/6 for 360p
# DELTA_X=25      #35 for 720p, 15/8 for 360p
# DELTA_Y=28      #20 for 720p, 12/4 for 360p
START_FRAME=36
END_FRAME=1000

def load_digit_training_data(container_path):
    digits_new = {}
    data = []
    target = []
    folders = [f for f in sorted(os.listdir(container_path)) if os.path.isdir(os.path.join(container_path, f))]
    #print folders
    for folder in folders:
        folder_path = os.path.join(container_path, folder)
        #print folder
        documents = [os.path.join(folder_path, d) for d in sorted(os.listdir(folder_path))]
        for pic in documents:
            if not pic.endswith('png'):
                continue
            pil_im = Image.open(pic, 'r')
            data.append(np.asarray(pil_im).ravel())
            target.append(int(folder))
    digits_new['data']=data
    digits_new['target']=target
    knn_neigh = KNeighborsClassifier(n_neighbors=5)
    knn_neigh.fit(digits_new['data'][:], digits_new['target'][:])
    return knn_neigh

def valid(num):
    if num != None and num!="" and len(num)==1 or len(num)==2 and num[0]=='1':
        return True
    return False

def set_valid(num):
    if num != None and num!="" and len(num)==1 and num[0] <= '4' and num[0] >= '0':
        return True
    return False

def find_frame_range(input_dir):
    first = 0
    last = 99999
    found = False

    while first<=last and not found:
        midpoint = (first + last)//2
        filepath = os.path.join(input_dir, 'frame_%05d.png'%midpoint)
        filepath_next = os.path.join(input_dir, 'frame_%05d.png'%(midpoint+1))
        if os.path.exists(filepath) and not os.path.exists(filepath_next):
            print "START_FRAME:", 0, "\tEND_FRAME", midpoint
            return 1, midpoint-1
        else:
            if not os.path.exists(filepath):
                last = midpoint-1
            else:
                first = midpoint+1

    return 0,0

def conv_to_num(knn_neigh, im):
    # print 'dim: ', np.asarray(im).shape
    num = knn_neigh.predict(np.asarray(im).ravel())
    max_prob = np.amax(knn_neigh.predict_proba(np.asarray(im).ravel())),
    # print 'knn prob: ', max_prob[0]
    return int(num[0]), float(max_prob[0])

def find_num(knn_neigh, knn_neigh_set, input_png):
    sharpness_factor = 10.0
    brightness_factor = 10.0
    im = Image.open(input_png)
    # player1 score
    im1 = im.crop((TOP_LEFT_X, TOP_LEFT_Y, TOP_LEFT_X+DELTA_X, TOP_LEFT_Y+DELTA_Y)).convert('L')
    # enhancer = ImageEnhance.Sharpness(im1)
    # im1 = enhancer.enhance(sharpness_factor)
    # enhancer = ImageEnhance.Brightness(im1)
    # im1 = enhancer.enhance(brightness_factor)
    # player2 score
    im2 = im.crop((TOP_LEFT_X, TOP_LEFT_Y+DELTA_Y, TOP_LEFT_X+DELTA_X, TOP_LEFT_Y+2*DELTA_Y)).convert('L')
    # enhancer = ImageEnhance.Sharpness(im2)
    # im2 = enhancer.enhance(sharpness_factor)
    # enhancer = ImageEnhance.Brightness(im2)
    # im2 = enhancer.enhance(brightness_factor)
    # player1 set score
    im_set1 = im.crop((TOP_LEFT_X+DELTA_X, TOP_LEFT_Y, TOP_LEFT_X+2*DELTA_X, TOP_LEFT_Y+DELTA_Y)).convert('L')
    # enhancer = ImageEnhance.Sharpness(im_set1)
    # im_set1 = enhancer.enhance(sharpness_factor)
    # player2 set score
    im_set2 = im.crop((TOP_LEFT_X+DELTA_X, TOP_LEFT_Y+DELTA_Y, TOP_LEFT_X+2*DELTA_X, TOP_LEFT_Y+2*DELTA_Y)).convert('L')
    # enhancer = ImageEnhance.Sharpness(im_set2)
    # im_set2 = enhancer.enhance(sharpness_factor)
    # Run pytesseract
    return (conv_to_num(knn_neigh, im1),
            conv_to_num(knn_neigh, im2),
            conv_to_num(knn_neigh_set, im_set1),
            conv_to_num(knn_neigh_set, im_set2))

def main(input_dir, output_dir):
    start_time = time.time()
    # Set START_FRAME and END_FRAME
    START_FRAME, END_FRAME = find_frame_range(input_dir)

    # Actual algorithm to find the split points
    index = START_FRAME
    pt_start_frame = START_FRAME
    knn_neigh = load_digit_training_data(TRAINING_SET_PATH)
    knn_neigh_set = load_digit_training_data(TRAINING_SET_SET_PATH)
    top_player_winning_filepath = os.path.join(output_dir, 'top_player_winning_frames.txt')
    bottom_player_winning_filepath = os.path.join(output_dir, 'bottom_player_winning_frames.txt')
    top_player_winning_file=open(top_player_winning_filepath, 'w+')
    bottom_player_winning_file=open(bottom_player_winning_filepath, 'w+')
    points_top_player_win = []
    points_bottom_player_win = []
    prev_num1 = 0
    prev_num2 = 0
    input_frame_file = os.path.join(input_dir, 'frame_%05d.png'%index)
    while (os.path.exists(input_frame_file) and index<=END_FRAME):
        input_frame_file = os.path.join(input_dir, 'frame_%05d.png'%index)
        num_1, num_2, num_set1, num_set2 = find_num(knn_neigh, knn_neigh_set, input_frame_file)
        if num_1[1] < 0.9 or num_2[1] < 0.9 or num_set1[1] < 0.9 or num_set2[1] < 0.9:
            # print "index:", index, ";score_1:", num_1, ";score_2:", num_2, ";set_1:", num_set1, ";set_2:", num_set2
            pt_start_frame = index+1
            index += 1
            continue
        num_int_1 = int(num_1[0])
        num_int_2 = int(num_2[0])
        num_int_set1 = int(num_set1[0])
        num_int_set2 = int(num_set2[0])
        # if a point change occurs at this particular frame.
        sets_sum=num_int_set1+num_int_set2
        if (index - pt_start_frame > 4 and (num_int_1 != prev_num1 or num_int_2 != prev_num2)):
            if ((num_int_1 > prev_num1 and num_int_2 == prev_num2 and
                    sets_sum < BEST_OF-1 and (sets_sum)%2==0) or
                    (num_int_1 == prev_num1 and num_int_2 > prev_num2 and
                    sets_sum < BEST_OF-1 and (sets_sum)%2==1)):
                points_top_player_win.append((pt_start_frame, index))
                output=str(pt_start_frame)+":"+str(index)
                print "write to top_player_winning_frames: ", output
                top_player_winning_file.write(output+'\n')
            elif ((num_int_1 > prev_num1 and num_int_2 == prev_num2 and
                    sets_sum < BEST_OF-1 and (sets_sum)%2==1) or
                    (num_int_1 == prev_num1 and num_int_2 > prev_num2 and
                    sets_sum < BEST_OF-1 and (sets_sum)%2==0)):
                points_bottom_player_win.append((pt_start_frame, index))
                output=str(pt_start_frame)+":"+str(index)
                print "write to bottom_player_winning_frames: ", output
                bottom_player_winning_file.write(output+'\n')
            pt_start_frame = index
            prev_num1 = num_int_1
            prev_num2 = num_int_2
            # print "VALIDATION_TEST_PASS - index:", index, ";score_1:", num_1, ";score_2:", num_2, ";set_1:", num_set1, ";set_2:", num_set2
        index+=1
    top_player_winning_file.close()
    bottom_player_winning_file.close()
    print "TRAINING_SET_CREATION.PY TAKES:"+str(time.time()-start_time)+" seconds"
    return

if __name__=='__main__':
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help='Path to the directory containing .png frames from the video')
    parser.add_argument("output_dir", type=str, help='Training set storage directory. Contain two folders, one for points where the top player wins, the other one for points where the bottom player wins')
    args = parser.parse_args()
    args.input_dir = os.path.abspath(args.input_dir)
    args.output_dir = os.path.abspath(args.output_dir)

