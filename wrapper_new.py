import os
import time
import argparse
import crawler
import decompose_ffmpeg
import training_set_creation_knn_new
import construct_clips_structure
import move_training_set

if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("url_file", type=str, help='Path to the url.txt file')
    parser.add_argument("inter_dir", type=str, help='Path to the directory where intermediate result goes. Including decomposed frame images, score images and frame pair files.')
    parser.add_argument("output_dir", type=str, help='Output directory where points are separated into top_winning and bottom_winning folders.')
    parser.add_argument("-s", "--steps", type=str, default='12345', help="steps to perform. 12345 to perform all steps.")
    parser.add_argument("-m", "--mp4_video_dir", type=str, default='final_input/videos', help="mp4_video_dir")
    parser.add_argument("-f", "--frames_dir", type=str, default='final_input/frames', help="frames_dir")
    args = parser.parse_args()

    file_name = args.url_file
    ############### STEP 1: CRAWLER.PY ##############
    if '1' in args.steps:
        print '\n\n'+"="*20+'STEP #1: CRAWLER.PY'+'='*20
        mp4_video_dir = os.path.join(args.inter_dir, 'videos')
        if not os.path.isdir(mp4_video_dir):
            os.makedirs(mp4_video_dir)
        crawler.main(file_name, mp4_video_dir)
    ############### STEP 2: DECOMPOSE_TO_FRAMES.PY ##############
    if '2' in args.steps:
        if not 'mp4_video_dir' in locals() and not 'mp4_video_dir' in globals():
            mp4_video_dir = args.mp4_video_dir
        print '\n\n'+"="*15+'STEP #2: DECOMPOSE_TO_FRAMES.PY'+'='*15
        frames_dir = os.path.join(args.inter_dir, 'frames')
        if not os.path.isdir(frames_dir):
            os.makedirs(frames_dir)
        decompose_ffmpeg.main(mp4_video_dir, frames_dir)
    ############### STEP 3: TRAINING_SET_CREATION.PY ##############
    ############### STEP 4: CONSTRUCT_CLIPS_STRUCTURE.PY ##############
    if '3' in args.steps or '4' in args.steps:
        if not 'mp4_video_dir' in locals() and not 'mp4_video_dir' in globals():
            mp4_video_dir = args.mp4_video_dir
        if not 'frames_dir' in locals() and not 'frames_dir' in globals():
            frames_dir = args.frames_dir
        training_data_dir = os.path.join(args.inter_dir, 'classified_data')
        scores_dir = os.path.join(args.inter_dir, 'scores_images')
        if not os.path.isdir(training_data_dir):
            os.makedirs(training_data_dir)
        if not os.path.isdir(scores_dir):
            os.makedirs(scores_dir)
        for fn in os.listdir(frames_dir):
            print '\n\n'+"="*15+'STEP #3: TRAINING_SET_CREATION.PY'+'='*15
            input_frame_dir = os.path.join(frames_dir, fn)
            if not os.path.isdir(input_frame_dir):
                continue
            print "folder: ", input_frame_dir
            result_subdir = os.path.join(input_frame_dir, 'results')
            if not os.path.isdir(result_subdir):
                os.makedirs(result_subdir)
            score_subdir = os.path.join(scores_dir, fn)
            if not os.path.isdir(score_subdir):
                os.makedirs(score_subdir)
            video_metadata = input_frame_dir.split('_')
            top_left_x, top_left_y, delta_x, delta_y = video_metadata[-5], video_metadata[-4], video_metadata[-3], video_metadata[-2]
            is_top_player_top = video_metadata[-1] == 't'
            training_set_creation_knn_new.main(input_frame_dir, score_subdir, result_subdir, int(top_left_x), int(top_left_y), int(delta_x), int(delta_y), is_top_player_top)

            print '\n\n'+"="*15+'STEP #4: CONSTRUCT_CLIPS_STRUCTURE.PY'+'='*15
            # Call construct_clips_structure.py
            train_subdir = os.path.join(training_data_dir, fn)
            if not os.path.isdir(train_subdir):
                os.makedirs(train_subdir)
            video_file = os.path.join(mp4_video_dir, str(fn)+'.mp4')
            construct_clips_structure.main(input_frame_dir, video_file, train_subdir)
    ############### STEP 5: MOVE_TRAINING_SET.PY ##############
    if '5' in args.steps:
        move_training_set.main(training_data_dir, args.output_dir)

