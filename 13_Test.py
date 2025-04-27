projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()
current_timeline = proj.GetCurrentTimeline()
MediaPool = proj.GetMediaPool()
current_folder = MediaPool.GetCurrentFolder()


# get all clips in the current timeline
clips = current_timeline.GetItemListInTrack("video", 1)
# get properties of the clip
for clip in clips:
    MediaPool_clip = clip.GetMediaPoolItem()

    print(MediaPool_clip.GetMetadata())
    print("\n")
    print(clip.GetProperty())
    print("\n")
    print("\n")
    
    # print(clip_name,clip_duration,clip_start,clip_end,clip_source_start,clip_source_end)
