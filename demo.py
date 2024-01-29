import tkinter as tk
from tkinter import filedialog
import os
from moviepy.editor import VideoFileClip
from tqdm import tqdm

def process_video(video_path, dur_input):
    clip = VideoFileClip(video_path)

    base_name = os.path.basename(video_path)
    file_name, _ = os.path.splitext(base_name)

    clip_duration = clip.duration
    num_subclips = int(clip_duration / dur_input)

    # Create a ParentFolder if it doesn't exist for this video
    folder_name = file_name

    current_path = os.getcwd()
    saved_folder = os.path.join(current_path, folder_name)

    if not os.path.isdir(saved_folder):
        os.makedirs(saved_folder)

    for i in tqdm(range(num_subclips), desc="Processing Subclips"):
        start = i * dur_input
        end = min((i + 1) * dur_input, clip_duration)
        output_name = f"cutted_{file_name}_part{i}.mp4"
        sub_clip = clip.subclip(start, end)

        if i == num_subclips - 1:
            remaining_duration = clip_duration - end
            if remaining_duration > 0:
                sub_clip = sub_clip.set_duration(sub_clip.duration + remaining_duration)

        output_path = os.path.join(saved_folder, output_name)
        sub_clip.write_videofile(output_path, codec='libx264', verbose=False)

    clip.close()

def browse_video_path():
    video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi")])
    if video_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, video_path)

def process_button_clicked():
    video_path = entry_path.get()
    duration = int(duration_input.get())
    if video_path:
        process_video(video_path, duration)
    else:
        print("Please select a video file.")

# Create the main application window
app = tk.Tk()
app.title("Video Processing Application")

# Create and place GUI components
label_path = tk.Label(app, text="Video Path:")
label_path.pack(pady=10)

entry_path = tk.Entry(app, width=40)
entry_path.pack(pady=10)

browse_button = tk.Button(app, text="Browse", command=browse_video_path)
browse_button.pack(pady=10)

label_duration = tk.Label(app, text="Duration of each video:")
label_duration.pack(pady=10)

duration_input = tk.Entry(app, width=40)
duration_input.pack(pady=10)

process_button = tk.Button(app, text="Process Video", command=process_button_clicked)
process_button.pack(pady=20)

# Start the GUI application
app.mainloop()
