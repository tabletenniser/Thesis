try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import time
import argparse
import os
import matplotlib.pyplot as plt

# IMAGE='testing/images/frame_00321.png'
# output_image='testing/images/frame_cropped.png'
output_image2='testing/images/frame_cropped_clean.png'
TOP_LEFT_X=366  #362 for 720p, 182 for 360p
TOP_LEFT_Y=590  #590 for 720p, 295/6 for 360p
DELTA_X=35      #35 for 720p, 15/8 for 360p
DELTA_Y=28      #20 for 720p, 12/4 for 360p
# TOP_LEFT_X=182  #362 for 720p, 182 for 360p
# TOP_LEFT_Y=295  #590 for 720p, 295/6 for 360p
# DELTA_X=18      #35 for 720p, 15/8 for 360p
# DELTA_Y=14      #20 for 720p, 12/4 for 360p
# START_FRAME=389
START_FRAME=1430
END_FRAME=1480

def valid(num):
    if num != None and num!="" and len(num)==1 or len(num)==2 and num[0]=='1':
        return True
    return False

def find_num(input_png, output_png_1, output_png_2):
    # im = Image.open(IMAGE)
    im = Image.open(input_png).convert('L')
    im1 = im.crop((TOP_LEFT_X, TOP_LEFT_Y, TOP_LEFT_X+DELTA_X, TOP_LEFT_Y+DELTA_Y))
    im1.save(output_png_1)
    im2 = im.crop((TOP_LEFT_X, TOP_LEFT_Y+DELTA_Y, TOP_LEFT_X+DELTA_X, TOP_LEFT_Y+2*DELTA_Y))
    im2.save(output_png_2)
    # cmd = "./textcleaner "+output_png+" "+output_image2
    # os.system(cmd)
    # im = Image.open(output_image2).convert('L')
    im_1 = Image.open(output_png_1).convert('L')
    im_2 = Image.open(output_png_2).convert('L')
    # print(pytesseract.image_to_string(im, boxes=True, config='-psm 6 digits'))
    # print(pytesseract.image_to_string(im, config='-psm 6 digits'))
    CONF = '-psm 6 digits'
    return (pytesseract.image_to_string(im_1, config=CONF), pytesseract.image_to_string(im_2, config=CONF))
    # return (pytesseract.image_to_string(im, config='-psm 5 digits'))

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
    # print input_frame_file
    while (os.path.exists(input_frame_file) and index<=END_FRAME):
        input_frame_file = os.path.join(args.input_dir, 'frame_%05d.png'%index)
        output_frame_file_1 = os.path.join(args.output_dir, 'frame_%05d_1.png'%index)
        output_frame_file_2 = os.path.join(args.output_dir, 'frame_%05d_2.png'%index)
        num_1,num_2 = find_num(input_frame_file, output_frame_file_1, output_frame_file_2)
        try:
            # if num != None and num!="" and int(num)<=30 and int(num)>=0:
            if valid(num_1) and valid(num_2):
                num_int_1 = int(num_1)
                num_int_2 = int(num_2)
                frame_num.append(index)
                score_num_1.append(num_int_1)
                score_num_2.append(num_int_2)
                print "PASS: ",
        except ValueError:
            pass
        print "index: ", index, "; num_1:", num_1, "; num_2:", num_2
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
