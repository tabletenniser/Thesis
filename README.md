Fourth Year Thesis
==========

Procedure to create training set to learn rule of table tennis:
1. python wrapper_new.py
2. python training_set_preparation_postprocessing.py


Steps:
---------------
1. python crawl.py `<path_to_utl.txt>` `<output_folder_for_mp4_files>`
2. python decompose_ffmpeg.py `<input_foler_for_mp4_files>` `<output_foler_for_jpg_files_with_subfolers>` using ffmpeg program
  * decompose_to_frames does the same thing but using opencv instead of ffmpeg
3. (optional) python create_edge_detected_frames.py `<folder_where_jpg_files_locate>` `<output_folder_for_edge_detected_images>`
4. (optional) python label_match_diff.py `<directory_for_short_video_frames>` `<directory_for_full_video_frames>` | tee log.txt
  * assume all images in the folder have the format of frame_%05d.jpg
5. (optional) python score_recognition.py `<directory_for_short_video_frames>` `<directory_for_score_images>` | tee log.txt
6. python training_set_creation.py `<directory_for_score_images>` `<directory_for_list_of_frame_pair_file>`
6. python construct_clips_structure.py `<frame_images>` `<path_to_mp4_file>` `<output_directory_for_images_within>`
