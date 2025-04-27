
import re
projectManager = resolve.GetProjectManager()
currentProject = projectManager.GetCurrentProject()
currentTimeline = currentProject.GetCurrentTimeline()

MediaPool = currentProject.GetMediaPool()
current_folder = MediaPool.GetCurrentFolder()
clip_list = current_folder.GetClipList()

# clip = clip_list[0]
for clip in clip_list:
    clip_name:str = clip.GetName()
    clip_name = clip_name.replace(" Multicam","")
    clip_scane = clip_name.split("_")[0]
    clip_take = clip_name.split("_")[-1]
    scene_number = int(re.findall(r"\d+",clip_scane)[0])














    # scene = clip.GetMetadata("Scene") 
#     # scene = scene.split("Sc")[0]
#     # scene = scene.split("+")[0]
    
    scene_number = f"{scene_number:03d}"
    print(f"{clip_name} -> {scene_number}")
    clip.SetMetadata("Shot",scene_number)
    clip.SetMetadata("Scene",clip_scane)
    clip.SetMetadata("Take",clip_take)
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