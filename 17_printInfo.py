import json

projectManager = resolve.GetProjectManager()
proj = projectManager.GetCurrentProject()
mediaPool = proj.GetMediaPool()


clips = mediaPool.GetSelectedClips()
clips.sort(key=lambda clip: clip.GetName())


projectRoot = r"D:/Projects/2025_01_16_Sharkmob_Exoborne Vegas"
data = {}
for clip in clips:
    metadata = clip.GetMetadata(metadataType=None)
    clipname = clip.GetName()
    cam = metadata["Camera #"]
    card = metadata["Roll Card #"]
    keywords = metadata["Keywords"].split(",")[0]
    sharepoint_path = f"/{cam} cam/{card}/XDROOT/Clip/{clipname}"
    proxypath = f"_in/Proxy/Projects/2025_01_16_Sharkmob_Exoborne Vegas/_in/Footage/{cam} cam/{clipname}"

    if f"{cam} cam" not in data:
        data[f"{cam} cam"] = {}

    # Ensure the nested key exists and is a list
    if keywords not in data[f"{cam} cam" ]:
        data[f"{cam} cam"][keywords] = {}
    
    data[f"{cam} cam"][keywords] [clipname]=sharepoint_path

jsonpath = r"D:/Projects/2025_01_16_Sharkmob_Exoborne Vegas/File_info.json"
with open(jsonpath, "w") as file:
    json.dump(data,file,indent=4)
print(data)


