from pytube import YouTube
import os
import time
import argparse
from pytube.utils import print_status
from pprint import pprint

# [<Video: MPEG-4 Visual (.3gp) - 144p>,
#  <Video: MPEG-4 Visual (.3gp) - 240p>,
#  <Video: Sorenson H.263 (.flv) - 240p>,
#  <Video: H.264 (.flv) - 360p>,
#  <Video: H.264 (.flv) - 480p>,
#  <Video: H.264 (.mp4) - 360p>,
#  <Video: H.264 (.mp4) - 720p>,
#  <Video: VP8 (.webm) - 360p>,
#  <Video: VP8 (.webm) - 480p>]

def download_video(yt, path, file_name):
    yt.set_filename(file_name)

    # print(yt.filter('mp4')[-1])
    # pprint(yt.filter(resolution='480p'))
    # video = yt.get('mp4', '720p')
    # video.download()
    # yt.videos[0].download()
    try:
        # yt.videos[0].download(path=os.getcwd(), on_progress=print_status)
        yt.get('mp4', '720p').download(path=path, on_progress=print_status)
    except KeyboardInterrupt:
        print("Download interrupted.")
    # Note: If you wanted to choose the output directory, simply pass it as an
    # argument to the download method.

if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("url_file", type=str, help='Path to the url.txt file')
    parser.add_argument("output_dir", type=str, help='Output directory where the downloaded .mp4 files go')
    args = parser.parse_args()

    file_name = args.url_file
    print "file_name is: ", file_name
    with open(file_name) as f:
        for line in f:
            if line[0] == "#":
                prev_line = line
                continue
            print "========= DOWNLOAD YOUTUBE VIDEO ========="
            print "Link: "+line[:-1]
            print "Name: "+prev_line[2:-1]
            yt = YouTube(line)
            # download_video(yt, os.getcwd(), prev_line[2:])
            download_video(yt, args.output_dir, prev_line[2:-1])
            prev_line = line
    print "TOTAL EXECUTION TIME:"+str(time.time() - start_time)+" seconds"

