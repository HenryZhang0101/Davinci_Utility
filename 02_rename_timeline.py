from tkinter import Tk, filedialog
# Get the Resolve instance
resolve = bmd.scriptapp('Resolve')
fu = bmd.scriptapp('Fusion')
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)

# get current timeline
projectManager = resolve.GetProjectManager()
currentProject = projectManager.GetCurrentProject()
mediapool = currentProject.GetMediaPool()


def choose_directory():
    # Create a hidden root window
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    # Open a dialog to choose a directory
    directory = filedialog.askopenfilename(title="Choose template")
    root.destroy()
    return directory



layout = ui.VGroup([
    ui.HGroup({'Weight': 5},[
        ui.Label({"Text":"Start EP"}),
        ui.SpinBox({"ID": "start", "Weight": 0.9}),
    ]),
    ui.HGroup({'Weight': 5},[
        ui.Label({"Text":"Total EP"}),
        ui.SpinBox({"ID": "total", "Weight": 0.9}),
    ]),
    
    ui.Button({"Text": "Create Timeline", "ID": "craete", "Weight": 0.1}),
    ui.Button({"Text": "Exit", "ID": "Exit", "Weight": 0.1})
])



# Create the window
win = disp.AddWindow({"WindowTitle": "Create Jobs From Markers", "ID": "MainWindow", "Geometry": [100, 150, 300, 210]}, layout)





# main function
def _render(ev):

    path = choose_directory()
    mediapool.ImportTimelineFromFile(path)

    # Access UI elements
    itm = win.GetItems()
    start = itm["start"].Value
    total = itm["total"].Value + 1




    for i in range(total):
        timeline = currentProject.GetTimelineByIndex(i+1)
        newName = f"EP {i + start}"
        timeline.SetName(newName)
        if i+1 < total:
            timeline.DuplicateTimeline()

def _exit(ev):
    disp.ExitLoop()


win.On["craete"].Clicked = _render
win.On["Exit"].Clicked = _exit

# Show the window
win.Show()

# Keep the window running
disp.RunLoop()

# Clean up after closing
win.Hide()















