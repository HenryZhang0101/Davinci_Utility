
import re
projectManager = resolve.GetProjectManager()
currentProject = projectManager.GetCurrentProject()
currentTimeline = currentProject.GetCurrentTimeline()

# ----------------------------------------
# rename subtitle track name


# currentTimeline.SetTrackName("subtitle",1,currentTimeline.GetName())

# ----------------------------------------

# Disable Tracks
# trackType = "audio"
# trackidmin = 5
# trackidmax = 21
# for i in range(trackidmin,trackidmax):
#     currentTimeline.SetTrackEnable(trackType, i, False)


# # Export XML

# path = "D:/Projects/2024_07_17_Say You Remember/10_XML/"
# currentTimeline.Export(path+ currentTimeline.GetName()+'.xml', resolve.EXPORT_FCP_7_XML)

# # ----------------------------------------


MediaPool = currentProject.GetMediaPool()
current_folder = MediaPool.GetCurrentFolder()
clip_list = current_folder.GetClipList()

# clip = clip_list[0]
for clip in clip_list:
    scene = clip.GetMetadata("Scene") 
#     # scene = scene.split("Sc")[0]
#     # scene = scene.split("+")[0]
    if not scene:
        scene = "000"
    scene_number = int(re.findall(r"\d+",scene)[0])
    
    scene_number = f"{scene_number:03d}"
    clip.SetMetadata("Shot",scene_number)
    # print(scene_number)

# for i, clip in enumerate(clip_list):
#     print(clip)
#     sceneNumber = i + 31
#     newName = f"EP {sceneNumber}"
#     test = clip.GetMetadata()
#     print(test)

# for i in range(14):
#     timeline = currentProject.GetTimelineByIndex(i+1)
#     newName = f"EP {i + 45}"
#     timeline.SetName(newName)