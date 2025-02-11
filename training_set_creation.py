try:
    import Image
except ImportError:
    from PIL import Image
from PIL import ImageEnhance
import PIL.ImageOps
import pytesseract
import time
import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import logging


BEST_OF=7
# TOP_LEFT_X=377  #362/6 for 720p, 182 for 360p
# TOP_LEFT_Y=595  #590 for 720p, 295/6 for 360p
# DELTA_X=24      #35 for 720p, 15/8 for 360p
# DELTA_Y=24      #28 for 720p, 12/4 for 360p
# long scoreboard
# TOP_LEFT_X=505
# TOP_LEFT_Y=615
# TOP_LEFT_SET_X=458
# DELTA_X=40
# DELTA_Y=40
# yellow scoreboard
TOP_LEFT_X=365  #362 for 720p, 182 for 360p
TOP_LEFT_Y=605  #590 for 720p, 295/6 for 360p
TOP_LEFT_SET_X=390
DELTA_X=25      #35 for 720p, 15/8 for 360p
DELTA_Y=28      #20 for 720p, 12/4 for 360p
START_FRAME=36
END_FRAME=1000

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

def find_num(score_dir, index, input_png, top_left_x, top_left_set_x, top_left_y, delta_x, delta_y):
    sharpness_factor = 1.0
    brightness_factor = 1.0
    #bw_threshold = 0.3
    im = Image.open(input_png)
    # player1 score
    im1 = im.crop((top_left_x, top_left_y, top_left_x+delta_x, top_left_y+delta_y)).convert('L')
    im1_array = np.asarray(im1)
    im1_array_mean = im1_array.mean()
    im1 = im1.point(lambda x: 0 if x < im1_array_mean else 255, '1')
    # im1 = PIL.ImageOps.invert(im1)
    #im_max=np.amax(np.asarray(im1))
    #im_min=np.amin(np.asarray(im1))
    #im1 = im1.point(lambda x: 0 if x<((im_max-im_min)*bw_threshold+im_min) else 255, '1')
    # enhancer = ImageEnhance.Sharpness(im1)
    # im1 = enhancer.enhance(sharpness_factor)
    # enhancer = ImageEnhance.Brightness(im1)
    # im1 = enhancer.enhance(brightness_factor)
    im1.save(os.path.join(score_dir, "frame%05d_p1.jpg" % index))
    # player2 score
    im2 = im.crop((top_left_x, top_left_y+delta_y, top_left_x+delta_x, top_left_y+2*delta_y)).convert('L')
    # im2 = PIL.ImageOps.invert(im2)
    # enhancer = ImageEnhance.Sharpness(im2)
    # im2 = enhancer.enhance(sharpness_factor)
    # enhancer = ImageEnhance.Brightness(im2)
    # # im2 = enhancer.enhance(brightness_factor)
    # im_max=np.amax(np.asarray(im2))
    # im_min=np.amin(np.asarray(im2))
    # im2 = im2.point(lambda x: 0 if x<((im_max-im_min)*bw_threshold+im_min) else 255, '1')
    im2.save(os.path.join(score_dir, "frame%05d_p2.jpg" % index))
    # player1 set score
    im_set1 = im.crop((top_left_set_x, top_left_y, top_left_set_x+delta_x, top_left_y+delta_y)).convert('L')
    # enhancer = ImageEnhance.Sharpness(im_set1)
    # # im_set1 = enhancer.enhance(sharpness_factor)
    # im_max=np.amax(np.asarray(im_set1))
    # im_min=np.amin(np.asarray(im_set1))
    # im_set1 = im_set1.point(lambda x: 255 if x<(im_max-(im_max-im_min)*(bw_threshold)) else 0, '1')
    im_set1.save(os.path.join(score_dir, "frame%05d_s1.jpg" % index))
    # player2 set score
    im_set2 = im.crop((top_left_set_x, top_left_y+delta_y, top_left_set_x+delta_x, top_left_y+2*delta_y)).convert('L')
    # enhancer = ImageEnhance.Sharpness(im_set2)
    # # im_set2 = enhancer.enhance(sharpness_factor)
    # im_max=np.amax(np.asarray(im_set2))
    # im_min=np.amin(np.asarray(im_set2))
    # im_set2 = im_set2.point(lambda x: 255 if x<(im_max-(im_max-im_min)*(bw_threshold)) else 0, '1')
    im_set2.save(os.path.join(score_dir, "frame%05d_s2.jpg" % index))
    # Run pytesseract
    CONF = '-psm 6 digits'
    return (pytesseract.image_to_string(im1, config=CONF), pytesseract.image_to_string(im2, config=CONF), pytesseract.image_to_string(im_set1, config=CONF), pytesseract.image_to_string(im_set2, config=CONF))

def main(input_dir, score_dir, output_dir, top_left_x, top_left_set_x, top_left_y, delta_x, delta_y, is_top_player_top, debug=False):
    start_time = time.time()
    # Set START_FRAME and END_FRAME
    START_FRAME, END_FRAME = find_frame_range(input_dir)

    # Actual algorithm to find the split points
    index = START_FRAME
    pt_start_frame = START_FRAME
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
        num_1,num_2, num_set1, num_set2 = find_num(score_dir, index, input_frame_file, top_left_x, top_left_set_x, top_left_y, delta_x, delta_y)
        # num_1 = num_1.strip()
        # num_2 = num_2.strip()
        # num_set1 = num_set1.strip()
        # num_set2 = num_set2.strip()
        try:
            if valid(num_1) and valid(num_2) and set_valid(num_set1) and set_valid(num_set2):
                num_int_1 = int(num_1)
                num_int_2 = int(num_2)
                num_int_set1 = int(num_set1)
                num_int_set2 = int(num_set2)
                # if a point change occurs at this particular frame.
                sets_sum=num_int_set1+num_int_set2
                if index-pt_start_frame > 5 and (num_int_1 != prev_num1 or num_int_2 != prev_num2):
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
            else:
                pt_start_frame = index+1
        except ValueError:
            pt_start_frame = index+1
            pass
        logging.debug("index:%d; score_1:%s; score_2:%s; set_1:%s; set_2:%s", index, num_1, num_2, num_set1, num_set2)
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

