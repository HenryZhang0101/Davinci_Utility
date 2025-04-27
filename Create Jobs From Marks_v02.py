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


def getMarkRange(markers,marker,start):
    inframe = start + marker
    duration = markers[marker]["duration"]
    outframe = inframe + duration
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
    ui.Label({"Text":"Render Preset"}),
    ui.ComboBox({"ID": "RenderPreset", "Weight": 0.1}),
    ui.Label({"Text":"Filename"}),
    # ui.ComboBox({"ID": "Name", "Weight": 0.1}),
    ui.LineEdit({"ID": "Name", "PlaceholderText": r"(you can use %{Marker Id} and %{Marker Name})", "Text": r"%{Marker Id}_%{Marker Name}"}),
    ui.Label({"Text":"Mark Color"}),
    ui.ComboBox({"ID": "color", "Weight": 0.1}),
    ui.Button({"Text": "Add to Render Queue", "ID": "Render", "Weight": 0.1}),
    ui.Button({"Text": "Exit", "ID": "Exit", "Weight": 0.1})
    
])




# Create the window
win = disp.AddWindow({"WindowTitle": "Create Jobs From Markers", "ID": "MainWindow", "Geometry": [100, 150, 450, 310]}, layout)

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
    color = itm['color'].CurrentText
    markers = currentTimeline.GetMarkers()
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
                inf, outf = getMarkRange(markers, marker, start)
                if outf > inf + 1:
                    marker_name = markers[marker]['name']

                    
                    naming:str = itm['Name'].Text
                    naming = naming.replace(r"%{Marker Name}", marker_name)
                    naming = naming.replace(r"%{Marker Id}", f"{clip_id+1:03d}")
                    
                    setCurrentRender(inf,outf,dir,naming)

                    currentProject.AddRenderJob()

                    JobStatus = currentProject.GetRenderJobList()[-1]

                    print(f"Added to Render Queue - {JobStatus["RenderJobName"]} : {naming}\n")
                    for status in JobStatus.keys():
                        print(f"   {status} : {JobStatus[status]}")
                    print("\n")

def _exit(ev):
    disp.ExitLoop()


win.On["Render"].Clicked = _render
win.On["Exit"].Clicked = _exit

# Show the window
win.Show()

# Keep the window running
disp.RunLoop()

# Clean up after closing
win.Hide()
