try:
    import Image
except ImportError:
    from PIL import Image
import time
import argparse
import os
import numpy as np
import shutil
from scipy.io.wavfile import read,write
from numpy.fft import rfft, irfft
from scipy.signal import blackmanharris, fftconvolve

SAMPLE_RATE = 20

def create_folder_if_not_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return

def crop_size_for_video_and_images(input_dir, output_image_dir, output_video_dir, output_audio_dir):
    create_folder_if_not_exist(output_image_dir)
    create_folder_if_not_exist(output_video_dir)
    create_folder_if_not_exist(output_audio_dir)
    folders = [f for f in sorted(os.listdir(input_dir)) if os.path.isdir(os.path.join(input_dir, f))]
    print 'folders:', folders

    # folders should contain bottom_player_winning and top_player_winning.
    for folder in folders:
        input_folder_path = os.path.join(input_dir, folder)
        image_folders = [f for f in sorted(os.listdir(input_folder_path)) if os.path.isdir(os.path.join(input_folder_path, f))]
        videos = [str(img)+'.mp4' for img in image_folders]
        output_video_path = os.path.join(output_video_dir, folder)
        output_audio_path = os.path.join(output_audio_dir, folder)
        output_image_path = os.path.join(output_image_dir, folder)
        create_folder_if_not_exist(output_video_path)
        create_folder_if_not_exist(output_image_path)
        create_folder_if_not_exist(output_audio_path)
        # if more than 10 image frames, copy re-sample video at SAMPLE_RATE
        # copy videos to output_video_path
        for img_folder in image_folders:
            v = img_folder+'.mp4'
            a = img_folder+'.wav'
            full_input_folder_name = os.path.join(input_folder_path, img_folder)
            if len(os.listdir(full_input_folder_name)) <= 10:
                continue
            full_video_name = os.path.join(input_folder_path, v)
            full_img_folder_name = os.path.join(output_image_path, img_folder)
            create_folder_if_not_exist(full_img_folder_name)
            output_img_files = os.path.join(full_img_folder_name, "frame_%05d.png")
            if (os.path.isfile(full_video_name)):
                # 1) Create cropped output image files re-sample at SAMPLE_RATE
                cmd = "ffmpeg -i "+full_video_name+" -vf 'crop=600:600:300:0' -r "+str(SAMPLE_RATE)+" "+output_img_files
                os.system(cmd)

                # 2) Create cropped output video files
                # ffmpeg -i point_00010.mp4 -vf "crop=600:600:300:0" after.mp4
                cmd = "ffmpeg -i "+full_video_name+" -vf 'crop=600:600:300:0' "+os.path.join(output_video_path,v)
                os.system(cmd)

                # 3) Create cropped output audio files
                cmd = "ffmpeg -i "+full_video_name+" "+os.path.join(output_audio_path, a)
                os.system(cmd)
        print 'Finish copying to video destination:', output_video_path
    return


def freq_from_fft(sig, fs):
    """Estimate frequency from peak of FFT

    """
    # Compute Fourier transform of windowed signal
    windowed = sig * blackmanharris(len(sig))
    f = rfft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = np.argmax(abs(f)) # Just use this for less-accurate, naive version
    # true_i = parabolic(log(abs(f)), i)[0]

    # Convert to equivalent frequency
    return fs * i / len(windowed)

def freq_over_time(y,Fs):
    resultFreq = []
    x_val = []
    start_num = 0
    while start_num+2*Fs < len(y):
        resultFreq.append(freq_from_fft(y[:,1][start_num: start_num+2*Fs], Fs))
        x_val.append(start_num)
        start_num += Fs/SAMPLE_RATE
    return resultFreq

###### CODE BELOW SELECTS LAST SAMPLE_RATE FRAMES (last second) OF EACH POINT AND PUT INTO THE *_selected FOLDER #####
def select_images_last_10(output_image_dir):
    assert(os.path.isdir(output_image_dir))
    folders = [f for f in sorted(os.listdir(output_image_dir)) if os.path.isdir(os.path.join(output_image_dir, f))]
    # folders should contain bottom_player_winning and top_player_winning.

    for folder in folders:
        output_selected_image_path = os.path.join(output_image_dir, folder+'_selected')
        create_folder_if_not_exist(output_selected_image_path)
        output_image_path = os.path.join(output_image_dir, folder)
        assert(os.path.isdir(output_image_path))

        image_folders = [f for f in sorted(os.listdir(output_image_path)) if os.path.isdir(os.path.join(output_image_path, f))]
        for img_folder in image_folders:
            full_output_image_path = os.path.join(output_image_path, img_folder)

            files_to_copy = sorted(os.listdir(full_output_image_path))
            if len(files_to_copy) < 10:
                continue
            for f in files_to_copy[-10:]:
                src = os.path.join(full_output_image_path, f)
                dest = os.path.join(output_selected_image_path, img_folder+'_'+f)
                print "DEBUG: copy ", src, " to ", dest
                shutil.copy(src, dest)


###### CODE BELOW SELECTS 10 FRAMES OF EACH POINT AND PUT INTO THE *_selected FOLDER #####
def select_images(output_image_dir, output_audio_dir):
    assert(os.path.isdir(output_image_dir))
    assert(os.path.isdir(output_audio_dir))
    folders = [f for f in sorted(os.listdir(output_image_dir)) if os.path.isdir(os.path.join(output_image_dir, f))]
    # folders should contain bottom_player_winning and top_player_winning.

    for folder in folders:
        output_selected_image_path = os.path.join(output_image_dir, folder+'_selected')
        create_folder_if_not_exist(output_selected_image_path)
        output_image_path = os.path.join(output_image_dir, folder)
        output_audio_path = os.path.join(output_audio_dir, folder)
        assert(os.path.isdir(output_image_path))
        assert(os.path.isdir(output_audio_path))

        image_folders = [f for f in sorted(os.listdir(output_image_path)) if os.path.isdir(os.path.join(output_image_path, f))]
        for img_folder in image_folders:
            full_output_image_path = os.path.join(output_image_path, img_folder)
            full_output_audio_file = os.path.join(output_audio_path, img_folder+'.wav')
            rate, data = read(full_output_audio_file)
            freq_array = freq_over_time(data, rate)
            print 'audio file: ', full_output_audio_file
            print 'freq array: ', freq_array
            # Iterate through all frequencies and find the first time where frequency goes under 250Hz from the back
            index = len(freq_array)-1
            while True:
                if index == 0:
                    index = len(freq_array)-1
                    break
                if freq_array[index] < 250 and freq_array[index-1] < 250 and freq_array[index-2] < 250:
                    break
                index -= 1

            files_to_copy = sorted(os.listdir(full_output_image_path))
            print 'files_to_copy.size(): ', len(files_to_copy), 'freq_array.size(): ', len(freq_array)
            # prop_index = len(freq_array)-1-index
            for f in files_to_copy[index+11:index+21]:  # +21 because frequency is taken over 2 seconds
                src = os.path.join(full_output_image_path, f)
                dest = os.path.join(output_selected_image_path, img_folder+'_'+f)
                print "DEBUG: copy ", src, " to ", dest
                shutil.copy(src, dest)

if __name__=='__main__':
    start_time = time.time()
    # Parse out the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str, help='Path to the directory containing a top_player_winning folder and a bottom_player_winning folder.')
    parser.add_argument("image_dir", type=str, help='Path to the output images from the game.')
    parser.add_argument("video_dir", type=str, help='Path to the output video directory.')
    parser.add_argument("audio_dir", type=str, help='Path to the output audio directory.')
    args = parser.parse_args()
    args.input_dir = os.path.abspath(args.input_dir)
    args.image_dir = os.path.abspath(args.image_dir)
    args.video_dir = os.path.abspath(args.video_dir)
    args.audio_dir = os.path.abspath(args.audio_dir)
    # crop_size_for_video_and_images(args.input_dir, args.image_dir, args.video_dir, args.audio_dir)
    # select_images(args.image_dir, args.audio_dir)
    select_images_last_10(args.image_dir)
    print "TOTAL EXECUTION TIME:"+str(time.time()-start_time)+" seconds"
