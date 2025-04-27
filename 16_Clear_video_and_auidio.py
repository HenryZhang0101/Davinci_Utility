projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()

timeline_count = proj.GetTimelineCount()

types = ["video","audio"]
# timeline_count = 1 
for timelineid in range(timeline_count):
    timeline = proj.GetTimelineByIndex(timelineid+1)
    timeline_name:str = timeline.GetName()
    if timeline_name.startswith("EP "):
        proj.SetCurrentTimeline(timeline)
        for type in types:
            count = timeline.GetTrackCount(type)
            for i in reversed(range(1,count+1)):
                timeline.DeleteTrack(type, 1)
            items = timeline.GetItemListInTrack(type, 1)
                

