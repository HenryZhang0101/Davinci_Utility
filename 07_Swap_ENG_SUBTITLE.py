projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()

timeline_count = proj.GetTimelineCount()

Eng = False
# timeline_count = 1 
for timelineid in range(timeline_count):
    timeline = proj.GetTimelineByIndex(timelineid+1)
    timeline_name:str = timeline.GetName()
    if timeline_name.startswith("EP "):
        proj.SetCurrentTimeline(timeline)
        if Eng:
            timeline.SetTrackEnable("subtitle", 1, True)
            timeline.SetTrackEnable("subtitle", 2, False)
            print("ENG Sub")
        else:
            timeline.SetTrackEnable("subtitle", 1, False)
            timeline.SetTrackEnable("subtitle", 2, True)
            print("CN SUB")
        