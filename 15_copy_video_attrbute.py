projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()
current_timeline = proj.GetCurrentTimeline()

attributes = ["Pan","Tilt","ZoomX","ZoomY"]
source_clips = current_timeline.GetItemListInTrack("video", 2)
target_clips = current_timeline.GetItemListInTrack("video", 1)
for i, clip in enumerate(source_clips):
    for attr in attributes:
        value = clip.GetProperty(attr)
        target_clip = target_clips[i]
        try:
            target_clip.SetProperty(attr,value)
        except:
            print(target_clip.GetName())
    
