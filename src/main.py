import ctypes
import subprocess
import sys
import threading
from argparse import ArgumentParser
from collections import namedtuple
from ctypes import windll, wintypes
from ctypes.wintypes import tagPOINT
from time import sleep

import pygetwindow as gw
import pywinauto
import TouchPortalAPI as TP
import win32api
import win32gui
from screeninfo import get_monitors
from TouchPortalAPI import TYPES
from TouchPortalAPI.logger import Logger

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
    "Windows Input Experience",
    "Touch Portal Control Edit"
]

# TouchPortal Client
try:
    TPClient = TP.Client(
        pluginId = "WindowMover",  # required ID of this plugin
        sleepPeriod = 0.05,    # allow more time than default for other processes
        autoClose = True,      # automatically disconnect when TP sends "closePlugin" message
        checkPluginId = True,  # validate destination of messages sent to this plugin
        maxWorkers = 4,        # run up to 4 event handler threads
        updateStatesOnBroadcast = False,  # do not spam TP with state updates on every page change
    )
except Exception as e:
    sys.exit(f"Could not create TP Client, exiting. Error was:\n{repr(e)}")

g_log = Logger("WindowMover")
no_permission_error = "Cannot change property of this Window. this could due to not running this program in Admin mode."

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

# Unused function
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

def Move_Window(Title, Display, Where, resize=False, window_instance=0):
    try:
        Window = gw.getWindowsWithTitle(Title)[window_instance]
    except IndexError:
        return
    Monitor = get_desktop()
    g_log.debug(Monitor)
    g_log.debug(f"Title {Title}, Display {Display}, Where {Where}, resize {resize}")

    Indexnum = []
    for x in Monitor:
        Indexnum.append(list(x.keys())[0])

    if Window.isMinimized:
        try:
            Window.restore()
            g_log.debug("Restore window. Because cannot move window when not active")
        except Exception as e:
            g_log.debug(no_permission_error)
            g_log.error(e)
    if Display in Indexnum:
        indexnum = Indexnum.index(Display)
        point = tagPOINT(Monitor[indexnum][Display]['x'], Monitor[indexnum][Display]['y'])
        monitor_area = win32api.GetMonitorInfo(user32.MonitorFromPoint(point, MonitorMode.get("MONITOR_DEFAULTTONEAREST")))
        g_log.debug(monitor_area)

        width = abs(monitor_area["Work"][2]-monitor_area["Work"][0])
        height = abs(monitor_area["Work"][3]-monitor_area["Work"][1])

        if resize == "True":
            try:
                if Where in (window_position := ["Top Half", "Bottom Half", "Left Half", "Right Half"]):
                    if Where in window_position[0:2]:
                        Window.resizeTo(int(width)+12, int(height/2))
                    else:
                        Window.resizeTo(int(width/2)+12, int(height))
                else:
                    Window.resizeTo(int(width/2)+12, int(height/2))
            except Exception as e:
                g_log.debug(no_permission_error)
                g_log.error(e)

        position_x = 0
        position_y = 0

        match Where:
            case "Top Left":
                position_x = monitor_area['Work'][0]-7
                position_y = monitor_area['Work'][1]
            case "Top Right":
                position_x = int(monitor_area['Work'][2]-Window.width)+7
                position_y = int(monitor_area['Work'][1])
            case "Top Middle":
                position_x = int(monitor_area['Work'][0]+(width-Window.width)/2)
                position_y = monitor_area['Work'][1]-7
            case "Bottom Middle":
                position_x = int(monitor_area['Work'][0]+(width-Window.width)/2)
                position_y = int(monitor_area['Work'][3]-Window.height)+7
            case "Left Middle":
                position_x = monitor_area['Work'][0]-7
                position_y = int((monitor_area['Work'][1]+(height-Window.height))/2)
            case "Right Middle":
                position_x = int(monitor_area['Work'][2]-Window.width)+7
                position_y = int((monitor_area['Work'][1]+(height-Window.height))/2)
            case "Bottom Left":
                position_x = int(monitor_area['Work'][0])-7
                position_y = int(monitor_area['Work'][3]-Window.height)+7
            case "Bottom Right":
                position_x = int(monitor_area['Work'][2]-Window.width)+7
                position_y = int(monitor_area['Work'][3]-Window.height)+7
            case "Center":
                position_x = int(monitor_area['Work'][0]+(width-Window.width)/2)
                position_y = int((monitor_area['Work'][1]+(height-Window.height))/2)
            case "Top Half":
                position_x = monitor_area['Work'][0]-7
                position_y = monitor_area['Work'][1]
            case "Bottom Half":
                position_x = monitor_area['Work'][0]-7
                position_y = int(monitor_area['Work'][3]-Window.height)
            case "Left Half":
                position_x = monitor_area['Work'][0]-7
                position_y = monitor_area["Work"][1]
            case "Right Half":
                position_x = int(monitor_area['Work'][2]-Window.width)+6
                position_y = monitor_area["Work"][1]
            case "_":
                g_log.info(f"Unknown position: {Where}")

        try:
            Window.moveTo(position_x, position_y)
        except Exception as e:
            g_log.debug(no_permission_error)
            g_log.error(e)

        g_log.info(f"presets: {Where} process: {Title} positon: {Window.position} size: {Window.size}")
        

def ResizeTo(Title, width, height):
    try:
        Window = gw.getWindowsWithTitle(Title)[0]
    except IndexError:
        return
    if Window.isMinimized:
        try:
            Window.restore()
        except:
            g_log.debug(no_permission_error)
    try:
        Window.resizeTo(int(width),int(height))
    except:
        g_log.debug(no_permission_error)

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
        g_log.debug(no_permission_error)

def increAndDecreResize(Title, width, height):
    try:
        Window = gw.getWindowsWithTitle(Title)[0]
    except IndexError:
        return
    if Window.isMinimized:
        try:
            Window.restore()
        except:
            g_log.debug(no_permission_error)
    try:
        Window.resize(int(width),int(height))
    except:
        g_log.debug(no_permission_error)

def focus_to_window(window_title=None):
    window = gw.getWindowsWithTitle(window_title)[0]
    if window.isActive == False:
        try:
            pywinauto.application.Application().connect(handle=window._hWnd).top_window().set_focus()
        except:
            g_log.debug(no_permission_error)

def SysAction(Title, action):
    try:
        Window = gw.getWindowsWithTitle(Title)[0]
        g_log.debug(Window)
    except IndexError:
        return
    if action in ["maximize", "minimize", "restore", "close"] :
        try:
            method = getattr(Window, action)
            method()
        except Exception as e:
            g_log.info(f"Error running {action} on {Title}. Most likely a permission error. {e}")
    elif action == "focus":
        try:
            focus_to_window(Title)
        except Exception as e:
            g_log.info(f"Unhandeled Error running {action} on {Title}. {e}")
    
def CustomAction(Title, x, y, width, hight):
    try:
        Window = gw.getWindowsWithTitle(Title)[0]
    except IndexError:
        return
    if Window.isMinimized:
        Window.restore()
    Window.moveTo(int(x),int(y))
    Window.resizeTo(int(width),int(hight))

def stateUpdate():
    Timer = threading.Timer(0.25, stateUpdate)
    monitor = [list(each.keys())[0].rstrip() for each in get_desktop()]
    if TPClient.choiceUpdateList.get("KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Displays") != monitor:
        TPClient.choiceUpdate("KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Displays", monitor)
        TPClient.choiceUpdate('KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Advanced.Displays', monitor)
        g_log.debug(f'updating Display List {monitor}')

    if TPClient.choiceUpdateList.get("KillerBOSS.TP.Plugins.WindowMover.customMove.Window") != (processWindow := list_windows()):
        TPClient.choiceUpdate("KillerBOSS.TP.Plugins.WindowMover.customMove.Window", processWindow)
        g_log.debug(f"Updating process list {processWindow}")

    currentFocusedWindow = gw.getActiveWindowTitle()
    TPClient.stateUpdate('KillerBOSS.TP.Plugins.WindowMover.states.ActiveWindow', gw.getActiveWindowTitle())


    if currentFocusedWindow and (WindowInfo := gw.getWindowsWithTitle(currentFocusedWindow)) and len(WindowInfo) > 0:
        WindowInfo = WindowInfo[0]
        if all(item in WindowInfo.__dir__() for item in ["top", "left", "width", "height", "isMaximized", "isMinimized", "isActive"]):
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
        else:
            g_log.debug("att is missing")
    
    if TPClient.isConnected():
        Timer.start()

@TPClient.on(TYPES.onAction)
def ManageAction(data):
    g_log.debug(f"Connection: {data}")
    g_log.info(f"Action: {data['actionId']}")

    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.Windowpresets":
        if data['data'][1]['value']:
            Move_Window(data['data'][1]['value'], data['data'][2]['value'], data['data'][0]['value'],data['data'][3]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.ResizeTo":
        if data['data'][0]['value']: 
            ResizeTo(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease":
        if data['data'][1]['value']:
            if data['data'][0]['value'] == "Increase":
                increAndDecreResize(data['data'][1]['value'], int(data['data'][2]['value']), int(data['data'][3]['value']))
            elif data['data'][0]['value'] == "Decrease":
                increAndDecreResize(data['data'][1]['value'], -int(data['data'][2]['value']), -int(data['data'][3]['value']))
    
    if data['actionId'] == 'KillerBOSS.TP.Plugins.WindowMover.SysActions':
        if data['data'][1]['value']:
            SysAction(data['data'][1]['value'],data['data'][0]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.MoveByXandY":
        if data['data'][0]['value']:
            if data['data'][3]['value'] == "Increase":
                MovebyXY(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
            elif data['data'][3]['value'] == "Decrease":
                MovebyXY(data['data'][0]['value'], -int(data['data'][1]['value']), -int(data['data'][2]['value']))
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.customMove":
        if data['data'][0]['value'] != '' and data['data'][1]['value'] != '' and data['data'][2]['value'] != '' and data['data'][3]['value'] != '' and data['data'][4]['value'] != '':
            CustomAction(data['data'][0]['value'],data['data'][1]['value'],data['data'][2]['value'],data['data'][3]['value'],data['data'][4]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.Advanced.MoveByXandY":
        if data['data'][0]['value'] and data['data'][3]['value'] == 'Increase':
            MovebyXY(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
        elif data['data'][0]['value'] and data['data'][3]['value'] == "Decrease":
            MovebyXY(data['data'][0]['value'], -int(data['data'][1]['value']), -int(data['data'][2]['value']))
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease.Advanced":
        if data['data'][1]['value'] and data['data'][0]['value'] == 'Increase':
            increAndDecreResize(data['data'][1]['value'], data['data'][2]['value'], data['data'][3]['value'])
            sleep(0.02)
        elif data['data'][1]['value'] and data['data'][0]['value'] == "Decrease":
            increAndDecreResize(data['data'][1]['value'], -int(data['data'][2]['value']), -int(data['data'][3]['value']))
            sleep(0.02)
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.Advanced.Windowpresets":
        if data['data'][1]['value']:
            Move_Window(data['data'][1]['value'],data['data'][2]['value'],data['data'][0]['value'], data['data'][3]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.ResizeTo.Advanced":
        if data['data'][0]['value']: 
            ResizeTo(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.Advanced.customMove":
        if data['data'][0]['value']:
            CustomAction(data['data'][0]['value'],data['data'][1]['value'],data['data'][2]['value'],data['data'][3]['value'],data['data'][4]['value'])
    if data['actionId'] == "KillerBOSS.TP.Plugins.WindowMover.SysActions.Advanced":
        if data['data'][1]['value']:
            SysAction(data['data'][1]['value'], data['data'][0]['value'])

@TPClient.on(TYPES.onListChange)
def listChange(data):
    g_log.debug(f"Connection: {data}")
    if data['listId'] == "KillerBOSS.TP.Plugins.WindowMover.customMove.Window":
        try:
            findwindow = win32gui.FindWindow(None,data['value'])
            rect = win32gui.GetWindowRect(findwindow)
        except KeyError:
            return
        TPClient.choiceUpdateSpecific("KillerBOSS.TP.Plugins.WindowMover.customMove.X", [str(rect[0])], data["instanceId"])
        TPClient.choiceUpdateSpecific("KillerBOSS.TP.Plugins.WindowMover.customMove.Y", [str(rect[1])], data["instanceId"])
        TPClient.choiceUpdateSpecific("KillerBOSS.TP.Plugins.WindowMover.customMove.width", [str(rect[2]-rect[0])], data["instanceId"])
        TPClient.choiceUpdateSpecific("KillerBOSS.TP.Plugins.WindowMover.customMove.height", [str(rect[3]-rect[1])], data["instanceId"])
        g_log.info(f"Window: {data['value']} has been selected updating values")

@TPClient.on(TYPES.onHold_down)
def holdAction(data):
    g_log.debug(f"Connection: {data}")
    g_log.info(f"Action: {data['actionId']} is being held down")
    while True:
        sleep(0.02)
        if TPClient.isActionBeingHeld('KillerBOSS.TP.Plugins.WindowMover.MoveByXandY'):
            if data['data'][3]['value'] == "Increase":
                MovebyXY(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
            elif data['data'][3]['value'] == "Decrease":
                MovebyXY(data['data'][0]['value'], -int(data['data'][1]['value']), -int(data['data'][2]['value']))

        elif TPClient.isActionBeingHeld('KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease'):
            if data['data'][0]['value'] == "Increase":
                increAndDecreResize(data['data'][1]['value'], int(data['data'][2]['value']), int(data['data'][3]['value']))
            if data['data'][0]['value'] == "Decrease":
                increAndDecreResize(data['data'][1]['value'], -int(data['data'][2]['value']), -int(data['data'][3]['value']))
        elif TPClient.isActionBeingHeld('KillerBOSS.TP.Plugins.WindowMover.Advanced.MoveByXandY'):
            if data['data'][0]['value'] and data['data'][3]['value'] == 'Increase':
                MovebyXY(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
            elif data['data'][0]['value'] and data['data'][3]['value'] == "Decrease":
                MovebyXY(data['data'][0]['value'], -int(data['data'][1]['value']), -int(data['data'][2]['value']))
        elif TPClient.isActionBeingHeld('KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease.Advanced'):
            if data['data'][1]['value'] and data['data'][0]['value'] == 'Increase':
                increAndDecreResize(data['data'][1]['value'], data['data'][2]['value'], data['data'][3]['value'])
            elif data['data'][1]['value'] and data['data'][0]['value'] == "Decrease":
                increAndDecreResize(data['data'][1]['value'], -int(data['data'][2]['value']), -int(data['data'][3]['value']))
        else:
            break
    g_log.info(f"Action: {data['actionId']} is no longer being held down")

@TPClient.on(TYPES.onConnect)
def Onconnect(data):
    g_log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
    g_log.debug(f"Connection: {data}")

    TPClient.settingUpdate("Version", "3.1.0")
    TPClient.settingUpdate("Is Running","True")

    TPClient.choiceUpdate("KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Displays", [])
    TPClient.choiceUpdate('KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Advanced.Displays', [])
    TPClient.choiceUpdate("KillerBOSS.TP.Plugins.WindowMover.customMove.Window", [])

    stateUpdate()

@TPClient.on(TYPES.onShutdown)
def Shutdown(data):
    g_log.debug(f"Connection: {data}")
    try:
        TPClient.settingUpdate("Is Running","False")
    except ConnectionResetError:
        pass
    g_log.info('Received shutdown event from TP Client.')

# Error handler
@TPClient.on(TYPES.onError)
def onError(exc):
    g_log.error(f'Error in TP Client event handler: {repr(exc)}')

def main():
    global TPClient, g_log
    ret = 0

    # default log file destination
    logFile = f"./log.log"
    # default log stream destination
    logStream = sys.stdout

    # Set up and handle CLI arguments. These all relate to logging options.
    # The plugin can be run with "-h" option to show available argument options.
    # Addtionally, a file constaining any of these arguments can be specified on the command line
    # with the `@` prefix. For example: `plugin-example.py @config.txt`
    # The file must contain one valid argument per line, including the `-` or `--` prefixes.
    # See the plugin-example-conf.txt file for an example config file.
    parser = ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("-d", action='store_true',
                        help="Use debug logging.")
    parser.add_argument("-w", action='store_true',
                        help="Only log warnings and errors.")
    parser.add_argument("-q", action='store_true',
                        help="Disable all logging (quiet).")
    parser.add_argument("-l", metavar="<logfile>", 
                        help=f"Log file name (default is '{logFile}'). Use 'none' to disable file logging.")
    parser.add_argument("-s", metavar="<stream>",
                        help="Log to output stream: 'stdout' (default), 'stderr', or 'none'.")

    # his processes the actual command line and populates the `opts` dict.
    opts = parser.parse_args()
    del parser

    # trim option string (they may contain spaces if read from config file)
    opts.l = opts.l.strip() if opts.l else 'none'
    opts.s = opts.s.strip().lower() if opts.s else 'stdout'
    g_log.info(opts)

    # Set minimum logging level based on passed arguments
    logLevel = "INFO"
    if opts.q: logLevel = None
    elif opts.d: logLevel = "DEBUG"
    elif opts.w: logLevel = "WARNING"

    # set log file if -l argument was passed
    if opts.l:
        logFile = None if opts.l.lower() == "none" else opts.l
    # set console logging if -s argument was passed
    if opts.s:
        if opts.s == "stderr": logStream = sys.stderr
        elif opts.s == "stdout": logStream = sys.stdout
        else: logStream = None

    # Configure the Client logging based on command line arguments.
    # Since the Client uses the "root" logger by default,
    # this also sets all default logging options for any added child loggers, such as our g_log instance we created earlier.
    TPClient.setLogFile(logFile)
    TPClient.setLogStream(logStream)
    TPClient.setLogLevel(logLevel)

    # ready to go
    g_log.info(f"Starting WindowsMover v302 on {sys.platform}.")

    try:
        TPClient.connect()
        g_log.info('TP Client closed.')
    except KeyboardInterrupt:
        g_log.warning("Caught keyboard interrupt, exiting.")
    except Exception:
        from traceback import format_exc
        g_log.error(f"Exception in TP Client:\n{format_exc()}")
        ret = -1
    finally:
        TPClient.disconnect()

    del TPClient

    g_log.info(f"WindowsMover stopped.")
    return ret

if __name__ == "__main__":
    sys.exit(main())
