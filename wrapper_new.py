import os
import time
import argparse
import crawler
import decompose_ffmpeg
import training_set_creation_knn_new
import training_set_creation
import construct_clips_structure
import move_training_set
import logging

def init_logging():
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)15s()] %(levelname)s:%(message)s"
    # FORMAT = "%(asctime)s %(levelname)s:\t%(message)s"
    logging.basicConfig(filename='wrapper_new.log', format=FORMAT, datefmt='%m/%d %H:%M:%S', level=logging.DEBUG)
    logging.info('PROGRAM STARTS')

def create_folder_if_not_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return

if __name__ == '__main__':
    init_logging()
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
        logging.info("="*20+'STEP #1: CRAWLER.PY'+'='*20)
        mp4_video_dir = os.path.join(args.inter_dir, 'videos')
        create_folder_if_not_exist(mp4_video_dir)
        crawler.main(file_name, mp4_video_dir)
    ############### STEP 2: DECOMPOSE_FFMPEG.PY ##############
    if '2' in args.steps:
        if not 'mp4_video_dir' in locals() and not 'mp4_video_dir' in globals():
            mp4_video_dir = args.mp4_video_dir
        logging.info("="*15+'STEP #2: DECOMPOSE_FFMPEG.PY'+'='*15)
        frames_dir = os.path.join(args.inter_dir, 'frames')
        create_folder_if_not_exist(frames_dir)
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
        create_folder_if_not_exist(training_data_dir)
        create_folder_if_not_exist(scores_dir)
        for fn in os.listdir(frames_dir):
            logging.info("="*15+'STEP #3: TRAINING_SET_CREATION.PY'+'='*15)
            input_frame_dir = os.path.join(frames_dir, fn)
            if not os.path.isdir(input_frame_dir):
                continue
            logging.info("input frame folder: %s", input_frame_dir)
            result_subdir = os.path.join(input_frame_dir, 'results')
            create_folder_if_not_exist(result_subdir)
            score_subdir = os.path.join(scores_dir, fn)
            create_folder_if_not_exist(score_subdir)
            video_metadata = input_frame_dir.split('_')
            top_left_x, top_left_set_x, top_left_y, top_left_second_y, delta_x, delta_y = video_metadata[-7], video_metadata[-6], video_metadata[-5], video_metadata[-4], video_metadata[-3], video_metadata[-2]
            if video_metadata[-1] == 't':
                is_top_player_top = True
            else:
                is_top_player_top = False
            # training_set_creation.main(input_frame_dir, score_subdir, result_subdir, int(top_left_x), int(top_left_set_x), int(top_left_y), int(delta_x), int(delta_y), is_top_player_top, debug=True)
            training_set_creation_knn_new.main(input_frame_dir, score_subdir, result_subdir, int(top_left_x), int(top_left_set_x), int(top_left_y), int(top_left_second_y), int(delta_x), int(delta_y), is_top_player_top, debug=True)

            logging.info("="*15+'STEP #4: CONSTRUCT_CLIPS_STRUCTURE.PY'+'='*15)
            # Call construct_clips_structure.py
            train_subdir = os.path.join(training_data_dir, fn)
            if not os.path.isdir(train_subdir):
                os.makedirs(train_subdir)
            video_file = os.path.join(mp4_video_dir, str(fn)+'.mp4')
            construct_clips_structure.main(input_frame_dir, video_file, train_subdir)
    ############### STEP 5: MOVE_TRAINING_SET.PY ##############
    if '5' in args.steps:
        logging.info("="*15+'STEP #5: MOVE_TRAINING_SET.PY'+'='*15)
        move_training_set.main(training_data_dir, args.output_dir)

