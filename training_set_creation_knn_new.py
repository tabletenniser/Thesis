try:
    import Image
except ImportError:
    from PIL import Image
from PIL import ImageEnhance
import PIL.ImageOps
from sklearn import datasets, svm, metrics
import numpy as np
# import pytesseract
import time
import argparse
import os
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
import logging

# TRAINING_SET_PATH = 'training_set'
# TRAINING_SET_SET_PATH = 'training_set_set'
TRAINING_SET_PATH = 'training_set_20_by_20_grey'
# TRAINING_SET_SET_PATH = 'training_set_18_by_18_grey'
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
WIDTH = 20
HEIGHT = 20

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
    knn_neigh = KNeighborsClassifier(n_neighbors=3)
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
            logging.info("binary search result - START_FRAME: %d\tEND_FRAME: %d", 0, midpoint)
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

def invert_if_black_on_white(im):
    im_array = np.asarray(im)
    im_array_mean = im_array.mean()
    if im_array[0][0] < im_array_mean and im_array[-1][-1] < im_array_mean and im_array[0][-1] < im_array_mean and im_array[-1][0] < im_array_mean:
        return im
    return PIL.ImageOps.invert(im)

def normalize_and_invert_if_black_on_white(im, is_score_black_on_white):
    im_array = np.asarray(im)
    if is_score_black_on_white:
        im = PIL.ImageOps.invert(im)
    im_array_min = im_array.min()
    im_array_max = im_array.max()
    if im_array_max-im_array_min != 0:
        im = im.point(lambda x: 255*(x-im_array_min)/(im_array_max - im_array_min) , 'L')
    return im

def normalize(im):
    im_array = np.asarray(im)
    im_array_min = im_array.min()
    im_array_max = im_array.max()
    if im_array_max-im_array_min != 0:
        im = im.point(lambda x: 255*(x-im_array_min)/(im_array_max - im_array_min) , 'L')
    return im

def find_num(score_dir, index, knn_neigh, input_png, top_left_x, top_left_set_x, top_left_y, top_left_second_y, delta_x, delta_y, is_score_black_on_white):
    sharpness_factor = 10.0
    brightness_factor = 10.0
    bw_threshold = 0.3
    im = Image.open(input_png)
    # player1 score
    im1 = im.crop((top_left_x, top_left_y, top_left_x+delta_x, top_left_y+delta_y)).convert('L')
    # im1_array = np.asarray(im1)
    # im1_array_mean = im1_array.mean()
    # im1 = im1.point(lambda x: 0 if x < im1_array_mean else 255, '1')
    im1 = im1.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
    im1 = normalize_and_invert_if_black_on_white(im1, is_score_black_on_white)
    im1.save(os.path.join(score_dir, "frame%05d_p1.png" % index))
    # enhancer = ImageEnhance.Sharpness(im1)
    # im1 = enhancer.enhance(sharpness_factor)
    # enhancer = ImageEnhance.Brightness(im1)
    # im1 = enhancer.enhance(brightness_factor)
    # player2 score
    im2 = im.crop((top_left_x, top_left_second_y, top_left_x+delta_x, top_left_second_y+delta_y)).convert('L')
    im2 = im2.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
    im2 = normalize_and_invert_if_black_on_white(im2, is_score_black_on_white)
    im2.save(os.path.join(score_dir, "frame%05d_p2.png" % index))
    # enhancer = ImageEnhance.Sharpness(im2)
    # im2 = enhancer.enhance(sharpness_factor)
    # enhancer = ImageEnhance.Brightness(im2)
    # im2 = enhancer.enhance(brightness_factor)
    # player1 set score
    im_set1 = im.crop((top_left_set_x, top_left_y, top_left_set_x+delta_x, top_left_y+delta_y)).convert('L')
    # im_set1_array = np.asarray(im_set1)
    # im_set1_array_mean = im_set1_array.mean()
    # im_set1 = im_set1.point(lambda x: 0 if x < im_set1_array_mean else 255, '1')
    im_set1 = im_set1.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
    im_set1 = normalize(im_set1)
    im_set1.save(os.path.join(score_dir, "frame%05d_s1.png" % index))
    # enhancer = ImageEnhance.Sharpness(im_set1)
    # im_set1 = enhancer.enhance(sharpness_factor)
    # player2 set score
    im_set2 = im.crop((top_left_set_x, top_left_second_y, top_left_set_x+delta_x, top_left_second_y+delta_y)).convert('L')
    im_set2 = im_set2.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
    im_set2 = normalize(im_set2)
    im_set2.save(os.path.join(score_dir, "frame%05d_s2.png" % index))
    # enhancer = ImageEnhance.Sharpness(im_set2)
    # im_set2 = enhancer.enhance(sharpness_factor)
    return (conv_to_num(knn_neigh, im1),
            conv_to_num(knn_neigh, im2),
            conv_to_num(knn_neigh, im_set1),
            conv_to_num(knn_neigh, im_set2))

# writes classified frames in .txt format to output_dir; cropped score images to score_dir
def main(input_dir, score_dir, output_dir, top_left_x, top_left_set_x, top_left_y, top_left_second_y, delta_x, delta_y, is_score_black_on_white, is_top_player_top, debug=False):
    start_time = time.time()
    # Set START_FRAME and END_FRAME
    START_FRAME, END_FRAME = find_frame_range(input_dir)

    # Actual algorithm to find the split points
    index = START_FRAME
    pt_start_frame = START_FRAME
    knn_neigh = load_digit_training_data(TRAINING_SET_PATH)
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
        num_1, num_2, num_set1, num_set2 = find_num(score_dir, index, knn_neigh, input_frame_file, top_left_x, top_left_set_x, top_left_y, top_left_second_y, delta_x, delta_y, is_score_black_on_white)
        logging.debug("index:%d; score_1:%s; score_2:%s; set_1:%s; set_2:%s", index, str(num_1), str(num_2), str(num_set1), str(num_set2))
        if num_1[1] < 0.9 or num_2[1] < 0.9 or num_set1[1] < 0.9 or num_set2[1] < 0.9 or num_set1[0] > 3 or num_set2[0] > 3:
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
                if is_top_player_top == True:
                    points_top_player_win.append((pt_start_frame, index))
                    output=str(pt_start_frame)+":"+str(index)
                    logging.info("write to top_player_winning_frames: %s", output)
                    top_player_winning_file.write(output+'\n')
                else:
                    points_bottom_player_win.append((pt_start_frame, index))
                    output=str(pt_start_frame)+":"+str(index)
                    logging.info("write to bottom_player_winning_frames: %s", output)
                    bottom_player_winning_file.write(output+'\n')
            elif ((num_int_1 > prev_num1 and num_int_2 == prev_num2 and
                    sets_sum < BEST_OF-1 and (sets_sum)%2==1) or
                    (num_int_1 == prev_num1 and num_int_2 > prev_num2 and
                    sets_sum < BEST_OF-1 and (sets_sum)%2==0)):
                if is_top_player_top == True:
                    points_bottom_player_win.append((pt_start_frame, index))
                    output=str(pt_start_frame)+":"+str(index)
                    logging.info("write to bottom_player_winning_frames: %s", output)
                    bottom_player_winning_file.write(output+'\n')
                else:
                    points_top_player_win.append((pt_start_frame, index))
                    output=str(pt_start_frame)+":"+str(index)
                    logging.info("write to top_player_winning_frames: %s", output)
                    top_player_winning_file.write(output+'\n')
            pt_start_frame = index
            prev_num1 = num_int_1
            prev_num2 = num_int_2
            logging.debug("VALIDATION_TEST_PASS - index:%d; score_1:%d; score_2:%d; set_1:%d; set_2:%d", index, num_1[0], num_2[0], num_set1[0], num_set2[0])
        index+=1
    top_player_winning_file.close()
    bottom_player_winning_file.close()
    logging.info("TRAINING_SET_CREATION.PY TAKES:"+str(time.time()-start_time)+" seconds")
    return

if __name__=='__main__':
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help='Path to the directory containing .png frames from the video')
    parser.add_argument("output_dir", type=str, help='Training set storage directory. Contain two folders, one for points where the top player wins, the other one for points where the bottom player wins')
    args = parser.parse_args()
    args.input_dir = os.path.abspath(args.input_dir)
    args.output_dir = os.path.abspath(args.output_dir)

