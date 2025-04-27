projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()

timeline_count = proj.GetTimelineCount()

tracknames = {
    1:"",
    2:"_cn"
}

# timeline_count = 1 
for timelineid in range(timeline_count):
    timeline = proj.GetTimelineByIndex(timelineid+1)
    timeline_name:str = timeline.GetName()
    if timeline_name.startswith("EP "):
        track_count = timeline.GetTrackCount("subtitle")
        for track_id in range(track_count):
            timeline.SetTrackName("subtitle",track_id+1,f"{timeline_name}{tracknames[track_id+1]}")
        