try:
    import Image
except ImportError:
    from PIL import Image
# from PIL import ImageEnhance
from sklearn import datasets, svm, metrics
import pylab as pl
import numpy as np
# import pytesseract
import time
import argparse
import os
import matplotlib.pyplot as plt
from sklearn import svm

CONTAINER_PATH = 'training_set'
TOP_LEFT_X=377  #362/6 for 720p, 182 for 360p
TOP_LEFT_Y=595  #590 for 720p, 295/6 for 360p
DELTA_X=24      #35 for 720p, 15/8 for 360p
DELTA_Y=24      #28 for 720p, 12/4 for 360p
# yellow scoreboard
# TOP_LEFT_X=365  #362 for 720p, 182 for 360p
# TOP_LEFT_Y=605  #590 for 720p, 295/6 for 360p
# DELTA_X=25      #35 for 720p, 15/8 for 360p
# DELTA_Y=28      #20 for 720p, 12/4 for 360p
# START_FRAME=389
START_FRAME=104
END_FRAME=3000

def load_digit_training_data():
    digits_new = {}
    data = []
    target = []
    folders = [f for f in sorted(os.listdir(CONTAINER_PATH)) if os.path.isdir(os.path.join(CONTAINER_PATH, f))]
    #print folders
    for folder in folders:
        folder_path = os.path.join(CONTAINER_PATH, folder)
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
    clf = svm.SVC(kernel='poly', degree = 3)
    clf.fit(digits_new['data'][:], digits_new['target'][:])
    return clf

def valid(num):
    if num != None and num!="" and len(num)==1 or len(num)==2 and num[0]=='1':
        return True
    return False

def set_valid(num):
    if num != None and num!="" and len(num)==1 and num[0] <= '4' and num[0] >= '0':
        return True
    return False

def conv_to_num(clf, im):
    # print np.asarray(im).shape
    num = clf.predict(np.asarray(im).ravel())
    return str(num[0])

def find_num(clf, input_png, output_serve, output_score_1, output_score_2, output_set_1, output_set_2):
    sharpness_factor = 0.0
    brightness_factor = 0.0
    # sharpness_factor = 10.0
    # brightness_factor = 10.0
    im = Image.open(input_png)
    # im = Image.open(input_png).convert('L')
    im_serve = im.crop((TOP_LEFT_X-DELTA_X, TOP_LEFT_Y, TOP_LEFT_X, TOP_LEFT_Y+DELTA_Y)).convert('L')
    # im_serve.save(output_serve)
    im1 = im.crop((TOP_LEFT_X, TOP_LEFT_Y, TOP_LEFT_X+DELTA_X, TOP_LEFT_Y+DELTA_Y)).convert('L')
    # enhancer = ImageEnhance.Sharpness(im1)
    # im1 = enhancer.enhance(sharpness_factor)
    # enhancer = ImageEnhance.Brightness(im1)
    # im1 = enhancer.enhance(brightness_factor)
    im1.save(output_score_1)
    im2 = im.crop((TOP_LEFT_X, TOP_LEFT_Y+DELTA_Y, TOP_LEFT_X+DELTA_X, TOP_LEFT_Y+2*DELTA_Y)).convert('L')
    # enhancer = ImageEnhance.Sharpness(im2)
    # im2 = enhancer.enhance(sharpness_factor)
    # enhancer = ImageEnhance.Brightness(im2)
    # im2 = enhancer.enhance(brightness_factor)
    im2.save(output_score_2)
    im_set1 = im.crop((TOP_LEFT_X+DELTA_X, TOP_LEFT_Y, TOP_LEFT_X+2*DELTA_X, TOP_LEFT_Y+DELTA_Y)).convert('L')
    # enhancer = ImageEnhance.Sharpness(im_set1)
    # im_set1 = enhancer.enhance(sharpness_factor)
    im_set1.save(output_set_1)
    im_set2 = im.crop((TOP_LEFT_X+DELTA_X, TOP_LEFT_Y+DELTA_Y, TOP_LEFT_X+2*DELTA_X, TOP_LEFT_Y+2*DELTA_Y)).convert('L')
    # enhancer = ImageEnhance.Sharpness(im_set2)
    # im_set2 = enhancer.enhance(sharpness_factor)
    im_set2.save(output_set_2)
    return (conv_to_num(clf, im_serve),
            conv_to_num(clf, im1),
            conv_to_num(clf, im2),
            conv_to_num(clf, im_set1),
            conv_to_num(clf, im_set2))


if __name__=='__main__':
    start_time = time.time()
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help='Path to the directory containing .png frames from the video')
    parser.add_argument("output_dir", type=str, help='Path to the directory where one wants to output the croped digit images')
    args = parser.parse_args()
    args.input_dir = os.path.abspath(args.input_dir)
    args.output_dir = os.path.abspath(args.output_dir)

    # Actual algorithm to find the split points
    index = START_FRAME
    input_frame_file = os.path.join(args.input_dir, 'frame_%05d.png'%index)
    frame_num = []
    score_num_1 = []
    score_num_2 = []
    set_num_1 = []
    set_num_2 = []
    clf = load_digit_training_data()
    # print input_frame_file
    while (os.path.exists(input_frame_file) and index<=END_FRAME):
        input_frame_file = os.path.join(args.input_dir, 'frame_%05d.png'%index)
        output_serve = os.path.join(args.output_dir, 'frame_%05d_serve1.png'%index)
        output_score_1 = os.path.join(args.output_dir, 'frame_%05d_1.png'%index)
        output_score_2 = os.path.join(args.output_dir, 'frame_%05d_2.png'%index)
        output_set_1 = os.path.join(args.output_dir, 'frame_%05d_set_1.png'%index)
        output_set_2 = os.path.join(args.output_dir, 'frame_%05d_set_2.png'%index)
        num_serve, num_1,num_2, num_set1, num_set2 = find_num(clf, input_frame_file, output_serve, output_score_1, output_score_2, output_set_1, output_set_2)
        num_1 = num_1.strip()
        num_2 = num_2.strip()
        num_set1 = num_set1.strip()
        num_set2 = num_set2.strip()
        try:
            # if num != None and num!="" and int(num)<=30 and int(num)>=0:
            if valid(num_1) and valid(num_2) and set_valid(num_set1) and set_valid(num_set2):
                num_int_1 = int(num_1)
                num_int_2 = int(num_2)
                num_int_set1 = int(num_set1)
                num_int_set2 = int(num_set2)
                frame_num.append(index)
                score_num_1.append(num_int_1)
                score_num_2.append(num_int_2)
                set_num_1.append(num_int_set1)
                set_num_2.append(num_int_set2)
                print "VALIDATION_TEST_PASS: ",
        except ValueError:
            pass
        print "index:", index, ";score_1:", num_1, ";score_2:", num_2, ";set_1:", num_set1, ";set_2:", num_set2, ";serve:", num_serve
        index+=1

    print "TOTAL EXECUTION TIME:"+str(time.time()-start_time)+" seconds"

    # Post-processing
    result_frame=[]
    result_score_1=[]
    result_score_2=[]
    for n in xrange(len(frame_num)):
        if n-1>=0 and n+1<len(frame_num) and frame_num[n]-frame_num[n-1]>3 and frame_num[n+1]-frame_num[n]>3:
            print "Removing element at index:", n
            print "\t", frame_num[n], score_num_1[n], score_num_2[n]
            continue
        result_frame.append(frame_num[n])
        result_score_1.append(score_num_1[n])
        result_score_2.append(score_num_2[n])

    # Print the result and generate plot
    for n in xrange(len(result_frame)):
        print result_frame[n], result_score_1[n], result_score_2[n]
    plt.plot(result_frame, result_score_1, "r--", result_frame, result_score_2, "g+")
    plt.ylim([-1, 12])
    plt.show()
