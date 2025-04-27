projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()
mediapool = proj.GetMediaPool()
timeline_count = proj.GetTimelineCount()


# get place holder

placeholder = mediapool.GetSelectedClips()[0]


# timeline_count = 1 
for timelineid in range(timeline_count):
    timeline = proj.GetTimelineByIndex(timelineid+1)
    timeline_name:str = timeline.GetName()
    if timeline_name.startswith("EP "):
        proj.SetCurrentTimeline(timeline)

        # get audio tracks 
        tracknum:int = timeline.GetTrackCount("audio")
        tracknum = min(tracknum,18)
        for trackid in range(tracknum):
            items = timeline.GetItemListInTrack("audio", trackid + 1)
            if len(items) == 0:
                timeline.SetCurrentTimecode("00:00:00:00")
                item = mediapool.AppendToTimeline([{
                    "mediaPoolItem":placeholder,
                    "startFrame":0,
                    "recordFrame":0,
                    "mediaType":2,
                    "trackIndex":trackid + 1
                    }])[0]
                item.SetClipColor("Chocolate")
                