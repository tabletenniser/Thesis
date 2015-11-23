import argparse
import os
import shutil
import time

# Take 4 .png iamges per second
SAMPLE_RATE = 4.0

# video_path is a .mp4 file; output_dir is the directory containing all the output frames.
def create_video_clip_and_copy_frames(frame_list_file, frames_path, video_path, output_dir):
    if not os.path.isdir(output_dir):
        print "create directory: ", output_dir
        os.makedirs(output_dir)

    f = open(frame_list_file, 'r')
    pt_index = 1
    for line in f:
        print line
        frames = line.split(':')
        frames[0] = int(frames[0])
        frames[1] = int(frames[1])
        print frames[0], frames[1]
        output_frame_dir = os.path.join(output_dir, 'point_%04d'%pt_index)
        if not os.path.isdir(output_frame_dir):
            os.makedirs(output_frame_dir)
        for index in xrange(frames[0], frames[1]):
            input_file = os.path.join(frames_path, "frame_%05d.png"%index)
            shutil.copy(input_file, output_frame_dir)
        # ffmpeg -i video1_xuxin_vs_fanzhendong_sweden_2015.mp4 -ss 313 -c copy -t 5 output.mp4
        output_file = os.path.join(output_dir, 'point_%04d.mp4'%pt_index)
        start_time = str(frames[0]/SAMPLE_RATE - 1)
        duration = str((frames[1]-frames[0])/SAMPLE_RATE)
        cmd = "ffmpeg -i "+video_path+" -ss "+start_time+" -c copy -t "+duration+" "+output_file
        print "Running command: ", cmd
        os.system(cmd)
        pt_index += 1
    return

def main(input_frame, input_video, output_dir):
    top_player_winning_file = os.path.join(input_frame, 'results', 'top_player_winning_frames.txt')
    bottom_player_winning_file = os.path.join(input_frame, 'results', 'bottom_player_winning_frames.txt')
    output_top_player_winning_dir = os.path.join(output_dir, 'top_player_winning')
    output_bottom_player_winning_dir = os.path.join(output_dir, 'bottom_player_winning')
    start_time = time.time()

    # Copy cut video clips and frame images over.
    create_video_clip_and_copy_frames(top_player_winning_file, input_frame, input_video, output_top_player_winning_dir)
    create_video_clip_and_copy_frames(bottom_player_winning_file, input_frame, input_video, output_bottom_player_winning_dir)
    print "CONSTRUCT_CLIPS_STRUCTURE.PY TAKES:"+str(time.time()-start_time)+" seconds"
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_frame", type=str, help='Path to the directory where the frames locate. Should also contain a /results folder containing top_player_winning_frames.txt and bottom_player_winning_frames.txt inside')
    parser.add_argument("input_video", type=str, help='Path to the original video clip.')
    parser.add_argument("output_dir", type=str, help='Path where the resultant individual points should locate.')
    args = parser.parse_args()
    args.input_frame = os.path.abspath(args.input_frame)
    args.input_video = os.path.abspath(args.input_video)
    args.output_dir = os.path.abspath(args.output_dir)
    main(args.input_frame, args.input_video, args.output_dir)
