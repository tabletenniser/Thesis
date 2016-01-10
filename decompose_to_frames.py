import cv2
import argparse
import os
import time
import logging

FRAME_GAP = 1
START_FRAME = 100

# video_path is a .mp4 file; output_dir is the directory containing all the output frames.
def extract_frames(video_path, output_dir):
    logging.info("Writing video: "+str(video_path)+" to "+str(output_dir))
    vidcap = cv2.VideoCapture(video_path)
    # image is an array of array of [R,G,B] values]
    success,image = vidcap.read()
    count = START_FRAME;
    while success:
        success,image = vidcap.read()
        if count % FRAME_GAP ==0:
            file_path = os.path.join(output_dir, "frame%d.jpg" % count)
            logging.info("Writing to file"+str(file_path))
            cv2.imwrite(file_path, image)     # save frame as JPEG file
        if cv2.waitKey(10) == 27:             # exit if Escape is hit
            break
        count += 1


if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help='Path to the directory where .mp4 files locate')
    parser.add_argument("output_dir", type=str, help='Path to where the .jpg frames will be output to')
    args = parser.parse_args()
    args.input_dir = os.path.abspath(args.input_dir)
    args.output_dir = os.path.abspath(args.output_dir)
    print "Input directory is ", args.input_dir
    print "Output directory is ", args.output_dir

    for fn in os.listdir(args.input_dir):
        video_file_path = os.path.join(args.input_dir, fn)
        video_file_name, video_file_extension = os.path.splitext(video_file_path)
        if not video_file_extension==".mp4":
            print "Skip non .mp4 file", video_file_path
            continue
        print "Input video path is: ", video_file_path
        output_path = os.path.join(args.output_dir, os.path.basename(video_file_name))
        print "Output path is: ", output_path
        if os.path.isdir(output_path):
            print "ERROR: OUTPUT PATH ALREADY EXISTS!!! Program exist"
            exit()
        os.makedirs(output_path)
        extract_frames(video_file_path, output_path)
    print "TOTAL EXECUTION TIME:"+str(time.time()-start_time)+" seconds"
