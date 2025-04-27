projectManager = resolve.GetProjectManager()
currentProject = projectManager.GetCurrentProject()
currentTimeline = currentProject.GetCurrentTimeline()

# audio
preset = {
    "DX" : 9,
    "MX" : 3,
    "FX" : 5
}
currentTimeline.SetTrackName("audio",1,"DX")
trackcount =1 
for audiotype in preset:
    for i in range(trackcount,trackcount+preset[audiotype]):
        currentTimeline.AddTrack("audio","mono")
        currentTimeline.SetTrackName("audio",i+1,audiotype)
    trackcount = currentTimeline.GetTrackCount("audio")