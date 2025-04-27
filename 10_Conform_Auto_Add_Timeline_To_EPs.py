import pyautogui

projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()
mediaPool = proj.GetMediaPool()


def foundConformed(timelineName):
    timeline_count = proj.GetTimelineCount()
    for timelineid in range(timeline_count):
        timeline = proj.GetTimelineByIndex(timelineid+1)
        timeline_name:str = timeline.GetName()
        if timeline_name == timelineName:
            return timelineid+1
        # print("no Conformed Timeline")
#{96.0: {color: Green, duration: 1.0, note: , `name`: 'Marker 1', `customData`:}, ...}
def getMarkerInOut(markers:dict,start:int):
    markersDict = {}

    for marker in markers.keys():
        startFrame:int = int(marker) + start
        endFrame = startFrame + int(markers[marker]["duration"]) - 1
        markersDict[markers[marker]['name']] = [startFrame,endFrame]

    return markersDict


timelineName = mediaPool.GetSelectedClips()[0].GetName()


timeline_idx = foundConformed(timelineName)
print(timelineName)
conformedTimeline = proj.GetTimelineByIndex(timeline_idx)
markers = conformedTimeline.GetMarkers()
start = conformedTimeline.GetStartFrame()
markersDict = getMarkerInOut(markers,0)
print(markersDict)
timeline_count = proj.GetTimelineCount()
# timeline_count = 0
for timelineid in range(timeline_count):
    timeline = proj.GetTimelineByIndex(timelineid+1)
    timeline_name:str = timeline.GetName()
    if timeline_name.startswith("EP "):
        success = proj.SetCurrentTimeline(timeline)
        if success:
            conformedTimeline.SetMarkInOut(markersDict[timeline_name][0], markersDict[timeline_name][1], type=all) 
        
            
            audioTrackNum:int = timeline.GetTrackCount("audio")
            for track in range(1,20):
                timeline.SetTrackEnable("audio", track, False) 

            # Add 4 audio track
            # trackName = ["MIX","DX","MX","FX"]
            # mixTrackID = audioTrackNum + 1
            # for newTrack in range(4):
            #     timeline. AddTrack("audio", {'audioType':"stereo"})
            #     newTrackID = audioTrackNum + newTrack + 1
            #     timeline.SetTrackName("audio", newTrackID, trackName[newTrack])     
                

            # set current timecode
            timeline.SetCurrentTimecode("00:00:00:00")
            pyautogui.hotkey('f12') 