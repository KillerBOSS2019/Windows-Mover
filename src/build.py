from TouchPortalAPI import tppbuild
from sys import platform
import TPPEntry

PLUGIN_MAIN = "main.py"
"""
PLUGIN_MAIN: This lets tppbuild know where your main python plugin file is located so it will know which file to compile.
"""

PLUGIN_EXE_NAME = "WinMover"
"""
PLUGIN_EXE_NAME: This defines what you want your plugin executable to be named. tppbuild will also use this for the .tpp file in the format:
                `pluginname + "_v" + version + "_" + os_name + ".tpp"`
                If left blank, the file name from PLUGIN_MAIN is used (w/out .py extension).
"""

PLUGIN_EXE_ICON = r"icon.png"
"""
PLUGIN_EXE_ICON: This should be a path to a .ico file. However if png passed in, it will automatically converted to ico.
"""

PLUGIN_ENTRY = "TPPEntry.py"
"""
PLUGIN_ENTRY: This can be either path to entry.tp or path to a python file that contains infomation about entry.
Note if you pass in a entry.tp, tppbuild will automatically validate the json. If you pass in a python file, it will
build entry.tp & validate it for you. If validation fails, tppbuild will exit.
"""

PLUGIN_ENTRY_INDENT = 2
"""
PLUGIN_ENTRY_INDENT: This is used for generating new entry.tp with indentations using python entry struct. default is 2 indents. 
"""

PLUGIN_ROOT = "Window-Mover"
""" This is the root folder name that will be inside of .tpp """

PLUGIN_ICON = PLUGIN_EXE_ICON
""" Path to icon file used in entry.tp for category `imagepath`, if any. If left blank, TP will use a default icon. """

OUTPUT_PATH = r"./"
""" This tells tppbuild where you want finished build tpp to be saved at. Default "./" meaning current dir where tppbuild is running from. """

""" PLUGIN_VERSION: A version string for the generated .tpp file name. This example reads the `__version__` from the example plugin's code. """
PLUGIN_VERSION = TPPEntry.__version__
# If you only wants to use TP entry.tp version you can use the code blow this code will read entry.tp and grab its version.
"""
import json
import os
entry = os.path.join(os.path.split(__file__)[0], PLUGIN_ENTRY)
with open(entry, "r") as f:
    PLUGIN_VERSION = str(json.load(f)['version'])
"""
# Or just set the PLUGIN_VERSION manually.
# PLUGIN_VERSION = "1.0.0-beta1"

"""
If you have any required file(s) that your plugin needs, put them in this list.
"""
ADDITIONAL_FILES = [
    "StartWinMover.bat",
    "Debug.bat"
]

"""
start.sh file is not needed for Windows machine. as it can execute the exe itself where as
Mac and Linux requires to run `chmod +x program` in order to run it.
"""
if platform != "win32":
    ADDITIONAL_FILES.append("start.sh")

"""
Any additional arguments to be passed to Pyinstaller. Optional.
"""
ADDITIONAL_PYINSTALLER_ARGS = [
    "--log-level=WARN"
]

ADDITIONAL_TPPSDK_ARGS = [
]

if __name__ == "__main__":
    tppbuild.runBuild()