projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()



# config subtitle 
charPerLine = 40
AutoCaptionSetting = {
    resolve.SUBTITLE_LANGUAGE: resolve.AUTO_CAPTION_ENGLISH,
    resolve.SUBTITLE_CAPTION_PRESET: resolve.AUTO_CAPTION_SUBTITLE_DEFAULT,
    resolve.SUBTITLE_CHARS_PER_LINE: charPerLine,
    resolve.SUBTITLE_LINE_BREAK: resolve.AUTO_CAPTION_LINE_SINGLE,
    resolve.SUBTITLE_GAP: 0
}


timeline_count = proj.GetTimelineCount()
# timeline_count = 1 
for timelineid in range(timeline_count):
    timeline = proj.GetTimelineByIndex(timelineid+1)
    timeline_name:str = timeline.GetName()
    if timeline_name.startswith("EP "):
        success = timeline.CreateSubtitlesFromAudio(AutoCaptionSetting)
        if success:
            print(f"Created subtitle for {timeline_name}!")
        else:
            print(f"failed")