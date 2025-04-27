from datetime import datetime
projectManager = resolve.GetProjectManager()
currentProject = projectManager.GetCurrentProject()

for i in range(23):
    timeline = currentProject.GetTimelineByIndex(i+1)
    date = datetime.today().strftime("%m%d")
    newname = timeline.GetName() + f"_{date}"
    timeline.DuplicateTimeline(newname)