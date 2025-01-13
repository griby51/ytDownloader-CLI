from pytubefix import Playlist, YouTube
import argparse
import sys
import shutil
import os

#thanks u chatgpt
def showProgressBar(progress, total, prefix=""):
    terminal_width = shutil.get_terminal_size().columns
    progress_width = 25
    space_for_progress = 10

    prefix_max_len = terminal_width - progress_width - space_for_progress - 4

    if len(prefix) > prefix_max_len:
        prefix = prefix[:prefix_max_len] + "..."
    
    ratio = progress / total
    filled = int(ratio * progress_width)
    
    bar = f"{prefix}{' ' * (terminal_width - len(prefix) - progress_width - space_for_progress)}[{'#' * filled}{' ' * (progress_width - filled)}] {ratio * 100:.2f}%"
    
    sys.stdout.write(f"\r{bar}")
    sys.stdout.flush()
    if progress == total:
        print()

def dlVideo(url, onlyAudio = False, prefix="", folder=""):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)

        yt = YouTube(url)
        title = yt.title
        prefix = prefix + " " + title
        yt.register_on_progress_callback(lambda stream, chunk, bytes_remaining: showProgressBar(stream.filesize - bytes_remaining, stream.filesize, prefix=prefix))

        if onlyAudio:
            video = yt.streams.get_audio_only()
        else:
            video = yt.streams.get_highest_resolution()
        video.download(folder)
    except Exception as e:
        print(e)

def dlPlaylist(url, onlyAudio = False, folder=""):
    pl = Playlist(url)
    i = 1
    for video_url in pl.video_urls:
        #prefix = (video url number/total video number)
        prefix = f"({i}/{len(pl.video_urls)})"
        dlVideo(video_url, onlyAudio=onlyAudio, prefix=prefix, folder=folder)
        i += 1

def main():
    parser = argparse.ArgumentParser(description="A simple Youtube Downloader")
    parser.add_argument("url", type=str, nargs="?" ,help="Paste the link of the YouTube video or playlist")
    parser.add_argument("-a", "--audio", action="store_true", help="Download only the audio")
    parser.add_argument("-f", "--folder", type=str, help="Download the video in selected folder")
    args = parser.parse_args()

    folder = args.folder
    if not folder:
        folder = "./"

    if not args.url:
        args.url = input("Paste the link of the YouTube video or playlist: ")
        onlyAudio = input("Download only the audio? (y/n): ")
        if onlyAudio == "y":
            args.audio = True
        else:
            args.audio = False
        
        folder = input("Download the video in selected folder? (y/n): ")
        if folder == "y":
            folder = input("Enter the folder path: ")
        else:
            folder = "./"
        
        

    try: 
        if "list" in args.url:
            dlPlaylist(args.url, args.audio, folder=folder)
        else:
            dlVideo(args.url, args.audio, folder=folder)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
