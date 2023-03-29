import subprocess
import pygetwindow as gw
from screeninfo import get_monitors
import TouchPortalAPI
from TouchPortalAPI import TYPES
import sys
from ctypes import windll, wintypes
import win32gui
import win32api
import ctypes
from collections import namedtuple
import pywinauto
from time import sleep
from ctypes.wintypes import tagPOINT
from time import sleep
from threading import Thread

user32 = ctypes.WinDLL('user32')
WindowInfo = namedtuple('WindowInfo', 'pid title')
MonitorMode = {
    "MONITOR_DEFAULTTONULL": 0,
    "MONITOR_DEFAULTTOPRIMARY": 1,
    "MONITOR_DEFAULTTONEAREST": 2
}

WNDENUMPROC = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,    
    wintypes.LPARAM
)

processBlocklist = [
    "PopupHost",
    "NVIDIA GeForce Overlay",
    "NVIDIA GPU Activity\n",
    "Windows Input Experience"
]

def list_windows():
    OptionList = []
    @WNDENUMPROC
    def enum_proc(hWnd, lParam):
        if user32.IsWindowVisible(hWnd):
            length = user32.GetWindowTextLengthW(hWnd) + 1
            title = ctypes.create_unicode_buffer(length)
            user32.GetWindowTextW(hWnd, title, length)
            if title.value != "":
                OptionList.append(title.value)
        return True
    user32.EnumWindows(enum_proc, 0)
    ProcessList = list(set(sorted(OptionList)))
    return [process for process in ProcessList if not process in processBlocklist]

def getMonitorFriendlyName(): # Not sure how to use this correctly bc theres no way for me to verify which is which example \\\\.\\DISPLAY0 
    systemencoding = windll.kernel32.GetConsoleOutputCP()
    systemencoding = f"cp{systemencoding}"

    cmd = "$Monitors = Get-WmiObject WmiMonitorID -Namespace root\wmi; ForEach ($Monitor in $Monitors) { [System.Text.Encoding]::ASCII.GetString($Monitor.UserFriendlyName) }"
    result = subprocess.Popen(["powershell", "-Command", cmd],stdout=subprocess.PIPE, shell=True).communicate()[0]
    return [monitorname.replace("\x00", "") for monitorname in result.decode().strip().split("\r\n")]

def get_desktop():
    display = []
    monitor = get_monitors()
    #monitorName = getMonitorFriendlyName()[::-1]
    for x in range(len(monitor)):
        display.append({f"Display-{x}": {"width": monitor[x].width, "height": monitor[x].height, "x": monitor[x].x, "y": monitor[x].y}})
    return display

def Move_Window(Title, Display, Where, resize=False):
    try:
        Window = gw.getWindowsWithTitle(Title)[0]
    except IndexError:
        return
    Monitor = get_desktop()
    print(Monitor)
    Indexnum = []
    for x in Monitor:
        Indexnum.append(list(x.keys())[0])
    if Window.isMinimized:
        try:
            Window.restore()
        except:
            print('No Perm')
    if Display in Indexnum:
        indexnum = Indexnum.index(Display)
        point = tagPOINT(Monitor[indexnum][Display]['x'],Monitor[indexnum][Display]['y'])
        monitor_area = win32api.GetMonitorInfo(user32.MonitorFromPoint(point, MonitorMode.get("MONITOR_DEFAULTTONEAREST")))
        print(monitor_area)
        width = abs(monitor_area["Work"][2]-monitor_area["Work"][0])
        height = abs(monitor_area["Work"][3]-monitor_area["Work"][1])
        print(monitor_area)
        if resize == "True":
            try:
                Window.resizeTo(int(width/2), int(height/2))
            except Exception as e:
                print(e)
                print('No Perm Reize')
        if Where == "Top Left":
            try:
                Window.moveTo(monitor_area['Work'][0]-7, monitor_area['Work'][1]-7)
                print("Top Left Moved to:",(monitor_area['Work'][0]-7, monitor_area['Work'][1]-7))
            except Exception:
                print('No perm Top Left')
        elif Where == "Top Right":
            try:
                Window.moveTo(int(monitor_area['Work'][2]-Window.width)+7, int(monitor_area['Work'][1]))
                print("Top Right Moved to:",(int(monitor_area['Work'][2]-Window.width)+7, int(monitor_area['Work'][1])))
            except Exception:
                print('No perm Top Right')
        elif Where == "Top Middle":
            try:
                Window.moveTo(int(monitor_area['Work'][0]+(width-Window.width)/2), monitor_area['Work'][1]-7)
                print("Top Middle Moved To:",(int(monitor_area['Work'][0]+(width-Window.width)/2), monitor_area['Work'][1]-7))
            except Exception as e:
                print(e)
        elif Where == "Bottom Middle":
            try:
                Window.moveTo(int(monitor_area['Work'][0]+(width-Window.width)/2), int(monitor_area['Work'][3]-Window.height)+7)
                print("Bottom Middle Moved To:",(int(monitor_area['Work'][0]+(width-Window.width)/2), int(monitor_area['Work'][3]-Window.height)+7))
            except Exception as e:
                print(e)
        elif Where == "Left Middle":
            try:
                Window.moveTo(monitor_area['Work'][0]-7, int((monitor_area['Work'][1]+(height-Window.height))/2))
                print("Left Middle Moved To:",(monitor_area['Work'][0]-7, int((monitor_area['Work'][1]+(height-Window.height))/2)))
            except Exception as e:
                print(e)
        elif Where == "Right Middle":
            try:
                Window.moveTo(int(monitor_area['Work'][2]-Window.width)+7, int((monitor_area['Work'][1]+(height-Window.height))/2))
                print("Right Middle Moved To:",(int(monitor_area['Work'][2]-Window.width)+7, int((monitor_area['Work'][1]+(height-Window.height))/2)))
            except Exception as e:
                print(e)
        elif Where == "Bottom Left":
            try:
                Window.moveTo(int(monitor_area['Work'][0])-7, int(monitor_area['Work'][3]-Window.height)+7)
                print("Bottom Left Moved To:",(int(monitor_area['Work'][0])-7, int(monitor_area['Work'][3]-Window.height)+7))
            except Exception as e:
                print(e)
        elif Where == "Buttom Right":
            try:
                Window.moveTo(int(monitor_area['Work'][2]-Window.width)+7, int(monitor_area['Work'][3]-Window.height)+7)
                print("Bottom Right Moved To:",(int(monitor_area['Work'][2]-Window.width)+7, int(monitor_area['Work'][3]-Window.height)+7))
            except Exception as e:
                print(e)
        elif Where == "Center":
            try:
                Window.moveTo(int(monitor_area['Work'][0]+(width-Window.width)/2),int((monitor_area['Work'][1]+(height-Window.height))/2))
                print("Center Moved to:",(int(monitor_area['Work'][0]+(width-Window.width)/2),int((monitor_area['Work'][1]+(height-Window.height))/2)))
            except Exception as e:
                print(e)

def ResizeTo(Title, width, height):
    try:
        Window = gw.getWindowsWithTitle(Title)[0]
    except IndexError:
        return
    if Window.isMinimized:
        try:
            Window.restore()
        except:
            print('No Perm')
    try:
        Window.resizeTo(int(width),int(height))
    except:
        print('No Perm')

def MovebyXY(Title, X,Y):
    try:
        Window = gw.getWindowsWithTitle(Title)[0]
    except IndexError:
        return
    if Window.isMinimized:
        try:
            Window.restore()
        except:
            pass
    try:
        Window.move(int(X),int(Y))
    except:
        print('No Perm')

def increAndDecreResize(Title, width, height):
    try:
        Window = gw.getWindowsWithTitle(Title)[0]
    except IndexError:
        return
    if Window.isMinimized:
        try:
            Window.restore()
        except:
            print('No Perm')
    try:
        Window.resize(int(width),int(height))
    except:
        print('No perm')

def focus_to_window(window_title=None):
    window = gw.getWindowsWithTitle(window_title)[0]
    if window.isActive == False:
        try:
            pywinauto.application.Application().connect(handle=window._hWnd).top_window().set_focus()
        except:
            print('No perm')

def SysAction(Title, Action):
    try:
        Window = gw.getWindowsWithTitle(Title)[0]
        print(Window)
    except IndexError:
        return
    if Action == "maximize":
        try:
            Window.maximize()
        except:
            print('no perm')
    elif Action == "minimize":
        try:
            Window.minimize()
        except:
            print('No Perm')
    elif Action == "restore":
        try:
            Window.restore()
        except:
            print('No perm')
    elif Action == "focus":
        try:
            focus_to_window(Title)
        except:
            return
    elif Action == "close":
        try:
            Window.close()
        except:
            print('No Perm')
    
def CustomAction(Title, x, y, width, hight):
    try:
        Window = gw.getWindowsWithTitle(Title)[0]
    except IndexError:
        return
    if Window.isMinimized:
        Window.restore()
    Window.moveTo(int(x),int(y))
    Window.resizeTo(int(width),int(hight))


# Setup
TPClient = TouchPortalAPI.Client('WindowMover')
global running
running = False
runOnce = False

def stateUpdate():
    global runOnce

    if not runOnce:
        print("running once")
        TPClient.choiceUpdate("KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Displays", [])
        TPClient.choiceUpdate('KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Advanced.Displays', [])

        TPClient.choiceUpdate("KillerBOSS.TP.Plugins.WindowMover.customMove.Window", [])
        runOnce = True

    while running:
        monitor = [list(each.keys())[0].rstrip() for each in get_desktop()]

        if TPClient.choiceUpdateList.get("KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Displays") != monitor:
            TPClient.choiceUpdate("KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Displays", monitor)
            TPClient.choiceUpdate('KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Advanced.Displays', monitor)
            print('updating Display List', monitor)

        if TPClient.choiceUpdateList.get("KillerBOSS.TP.Plugins.WindowMover.customMove.Window") != (processWindow := list_windows()):
            TPClient.choiceUpdate("KillerBOSS.TP.Plugins.WindowMover.customMove.Window", processWindow)
            print("Updating process list", processWindow)

        try:
            currentFocusedWindow = gw.getActiveWindowTitle()
            TPClient.stateUpdate('KillerBOSS.TP.Plugins.WindowMover.states.ActiveWindow', currentFocusedWindow)
            WindowInfo = gw.getWindowsWithTitle(currentFocusedWindow)[0]
            TPClient.stateUpdateMany([
            {
                "id": 'KillerBOSS.TP.Plugins.WindowMover.states.ActiveWindow.X',
                "value": str(WindowInfo.top)
            },
            {
                "id": 'KillerBOSS.TP.Plugins.WindowMover.states.ActiveWindow.Y',
                "value": str(WindowInfo.left)
            },
            {
                "id": 'KillerBOSS.TP.Plugins.WindowMover.states.ActiveWindow.width',
                "value": str(WindowInfo.width)
            },
            {
                "id": 'KillerBOSS.TP.Plugins.WindowMover.states.ActiveWindow.height',
                "value": str(WindowInfo.height)
            },
            {
                "id": 'KillerBOSS.TP.Plugins.WindowMover.states.isCurrentWindowMaximized',
                "value": str(WindowInfo.isMaximized)
            },
            {
                "id": 'KillerBOSS.TP.Plugins.WindowMover.states.isCurrentWindowminimize',
                "value": str(WindowInfo.isMinimized)
            },
            {
                "id": 'KillerBOSS.TP.Plugins.WindowMover.states.isCurrentWindowActive',
                "value": str(WindowInfo.isActive)
            }
        ])
        except (IndexError,AttributeError,ConnectionResetError):
            pass

        sleep(0.2) # add delay

@TPClient.on(TYPES.onAction)
def ManageAction(data):
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.Windowpresets":
        if data['data'][1]['value'] is not '':
            Move_Window(data['data'][1]['value'], data['data'][2]['value'], data['data'][0]['value'],data['data'][3]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.ResizeTo":
        if data['data'][0]['value'] is not '': 
            ResizeTo(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease":
        if data['data'][1]['value'] is not '':
            if data['data'][0]['value'] == "Increase":
                increAndDecreResize(data['data'][1]['value'], int(data['data'][2]['value']), int(data['data'][3]['value']))
            elif data['data'][0]['value'] == "Decrease":
                increAndDecreResize(data['data'][1]['value'], -int(data['data'][2]['value']), -int(data['data'][3]['value']))
    
    if data['actionId'] == 'KillerBOSS.TP.Plugins.WindowMover.SysActions':
        if data['data'][1]['value'] is not '':
            SysAction(data['data'][1]['value'],data['data'][0]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.MoveByXandY":
        if data['data'][0]['value'] is not '':
            if data['data'][3]['value'] == "Increase":
                MovebyXY(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
            elif data['data'][3]['value'] == "Decrease":
                MovebyXY(data['data'][0]['value'], -int(data['data'][1]['value']), -int(data['data'][2]['value']))
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.customMove":
        if data['data'][0]['value'] != '' and data['data'][1]['value'] != '' and data['data'][2]['value'] != '' and data['data'][3]['value'] != '' and data['data'][4]['value'] != '':
            CustomAction(data['data'][0]['value'],data['data'][1]['value'],data['data'][2]['value'],data['data'][3]['value'],data['data'][4]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.Advanced.MoveByXandY":
        if data['data'][0]['value'] is not "" and data['data'][3]['value'] == 'Increase':
            MovebyXY(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
        elif data['data'][0]['value'] is not "" and data['data'][3]['value'] == "Decrease":
            MovebyXY(data['data'][0]['value'], -int(data['data'][1]['value']), -int(data['data'][2]['value']))
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease.Advanced":
        if data['data'][1]['value'] is not "" and data['data'][0]['value'] == 'Increase':
            increAndDecreResize(data['data'][1]['value'], data['data'][2]['value'], data['data'][3]['value'])
            sleep(0.02)
        elif data['data'][1]['value'] is not "" and data['data'][0]['value'] == "Decrease":
            increAndDecreResize(data['data'][1]['value'], -int(data['data'][2]['value']), -int(data['data'][3]['value']))
            sleep(0.02)
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.Advanced.Windowpresets":
        if data['data'][1]['value'] is not "":
            Move_Window(data['data'][1]['value'],data['data'][2]['value'],data['data'][0]['value'], data['data'][3]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.ResizeTo.Advanced":
        if data['data'][0]['value'] is not '': 
            ResizeTo(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.Advanced.customMove":
        if data['data'][0]['value'] is not '':
            CustomAction(data['data'][0]['value'],data['data'][1]['value'],data['data'][2]['value'],data['data'][3]['value'],data['data'][4]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.SysActions.Advanced":
        if data['data'][1]['value'] is not '':
            SysAction(data['data'][1]['value'], data['data'][0]['value'])

@TPClient.on(TYPES.onListChange)
def listChange(data):
    if data['listId'] == "KillerBOSS.TP.Plugins.WindowMover.customMove.Window":
        try:
            findwindow = win32gui.FindWindow(None,data['value'])
            rect = win32gui.GetWindowRect(findwindow)
        except KeyError:
            return
        TPClient.choiceUpdate("KillerBOSS.TP.Plugins.WindowMover.customMove.X", [str(rect[0])])
        TPClient.choiceUpdate("KillerBOSS.TP.Plugins.WindowMover.customMove.Y", [str(rect[1])])
        TPClient.choiceUpdate("KillerBOSS.TP.Plugins.WindowMover.customMove.width", [str(rect[2]-rect[0])])
        TPClient.choiceUpdate("KillerBOSS.TP.Plugins.WindowMover.customMove.height", [str(rect[3]-rect[1])])

@TPClient.on(TYPES.onHold_down)
def holdAction(data):
    while True:
        if TPClient.isActionBeingHeld('KillerBOSS.TP.Plugins.WindowMover.MoveByXandY'):
            if data['data'][3]['value'] == "Increase":
                MovebyXY(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
                sleep(0.02)
            elif data['data'][3]['value'] == "Decrease":
                MovebyXY(data['data'][0]['value'], -int(data['data'][1]['value']), -int(data['data'][2]['value']))
                sleep(0.02)

        elif TPClient.isActionBeingHeld('KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease'):
            if data['data'][0]['value'] == "Increase":
                increAndDecreResize(data['data'][1]['value'], int(data['data'][2]['value']), int(data['data'][3]['value']))
                sleep(0.02)
            if data['data'][0]['value'] == "Decrease":
                increAndDecreResize(data['data'][1]['value'], -int(data['data'][2]['value']), -int(data['data'][3]['value']))
                sleep(0.02)
        elif TPClient.isActionBeingHeld('KillerBOSS.TP.Plugins.WindowMover.Advanced.MoveByXandY'):
            if data['data'][0]['value'] is not "" and data['data'][3]['value'] == 'Increase':
                MovebyXY(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
                sleep(0.02)
            elif data['data'][0]['value'] is not "" and data['data'][3]['value'] == "Decrease":
                MovebyXY(data['data'][0]['value'], -int(data['data'][1]['value']), -int(data['data'][2]['value']))
                sleep(0.02)
        elif TPClient.isActionBeingHeld('KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease.Advanced'):
            if data['data'][1]['value'] is not "" and data['data'][0]['value'] == 'Increase':
                increAndDecreResize(data['data'][1]['value'], data['data'][2]['value'], data['data'][3]['value'])
                sleep(0.02)
            elif data['data'][1]['value'] is not "" and data['data'][0]['value'] == "Decrease":
                increAndDecreResize(data['data'][1]['value'], -int(data['data'][2]['value']), -int(data['data'][3]['value']))
                sleep(0.02)
        else:
            break

@TPClient.on(TYPES.onConnect)
def Onconnect(data):
    global running
    running = True
    TPClient.settingUpdate("Version", "2.1")
    TPClient.settingUpdate("Is Running","True")
    Thread(target=stateUpdate).start()
    print(data)

@TPClient.on(TYPES.onShutdown)
def Shutdown(data):
    global running
    running = False
    try:
        TPClient.settingUpdate("Is Running","False")
    except:
        pass
    TPClient.disconnect()
    sys.exit()

TPClient.connect()
