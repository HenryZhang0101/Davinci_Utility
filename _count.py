projectManager = resolve.GetProjectManager()
currentProject = projectManager.GetCurrentProject()
currentTimeline = currentProject.GetCurrentTimeline()


# get all markers in the timeline
markers = currentTimeline.GetMarkers()

# get num of all markers
num_markers = len(markers)

# get all clips in the timeline
clips = currentTimeline.GetItemListInTrack("video", 1)
num_clips = len(clips)

print(f"Number of markers: {num_markers}")
print(f"Number of clips: {num_clips}")