import json
import os
import csv

projectManager = resolve.GetProjectManager()
currentProject = projectManager.GetCurrentProject()
currentTimeline = currentProject.GetCurrentTimeline()

# get all markers in the timeline
markers = currentTimeline.GetMarkers()

# convert markers to list
markers_list = list(markers.keys())
# print(markers_list)

# get all clips in the timeline
clips = currentTimeline.GetItemListInTrack("video", 1)
plate_clips = currentTimeline.GetItemListInTrack("video", 4)



# get num of all markers
# num_markers = len(markers)
num_clips = len(clips)

# print(f"Number of markers: {num_markers}")
# print(f"Number of clips: {num_clips}")

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

# create header for csv file

header = ["Clip Id", "Source Clip Name", "Plate Name", "Color", "Clip Frames", "Record In", "Record Out", "Source In", "Source Out", "Note"]
table = [header]
dictory = dict()
total_clips = 0
for i in range(num_clips):
    plate_name = markers[markers_list[i]]["name"]
    print(i)
    marker_color = markers[markers_list[i]]["color"]
    if marker_color == "Red":
        plate_name = "plate not found"
    
    source = clips[i]
    id = f"{i+1:04d}"
    clip_duration = source.GetDuration()
    end = source.GetEnd()
    start = source.GetStart()
    source_start = source.GetSourceStartFrame()
    source_end = source.GetSourceEndFrame()
    notes = list()
    notes.append(markers[markers_list[i]]["note"])
    enable = source.GetClipEnabled()
    if not enable:
        notes.append("This clip did not exported since it has duplicate clip")
    note = " | ".join(notes)

    # get the color of the marker
    

    # create content for csv file
    content = [id, source.GetName(), plate_name, marker_color, clip_duration, frame_to_timecode(start), frame_to_timecode(end), frame_to_timecode(source_start), frame_to_timecode(source_end), note]
    dictory[id] = {
        "name": source.GetName(),
        "plate": plate_name,
    }
    table.append(content)


    
    

# add
print(table)
# write to csv file
path = os.path.join("D:/Projects/2025_04_02_The Remedy/_out", "report_v02.csv")
with open(path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(table)

# write to json file
with open(path.replace(".csv", ".json"), "w") as f:
    json.dump(dictory, f, indent=4)
    