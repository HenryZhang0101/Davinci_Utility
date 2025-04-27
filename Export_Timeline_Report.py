import json
import os
import csv
from tkinter import Tk, filedialog

# header for csv file
header = ["Clip Id", "Source Clip Name", "Clip Color", "Total Frames", "Record In", "Record Out", "Source In", "Source Out", "Notes"]

# create a function to ask user to save the file
def save_file():
    # Create a hidden root window
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    # Open a dialog to choose a directory
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save as CSV")
    root.destroy()
    return file_path

# create a function to convert frame to timecode
def frame_to_timecode(frame_number, fps=24):
    """
    Convert a frame number to timecode (HH:MM:SS:FF)

    Parameters:
        frame_number (int): The frame number to convert.
        fps (float): Frames per second.

    Returns:
        str: Timecode in the format HH:MM:SS:FF
    """
    total_seconds = int(frame_number // fps)
    frames = int(frame_number % fps)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

projectManager = resolve.GetProjectManager()
currentProject = projectManager.GetCurrentProject()
currentTimeline = currentProject.GetCurrentTimeline()

clips = list()

# get all tracks in the timeline
tracks_num = currentTimeline.GetTrackCount("video")
for i in range(1, tracks_num+1):
    trackenable = currentTimeline.GetIsTrackEnabled("video", i)
    if trackenable:
        clips.extend(currentTimeline.GetItemListInTrack("video", i))

# sort clips by start frame
clips.sort(key=lambda x: x.GetStart())
num_clips = len(clips)

table = [header]
total_clips = 0
clip_id = 0
for i in range(num_clips):
    
        
    source = clips[i]
    enable = source.GetClipEnabled()
    if not enable:
        continue
    total_clips += 1
    clip_id += 1

    clip_color = source.GetClipColor()
    # print(clip_color)
    clip_duration = source.GetDuration()
    end = source.GetEnd()
    start = source.GetStart()
    source_start = source.GetSourceStartFrame()
    source_end = source.GetSourceEndFrame()

    notes = list()
    markers = source.GetMarkers()
    for i, marker in enumerate(markers):
        # marker_color = markers[marker]["color"]
        marker_name = markers[marker]["name"]
        marker_start = marker - source_start
        marker_note = markers[marker]["note"]
        notes.append (f"Frame {marker_start} - {marker_name} : {marker_note}")
    note = "\n".join(notes)
    # print(markers)

   

    # create content for csv file
    content = [clip_id, source.GetName(),  clip_color, clip_duration, frame_to_timecode(start), frame_to_timecode(end), frame_to_timecode(source_start), frame_to_timecode(source_end), note]
    table.append(content)


file = save_file()
# check the dir of the file exists
dir = os.path.dirname(file)
if not os.path.exists(dir):
    os.makedirs(dir)


with open(file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(table)


    