Fourth Year Thesis
==========

Steps:
---------------
1. python crawl.py <path_to_utl.txt> <output_folder_for_mp4_files>
2. python decompose_ffmpeg.py <input_foler_for_mp4_files> <output_foler_for_jpg_files_with_subfolers> using ffmpeg program
  * decompose_to_frames does the same thing but using opencv instead of ffmpeg
3. (optional) python create_edge_detected_frames.py <folder_where_jpg_files_locate> <output_folder_for_edge_detected_images>
4. python label_match.py <directory_for_short_video_frames> <directory_for_full_video_frames> | tee log.txt
  * assume all images in the folder have the format of frame_%05d.jpg
