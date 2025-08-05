from tkinter import Tk, filedialog

# Get the Resolve instance
resolve = bmd.scriptapp('Resolve')
fu = resolve.Fusion()
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)

# get current timeline
projectManager = resolve.GetProjectManager()
currentProject = projectManager.GetCurrentProject()
currentTimeline = currentProject.GetCurrentTimeline()



# functions
def get_render_preset() -> list:
        ls:list = currentProject.GetRenderPresetList()
        ls.append("Current Setting")
        ls.reverse()
        
        return ls


def getMarkRange(markers,marker,start, isOffset = "Unchecked"):
    inframe = start + marker
    duration = markers[marker]["duration"]
    outframe = inframe + duration - 1
    if isOffset == "Checked":
        outframe -= 1
    return inframe, outframe

            
def setCurrentRender(inframe,outframe,dir,filename):
      RenderPreset = itm["RenderPreset"].CurrentText
      if RenderPreset != "Current Setting":
        currentProject.LoadRenderPreset(RenderPreset)
      currentProject.SetRenderSettings({
            "SelectAllFrames": False,
            "MarkIn": inframe,
            "MarkOut": outframe,
            "TargetDir": dir,
            "FilenameUses":0,
            "CustomName":filename})
#
# function turn a array of subtitle's start, end and text into a srt file
def create_srt(subtitle_list, file_path, offset=0):
    # get timeline frame rate
    fps = currentTimeline.GetSetting("timelineFrameRate")

    with open(file_path, 'w', encoding='utf-8') as f:
        sub_str = ""
        for i, subtitle in enumerate(subtitle_list):
            start_frame = subtitle.GetStart() + offset
            end_frame = subtitle.GetEnd() + offset
            text = subtitle.GetName()

            # Convert frame to SRT format (HH:MM:SS,frame)
            def frame_to_srt_time(frame, fps):
                total_seconds = frame / fps
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                seconds = int(total_seconds % 60)
                milliseconds = int((total_seconds - int(total_seconds)) * 1000)
                total_seconds = frame / fps
                return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

            start_time_str = frame_to_srt_time(start_frame, fps)
            end_time_str = frame_to_srt_time(end_frame, fps)
            # print srt format
            # print(f"{i + 1}\n{start_time_str} --> {end_time_str}\n{text}\n")

            sub_str += f"{i + 1}\n{start_time_str} --> {end_time_str}\n{text}\n\n"


        f.write(sub_str.strip())  # Remove the last newline character
      
def choose_directory():
    # Create a hidden root window
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    # Open a dialog to choose a directory
    directory = filedialog.askdirectory(title="Select Target Directory")
    root.destroy()
    return directory

# Define the UI layout
layout = ui.VGroup({
    "Spacing": 10
}, [
    ui.Label({"Text":"Render Preset","Weight": 0.1}),
    ui.ComboBox({"ID": "RenderPreset", "Weight": 0.1}),
    ui.Label({"Text":"Filename","Weight": 0.1}),
    # ui.ComboBox({"ID": "Name", "Weight": 0.1}),
    ui.LineEdit({"ID": "Name", "PlaceholderText": r"(you can use %{Marker Id} and %{Marker Name})", "Text": r"%{Marker Id}_%{Marker Name}","Weight": 0.1}),
    ui.CheckBox({"ID": "Offset","Text": "Offset Marker Ending -1", "Weight": 0.1}),
    ui.Label({"Text":"Mark Color","Weight": 0.1}),
    ui.ComboBox({"ID": "color", "Weight": 0.1}),
    ui.Button({"Text": "Add to Render Queue", "ID": "Render", "Weight": 0.1}),
    ui.Button({"Text": "Create Marker", "ID": "createMarker", "Weight": 0.1}),
    ui.Button({"Text": "Export subtitle", "ID": "exportSub", "Weight": 0.1}),
    
    ui.Button({"Text": "Exit", "ID": "Exit", "Weight": 0.1})
    
])




# Create the window
win = disp.AddWindow({"WindowTitle": "Create Jobs From Markers", "ID": "MainWindow", "Geometry": [100, 150, 450, 450]}, layout)

# Access UI elements
itm = win.GetItems()
itm['RenderPreset'].AddItems(list(get_render_preset()))
# itm['Name'].AddItems(["Marker Name", "Custom Name"])

colorset = list()
colorset.append("All")
for marker in currentTimeline.GetMarkers():
    marker_color = currentTimeline.GetMarkers()[marker]["color"]
    if marker_color not in colorset:
        colorset.append(marker_color)
itm['color'].AddItems(list(colorset))



# main function
def _render(ev):
    markers = currentTimeline.GetMarkers()
    color = itm['color'].CurrentText
    
    start = currentTimeline.GetStartFrame()
    dir = choose_directory()
    clip_id = 0
    if dir:
        enable = 0
        for marker in markers:
            if color == "All":
                enable = 1
            else:
                marker_color = markers[marker]["color"]
                if marker_color == color:
                    enable = 1
                else:
                    enable = 0
            if enable == 1:
                clip_id += 1
                inf, outf = getMarkRange(markers, marker, start, itm['Offset'].CheckState)
                print(itm['Offset'].CheckState)
                print(f"inf: {inf}, outf: {outf}")
                if outf > inf + 1:
                    marker_name = markers[marker]['name']

                    
                    naming:str = itm['Name'].Text
                    naming = naming.replace(r"%{Marker Name}", marker_name)
                    naming = naming.replace(r"%{Marker Id}", f"{clip_id:02d}")
                    
                    setCurrentRender(inf,outf,dir,naming)

                    currentProject.AddRenderJob()

                    JobStatus = currentProject.GetRenderJobList()[-1]

                    print(f"Added to Render Queue - {JobStatus["RenderJobName"]} : {naming}\n")
                    for status in JobStatus.keys():
                        print(f"   {status} : {JobStatus[status]}")
                    print("\n")


def _exportSub(ev):
    markers = currentTimeline.GetMarkers()
    # get all subtitle in the current timeline
    subs = currentTimeline.GetItemListInTrack("subtitle", 1)
    color = itm['color'].CurrentText
    
    timeline_start = currentTimeline.GetStartFrame()
    
    dir = choose_directory()
    clip_id = 0
    if dir:
        enable = 0
        for marker in markers:
            if color == "All":
                enable = 1
            else:
                marker_color = markers[marker]["color"]
                if marker_color == color:
                    enable = 1
                else:
                    enable = 0
            if enable == 1:
                clip_id += 1
                inf, outf = getMarkRange(markers, marker, timeline_start)
                if outf > inf + 1:
                    marker_start = marker
                    offset =  timeline_start* -1 - marker_start


                    subtitle_list = []
                    # get all subtitles in the range of the marker
                    for sub in subs:
                        sub_start = sub.GetStart()
                        if sub_start >= inf and sub_start <= outf:
                            subtitle_list.append(sub)
                    # remove appended subtitles from the list
                    for sub in subtitle_list:
                        subs.remove(sub)

                    if len(subtitle_list) > 0:
                        marker_name = markers[marker]['name']

                    
                        naming:str = itm['Name'].Text
                        naming = naming.replace(r"%{Marker Name}", marker_name)
                        naming = naming.replace(r"%{Marker Id}", f"{clip_id+1:03d}")
                        subtile_path = f"{dir}/{naming}.srt"
                    # create srt file
                        create_srt(subtitle_list, subtile_path, offset)
                    

def _createMarker(ev):
    second_layuout = ui.VGroup([
            ui.Label({"Text":"Track Number","Weight": 0.0}),
            ui.ComboBox({"ID": "Track_Number", "Weight": 0.0}),
            ui.Button({"ID" :"createMarker", "Text" : "Create Marker","Weight":0.0}),
            ui.Button({"ID" :"CloseBtn", "Text" : "Close","Weight":0})
        ])
    
    secondary_win = disp.AddWindow({
        "ID" : "createMarker",
        "WindowTitle" : "Create Marker",
        "Geometry": [200, 200, 200, 120]
    },second_layuout)

    
    win_items = secondary_win.GetItems()

    videotrackcount = currentTimeline.GetTrackCount("video")
    videotrack = {}
    for i in range(videotrackcount):
        track_name = currentTimeline.GetTrackName("video", i+1)
        win_items["Track_Number"].AddItem(track_name)
        videotrack[track_name] = i+1






    def on_close(ev):
        secondary_win.Hide()
        return True

    def createMakerOnTimeline(ev):
        track = win_items['Track_Number'].CurrentText
        track_id = videotrack[track]
        clips = currentTimeline.GetItemListInTrack("video", track_id)
        for i, clip in enumerate(clips):
            timelineStart = currentTimeline.GetStartFrame()
            markerStart = clip.GetEnd() - timelineStart
            if i == len(clips) - 1:
                markerEnd = currentTimeline.GetEndFrame() - 1 
            else:
                markerEnd = clips[i+1].GetStart() - 1
            markerEnd = markerEnd - timelineStart
            # print("i:", i)
            fusion_comp_count = clip.GetFusionCompCount()
            if fusion_comp_count == 0:
                continue
            else:
                comp = clip.GetFusionCompByIndex(1)
                tool = comp.GetToolList(False,"TextPlus")[1]
                title = tool.GetInput("StyledText")
            duration = markerEnd - markerStart + 1
            currentTimeline.AddMarker(markerStart, "Pink", title, "", duration)
            print(f"Title: {title}, start: {markerStart}, end: {markerEnd}")


            
            

    secondary_win.On["CloseBtn"].Clicked = on_close
    secondary_win.On["createMarker"].Clicked = createMakerOnTimeline
    secondary_win.Show()

    
        


def _exit(ev):
    disp.ExitLoop()


win.On["Render"].Clicked = _render
win.On["exportSub"].Clicked = _exportSub
win.On["createMarker"].Clicked = _createMarker
win.On["Exit"].Clicked = _exit

# Show the window
win.Show()

# Keep the window running
disp.RunLoop()

# Clean up after closing
win.Hide()
