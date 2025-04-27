projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()
current_timeline = proj.GetCurrentTimeline()
MediaPool = proj.GetMediaPool()
current_folder = MediaPool.GetCurrentFolder()


start_frame = "05:00:00:00"
current_timeline.SetCurrentTimecode(start_frame)

clips = current_folder.GetClipList()
for id, clip in enumerate(clips):
    c_name = clip.GetName()


    # insert text
    title = current_timeline.InsertFusionTitleIntoTimeline("Text+")
    title.SetClipColor("Brown")
    fusion_comp = title.GetFusionCompByIndex(1)
    tool = fusion_comp.GetToolList(False,"TextPlus")[1]
    tool.SetInput("StyledText", c_name)


    #insert timeline
    timelineclip = MediaPool.AppendToTimeline(clip)[0]
    
    # in out marker
    timeline_start = current_timeline.GetStartFrame()
    start:int = timelineclip.GetStart() - timeline_start
    dur:int = timelineclip.GetDuration()
    marker = current_timeline.AddMarker(start, "Pink" , c_name,"", dur)