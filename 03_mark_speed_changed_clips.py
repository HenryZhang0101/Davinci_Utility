projectManager = resolve.GetProjectManager()
currentProject = projectManager.GetCurrentProject()
currentTimeline = currentProject.GetCurrentTimeline()

items = currentTimeline.GetItemListInTrack("video", 1)

for item in items:
    duration = item.GetDuration()

    start = item.GetSourceStartFrame()
    end = item.GetSourceEndFrame()
    source_duration = end - start
    threshold = 10
    if(abs(source_duration - duration) > threshold ):
        item.SetClipColor("Tan")
    # print(source_duration)
    # print("~~~~~~~~~~~~")