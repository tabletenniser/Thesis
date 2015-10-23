import argparse
import os
# import subprocess
import time

# Take 4 .jpg iamges per second
SAMPLE_RATE = 4

# video_path is a .mp4 file; output_dir is the directory containing all the output frames.
def extract_frames(video_path, output_dir):
    output_files = os.path.join(output_dir, "frame_%05d.jpg")
    # cmd = ["ffmpeg", "-i", video_path, "-r", str(SAMPLE_RATE), output_files]
    # print "command running is", cmd
    # subprocess.call(cmd, shell=True)
    cmd = "ffmpeg -i "+video_path+" -r "+str(SAMPLE_RATE)+" "+output_files
    os.system(cmd)
    return

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
