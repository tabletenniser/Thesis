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
TOP_LEFT_X=182  #362 for 720p, 182 for 360p
TOP_LEFT_Y=295  #590 for 720p, 296 for 360p
DELTA_X=18      #35 for 720p, 15 for 360p
DELTA_Y=14      #20 for 720p, 12 for 360p
START_FRAME=275
END_FRAME=400

def find_num(input_png, output_png):
    # im = Image.open(IMAGE)
    im = Image.open(input_png).convert('L')
    im = im.crop((TOP_LEFT_X, TOP_LEFT_Y, TOP_LEFT_X+DELTA_X, TOP_LEFT_Y+DELTA_Y))
    im.save(output_png)
    # cmd = "./textcleaner "+output_png+" "+output_image2
    # os.system(cmd)
    # im = Image.open(output_image2).convert('L')
    im = Image.open(output_png).convert('L')
    # print(pytesseract.image_to_string(im, boxes=True, config='-psm 6 digits'))
    # print(pytesseract.image_to_string(im, config='-psm 6 digits'))
    return (pytesseract.image_to_string(im, config='-psm 6 digits'))
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
    score_num = []
    # print input_frame_file
    while (os.path.exists(input_frame_file) and index<=END_FRAME):
        input_frame_file = os.path.join(args.input_dir, 'frame_%05d.png'%index)
        output_frame_file = os.path.join(args.output_dir, 'frame_%05d.png'%index)
        num = find_num(input_frame_file, output_frame_file)
        try:
            # if num != None and num!="" and int(num)<=30 and int(num)>=0:
            if num != None and num!="" and len(num)==1 or len(num)==2 and num[0]=='1':
                num_int = int(num)
                frame_num.append(index)
                score_num.append(num_int)
        except ValueError:
            pass
        print "index: ", index, "; num:", num
        index+=1

    print "TOTAL EXECUTION TIME:"+str(time.time()-start_time)+" seconds"
    for n in xrange(len(frame_num)):
        print frame_num[n], score_num[n]
    plt.plot(frame_num, score_num)
    plt.show()
