projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()

timeline_count = proj.GetTimelineCount()
# timeline_count = 1 
for timelineid in range(timeline_count):
    timeline = proj.GetTimelineByIndex(timelineid+1)
    timeline_name:str = timeline.GetName()
    if timeline_name.startswith("EP "):
        timeline.SetStartTimecode("00:00:00:00")
        print(f"set {timeline_name} timecode: 00:00:00:00")

        
