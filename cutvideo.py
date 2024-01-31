import tkinter as tk
from tkinter import filedialog
import os
from moviepy.editor import VideoFileClip
from tqdm import tqdm

def accessPL():
    base_path = os.getcwd()
    PLfolder = os.path.join(base_path, 'processingLab')
    return os.listdir(PLfolder)

def process_video(video_path, dur_input):
    clip = VideoFileClip(video_path)

    base_name = os.path.basename(video_path)
    file_name, _ = os.path.splitext(base_name)

    clip_duration = clip.duration
    num_subclips = int(clip_duration / dur_input)

    # Create a ParentFolder if it doesn't exist for this video
    folder_name = file_name

    current_path = os.getcwd()
    saved_folder = os.path.join(current_path, 'imgFolder')

    if not os.path.isdir(saved_folder):
        os.makedirs(saved_folder)

    for i in tqdm(range(num_subclips), desc="Processing Subclips"):
        start = i * dur_input
        end = min((i + 1) * dur_input, clip_duration)
        output_name = f"p_{file_name}_{i}.mp4"
        sub_clip = clip.subclip(start, end)

        if i == num_subclips - 1:
            remaining_duration = clip_duration - end
            if remaining_duration > 0:
                sub_clip = sub_clip.set_duration(sub_clip.duration + remaining_duration)

        output_path = os.path.join(saved_folder, output_name)
        sub_clip.write_videofile(output_path, codec='libx264', verbose=False)

    clip.close()

if __name__ == "__main__":
    base_path = os.getcwd()
    imgFolder = os.path.join(base_path, 'imgFolder')
    print("Start processing videos...")
    for video in accessPL():
        print(f'Processing video {video}')
        video_path = os.path.join(imgFolder,video)
        process_video(video_path,15)
        print(f'{video} is done!')
