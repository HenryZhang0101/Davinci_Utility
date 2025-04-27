projectManager = resolve.GetProjectManager()
currentProject = projectManager.GetCurrentProject()
currentTimeline = currentProject.GetCurrentTimeline()


print("Current Timeline: ", currentTimeline.GetName())

# Get all clips in the current timeline
clips = currentTimeline.GetItemListInTrack("video", 4)

# get the start frame of the timeline
timelineStartFrame = currentTimeline.GetStartFrame()

for clip in clips:
    # get clip name
    clipName = clip.GetName()

    # get clip duration
    clipDuration = clip.GetDuration() + 1

    sourceStartFrame = clip.GetSourceStartFrame()

    if sourceStartFrame != 0:
        note = f"Clip {clipName} has a start frame of {sourceStartFrame}"
    else:
        note = ""

    # get clip start frame
    startFrame = clip.GetStart() - timelineStartFrame

    # add green marker to the timeline
    success = currentTimeline.AddMarker(startFrame, "Green", clipName, note, clipDuration)
    if success:
        print(f"Added marker to {clipName} at frame {startFrame}")
    # print(f"Clip Name: {clipName} Start Frame: {startFrame}")



# get all markers in the current timeline
# markers = currentTimeline.GetMarkers()
# print("Markers: ", markers)