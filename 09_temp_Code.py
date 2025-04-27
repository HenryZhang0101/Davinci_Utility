projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()

timeline_count = proj.GetTimelineCount()

mx = False
# timeline_count = 1 
for timelineid in reversed(range(timeline_count)):
    timeline = proj.GetTimelineByIndex(timelineid+1)
    timeline_name:str = timeline.GetName()
    if timeline_name.startswith("EP "):
        # Offset EP
        offset = int(1) 
        old_ep = int(timeline_name.split(" ")[-1])
        new_ep = old_ep + offset
        new_timeline_name = f"EP {new_ep:2d}"

        timeline.SetName(new_timeline_name)
        print(f"{timeline_name} -> {new_timeline_name}")
