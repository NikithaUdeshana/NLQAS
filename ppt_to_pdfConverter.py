import os
import glob
import win32com.client
import win32gui
import win32con
import pythoncom

dir = r"" + os.getcwd() + "/test files"
output_dir = r"" + os.getcwd() + "/test files"

def ppt_to_pdf(files, formatType = 32):
    pythoncom.CoInitialize()
    powerpoint = win32com.client.Dispatch("Powerpoint.Application")
    powerpoint.Visible = 1
    hwnd = win32gui.FindWindow(None, "Powerpoint")
    for filename in files:
        new_name = os.path.splitext(filename)[0] + ".pdf"
        new_name = os.path.split(new_name)[1]
        new_name = os.path.join(output_dir, new_name)
        deck = powerpoint.Presentations.Open(filename)
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        deck.SaveAs(new_name, formatType)
        deck.Close()
    powerpoint.Quit()

# files = glob.glob(os.path.join(dir, "*.ppt*"))
# print(files)