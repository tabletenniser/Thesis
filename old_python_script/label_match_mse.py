import math, operator
import argparse
import time
import os
from skimage.measure import structural_similarity as ssim
from skimage import color
from skimage import io
from PIL import Image

# SHORT_VIDEO_STARTING_FRAME = 1
SHORT_VIDEO_STARTING_FRAME = 50
# FULL_VIDEO_STARTING_FRAME = 896
FULL_VIDEO_STARTING_FRAME = 1073
# FRAME_NUM_OFFSET = 895
FRAME_NUM_OFFSET = FULL_VIDEO_STARTING_FRAME - SHORT_VIDEO_STARTING_FRAME
WINDOW_SIZE = 5
NUM_OF_FRAMES = 150       # Check the next 250 frames to find the maximum offset
match = []              # match[i-SHORT_VIDEO_STARTING_FRAME] = corresponding index in full video

def compute_offset(args, s_index, f_index):
    short_video_file = os.path.join(args.short_video_dir, 'frame_%05d.jpg'%s_index)
    # short_video_image = io.imread(short_video_file)
    min_score = 9999999
    count = 0
    while (count < NUM_OF_FRAMES):
        full_video_file = os.path.join(args.full_video_dir, 'frame_%05d.jpg'%(f_index+count))
        if not os.path.exists(full_video_file):
            break
        # full_video_image = io.imread(full_video_file)
        image1 = Image.open(short_video_file)
        image2 = Image.open(full_video_file)
        h1 = image1.histogram()
        h2 = image2.histogram()
        score = math.sqrt(reduce(operator.add, map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
        if score < min_score:
            min_score = score
            max_f_index = f_index+count
        count+=1
    return max_f_index-s_index

if __name__=='__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("short_video_dir", type=str, help='Path to the directory containing frames from the short video')
    parser.add_argument("full_video_dir", type=str, help='Path to the directory containing frames from the full video')
    args = parser.parse_args()
    args.short_video_dir = os.path.abspath(args.short_video_dir)
    args.full_video_dir = os.path.abspath(args.full_video_dir)

    s_index = SHORT_VIDEO_STARTING_FRAME
    f_index = FULL_VIDEO_STARTING_FRAME
    cur_offset = FRAME_NUM_OFFSET
    short_video_file = os.path.join(args.short_video_dir, 'frame_%05d.jpg'%s_index)
    print short_video_file
    max_offset_count = 0
    min_over_offset = 99999999
    while (os.path.exists(short_video_file) and (s_index - SHORT_VIDEO_STARTING_FRAME )<40):
        max_offset = compute_offset(args, s_index, s_index+cur_offset)
        print "Offset for s_index "+str(s_index)+" is "+str(max_offset)+"."
        match.append(max_offset)
        if max_offset > cur_offset+5:
            if max_offset_count == 5:
                cur_offset = min_over_offset
                max_offset_count = 0
                min_over_offset = 99999999
            else:
                max_offset_count += 1
                if max_offset < min_over_offset:
                    min_over_offset = max_offset
        s_index+=1
    print "="*10+"BELOW IS THE FRAME MATCHING"+"="*10
    for i in xrange(len(match)):
        print '%d\t%d'%(i+SHORT_VIDEO_STARTING_FRAME, i+SHORT_VIDEO_STARTING_FRAME+match[i])

    print "TOTAL EXECUTION TIME:"+str(time.time()-start_time)+" seconds"
