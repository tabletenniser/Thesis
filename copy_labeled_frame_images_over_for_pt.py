try:
    import Image
except ImportError:
    from PIL import Image
import time
import argparse
import os
import sys
import logging
import shutil

SAMPLE_RATE = 25.0

def create_dir_if_not_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return

# Copy frames images specified by input_label_file to the corresponding folder in output_dir
def main(input_frame_dir, input_video_path, input_label_file, output_dir, debug=True):
    perform_start_time = time.time()
    cur_pt_lines = []
    output_pt_dir = ''

    # If manual label file doesn't exist, return directly.
    if not os.path.isfile(input_label_file):
        return

    with open(input_label_file) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0 or line[0] == "#":
                if len(cur_pt_lines) > 0:
                    output_label_file = os.path.join(output_pt_dir, 'label.txt')
                    with open(output_label_file, 'w+') as f:
                        for l in cur_pt_lines:
                            f.write('%s\n'%l)
                    cur_pt_lines = []
                if len(line) > 0 and line[0] == "#" and "POINT" in line:
                    output_pt_dir = os.path.join(output_dir, line[1:])
                    create_dir_if_not_exist(output_pt_dir)
                continue

            cur_pt_lines.append(line)
            frames = line.split(':')
            # case where a label instead of the actual frame range
            if len(frames)!=3:
                print "ERROR: illegal line format!"
                continue

            # Case where the actual point data - COPY OVER THE IMAGES
            frames[0] = int(frames[0])
            frames[1] = int(frames[1])
            cls = frames[2]

            print "Copy image from ", input_frame_dir, " to ", output_pt_dir
            for index in xrange(frames[0], frames[1]):
                input_file = os.path.join(input_frame_dir, "frame_%05d.png"%index)
                shutil.copy(input_file, output_pt_dir)

            # ffmpeg -i video1_xuxin_vs_fanzhendong_sweden_2015.mp4 -ss 313 -c copy -t 5 output.mp4
            # DO NOT RECREATE VIDEO SAMPLE FOR NOW
            # output_file = os.path.join(output_class_dir, 'point_%04d.mp4'%pt_index)
            # start_time = str(frames[0]/SAMPLE_RATE - 1)
            # duration = str((frames[1]-frames[0])/SAMPLE_RATE)
            # cmd = "ffmpeg -i "+input_video_path+" -ss "+start_time+" -c copy -t "+duration+" "+output_file
            # print "Running command: ", cmd
            # os.system(cmd)

    logging.info("COPY_LABLED_FRAME_IMAGES_OVER.PY TAKES:"+str(time.time()-perform_start_time)+" seconds")
    return

if __name__=='__main__':
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_frame_dir", type=str, help='Path to the directory containing .png frames from the video')
    # parser.add_argument("input_video_path", type=str, help='Path to the original video file')
    parser.add_argument("input_label_file", type=str, help='File containing the labels and corresponding set of frame numbers')
    parser.add_argument("output_dir", type=str, help='Training set storage directory. Contain folders, each one is a label specified in input_label_file(e.g top_player_winning and bottom_player_winning)')
    args = parser.parse_args()
    args.input_frame_dir = os.path.abspath(args.input_frame_dir)
    # args.input_video_path = os.path.abspath(args.input_video_path)
    args.input_label_file = os.path.abspath(args.input_label_file)
    args.output_dir = os.path.abspath(args.output_dir)

    ########## Initialize the logging to stdout
    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)
    logging=log

    ######### Call main function to perform the copies
    # main(args.input_frame_dir, args.input_video_path, args.input_label_file, args.output_dir)
    main(args.input_frame_dir, '', args.input_label_file, args.output_dir)
