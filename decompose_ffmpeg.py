import argparse
import os
# import subprocess
import time
import logging

# Take 4 .png iamges per second
SAMPLE_RATE = 25

# video_path is a .mp4 file; output_dir is the directory containing all the output frames.
def extract_frames(video_path, output_dir):
    output_files = os.path.join(output_dir, "frame_%05d.png")
    # cmd = ["ffmpeg", "-i", video_path, "-r", str(SAMPLE_RATE), output_files]
    # subprocess.call(cmd, shell=True)
    cmd = "ffmpeg -i "+video_path+" -r "+str(SAMPLE_RATE)+" "+output_files
    logging.debug("command running is %s", str(cmd))
    os.system(cmd)
    return

def main(input_dir, output_dir):
    start_time = time.time()
    for fn in os.listdir(input_dir):
        video_file_path = os.path.join(input_dir, fn)
        video_file_name, video_file_extension = os.path.splitext(video_file_path)
        if not video_file_extension==".mp4":
            logging.info("Skip non .mp4 file: %s", video_file_path)
            continue
        logging.info("Input video path is: %s", video_file_path)
        output_path = os.path.join(output_dir, os.path.basename(video_file_name))
        logging.info("Output path is: %s", output_path)
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        extract_frames(video_file_path, output_path)
    logging.info("DECOMPOSE_TO_FRAMES.PY TAKES:"+str(time.time()-start_time)+" seconds")
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help='Path to the directory where .mp4 files locate')
    parser.add_argument("output_dir", type=str, help='Path to where the .png frames will be output to')
    args = parser.parse_args()
    args.input_dir = os.path.abspath(args.input_dir)
    args.output_dir = os.path.abspath(args.output_dir)
    print "Input directory is ", args.input_dir
    print "Output directory is ", args.output_dir
    main(args.input_dir, args.output_dir)

