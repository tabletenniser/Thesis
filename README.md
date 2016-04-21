Fourth Year Thesis
==========

Hi there, welcome to my undergraduate thesis github repo! This project aims to utilize machine learning techniques to create semantic understanding in table tennis video clips. The current result is summarized in the final_report.pdf. Check out some data visualization of this project here:
https://www.youtube.com/watch?v=G8wE_eo7o-I
https://www.youtube.com/watch?v=aEgCOY8CNso


Procedure to reproduce the 58% annotation accuracy mentioned in final_report.pdf:
---------------
1. python wrapper_new_manual_label_for_pt.py final_input/url.txt final_input inter_dir output_dir output_labeled_image_dir
   * Create inter_dir folder containing the downloaded .mp4 files in videos/, decomposed frame images in frames/.
   * Create output_dir folder containing the set of corresponding frame images for each point.
   * Create output_labeled_image_dir folder containing same images as the output_dir but properly cropped and pre-processed. One folder per point.
2. Open sqlearn_data_preparation.py and change container_path (line 48) to the output_labeled_image_dir above and set the output_file (line 176) to the desired folder. Run 'python sqlearn_data_preparation.py'
   * This forward propogates over the AlexNet and convert each frame image into a 4096 vector and store the result in the corresponding .dat files. Each line in the .dat file corresponding to an image frame and contains values of the 4096 vector followed by the corresponding label.
3. Set the training_files and testing_files in sqlearn_crf.py to the corresponding folders containing the .dat files above and run 'python sqlearn_crf.py'. It should output 58% annotation accuracy to stdout!!!


Fine-tuning on AlexNet
---------------
1. python wrapper_new_manual_label.py final_input/url.txt final_input inter_dir output_dir output_labeled_image_dir
   * Create inter_dir folder containing the downloaded .mp4 files in videos/, decomposed frame images in frames/.
   * Create output_dir folder containing the set of corresponding frame images for each of the 28 defined classes (20 player stroke classes and 8 point-ending classes)
   * Create output_labeled_image_dir folder containing same images as the output_dir but properly cropped and pre-processed. All images from the same class but different points are put into the same folder.
   * 

Data Visualization
---------------



Steps in wrapper_new_manual_label.py
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
