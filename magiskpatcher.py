from mp.ui import *

# For pyinstaller
try:
    from mp import splash
except: pass

if __name__ == '__main__':
    root = MagiskPatcherUI()
    root.title(TITLE)
    root.geometry("%dx%d" % (WIDTH, HEIGHT))

    # Fix high dpi
    if osname == 'nt':
        # Tell system using self dpi adapt
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        # Get screen resize scale factor
        scalefactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        root.tk.call('tk', 'scaling', scalefactor/75)

    root.update()
    centerWindow(root)
    #ctk.set_window_scaling(1.25)

    root.mainloop()