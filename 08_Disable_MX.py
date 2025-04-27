projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()

timeline_count = proj.GetTimelineCount()

enable = False
# timeline_count = 1 
for timelineid in range(timeline_count):
    timeline = proj.GetTimelineByIndex(timelineid+1)
    timeline_name:str = timeline.GetName()
    if timeline_name.startswith("EP "):
        proj.SetCurrentTimeline(timeline)


        for i in range(1,22):

            timeline.SetTrackEnable("audio", i, enable)
        print(f"{timeline_name}:{enable}")
