#!/usr/bin/env python3

__version__ = "3.1.0"

TP_PLUGIN_INFO = {
    "sdk": 6,
    "version": 310,
    "name": "Windows Mover",
    "id": "WindowMover",
    "configuration": {
        "colorDark": "#222423",
        "colorLight": "#020202"
    },
    "plugin_start_cmd": "%TP_PLUGIN_FOLDER%Window-Mover\\StartWinMover.bat"
}

TP_PLUGIN_SETTINGS = {
    "1": {
        "name": "Build by",
        "type": "text",
        "default": "Killer_BOSS",
        "readOnly": True
    },
    "2": {
        "name": "Version",
        "type": "text",
        "default": "0",
        "readOnly": True
    },
    "3": {
        "name": "Is Running",
        "type": "text",
        "default": "False",
        "readOnly": True
    }
}

TP_PLUGIN_CATEGORIES = {
    "main": {
        "id": "main",
        "name": "Window Mover",
        "imagepath": "%TP_PLUGIN_FOLDER%Window-Mover\\icon.png"
    },
    "Simple": {
        "id": "Simple",
        "name": "Window Mover - Simple",
        "imagepath": "%TP_PLUGIN_FOLDER%Window-Mover\\icon.png"
    },
    "Advanced": {
        "id": "Advanced",
        "name": "Window Mover - Advanced",
        "imagepath": "%TP_PLUGIN_FOLDER%Window-Mover\\icon.png"
    }
}

TP_PLUGIN_CONNECTORS = {}

TP_PLUGIN_ACTIONS = {
    "1": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.Windowpresets",
        "name": "Window Mover: Simple Move Window by presets",
        "prefix": "plugin",
        "type": "communicate",
        "doc": "Pre programmed Presets allows user to move X window to Top Left, Bottom Middle, Center etc...",
        "tryInline": True,
        "format": "Move $[2] on Display:$[3] to $[1] Allow Resize:$[4]",
        "data": {
            "1": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Presets",
                "type": "choice",
                "label": "choice",
                "default": "Top Left",
                "valueChoices": [
                    "Top Left",
                    "Top Right",
                    "Top Middle",
                    "Bottom Left",
                    "Bottom Right",
                    "Bottom Middle",
                    "Top Half",
                    "Bottom Half",
                    "Left Half",
                    "Right Half",
                    "Left Middle",
                    "Right Middle",
                    "Center"
                ]
            },
            "2": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.Window",
                "label": "Window",
                "type": "choice",
                "default": "",
                "valueChoices": []
            },
            "3": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Displays",
                "type": "choice",
                "label": "choice",
                "valueChoices": []
            },
            "4": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.Windowpresets.AllowResize",
                "type": "choice",
                "label": "choice",
                "default": "True",
                "valueChoices": [
                    "True",
                    "False"
                ]
            }
        },
        "category": "Simple"
    },
    "2": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.MoveByXandY",
        "name": "Window Mover: Simple Increase X, Y",
        "prefix": "plugin",
        "type": "communicate",
        "tryInline": True,
        "doc": "Allow user to move window by x or y amount",
        "hasHoldFunctionality": True,
        "format": "$[4] Window:$[1] by X:$[2] and Y:$[3]",
        "data": {
            "1": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.Window",
                "label": "Window",
                "type": "choice",
                "default": "",
                "valueChoices": []
            },
            "2": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.MoveByXandY.X",
                "label": "Move By X",
                "type": "number",
                "allowDecimals": False,
                "default": 1
            },
            "3": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.MoveByXandY.Y",
                "label": "Move By Y",
                "type": "number",
                "allowDecimals": False,
                "default": 1
            },
            "4": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.MoveByXandY.Choice",
                "label": "Update Choice",
                "type": "choice",
                "default": "Increase",
                "valueChoices": [
                    "Increase",
                    "Decrease"
                ]
            }
        },
        "category": "Simple"
    },
    "3": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeTo",
        "name": "Window Mover: Simple Resize Window",
        "prefix": "plugin",
        "type": "communicate",
        "doc": "Ability to Resize Window to specific size.",
        "tryInline": True,
        "format": "Set $[1] Size to width:$[2] and height:$[3]",
        "data": {
            "1": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.Window",
                "label": "Window",
                "type": "choice",
                "default": "",
                "valueChoices": []
            },
            "2": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeTo.width",
                "label": "Move By X",
                "type": "number",
                "allowDecimals": False,
                "default": 400
            },
            "3": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeTo.height",
                "label": "Move By Y",
                "type": "number",
                "allowDecimals": False,
                "default": 400
            }
        },
        "category": "Simple"
    },
    "4": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease",
        "name": "Window Mover: Simple Resize Increase Width, Height",
        "prefix": "plugin",
        "type": "communicate",
        "doc": "Increase or Decrease window current width and height",
        "tryInline": True,
        "hasHoldFunctionality": True,
        "format": "$[1]Window:$[2]by Width:$[3] and Height:$[4]",
        "data": {
            "1": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease.In&Decre",
                "type": "choice",
                "label": "choice",
                "default": "Increase",
                "valueChoices": [
                    "Increase",
                    "Decrease"
                ]
            },
            "2": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.Window",
                "label": "Window",
                "type": "choice",
                "default": "",
                "valueChoices": []
            },
            "3": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease.width",
                "label": "Move By X",
                "type": "number",
                "allowDecimals": False,
                "default": 1
            },
            "4": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease.height",
                "label": "Move By Y",
                "type": "number",
                "allowDecimals": False,
                "default": 1
            }
        },
        "category": "Simple"
    },
    "5": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.SysActions",
        "name": "Window Mover: Simple focus, restore, minimize, and restore",
        "prefix": "plugin",
        "type": "communicate",
        "doc": "Simple window action allows you to focus, restore, maximize, close and minimize.",
        "tryInline": True,
        "format": "$[1] Window:$[2]",
        "data": {
            "1": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.SysActions.Choice",
                "type": "choice",
                "label": "choice",
                "default": "maximize",
                "valueChoices": [
                    "maximize",
                    "minimize",
                    "restore",
                    "focus",
                    "close"
                ]
            },
            "2": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.Window",
                "label": "Window",
                "type": "choice",
                "default": "",
                "valueChoices": []
            }
        },
        "category": "Simple"
    },
    "6": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.customMove",
        "name": "Window Mover: Simple Move Window by current data",
        "prefix": "plugin",
        "type": "communicate",
        "tryInline": True,
        "doc": "When selecting a window it'll auto populate x, y pos and width and height",
        "format": "Load $[1] with X:$[2]Y:$[3]Width:$[4]height:$[5]",
        "data": {
            "1": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.Window",
                "label": "Window",
                "type": "choice",
                "default": "",
                "valueChoices": []
            },
            "2": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.X",
                "type": "choice",
                "label": "choice",
                "valueChoices": []
            },
            "3": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.Y",
                "type": "choice",
                "label": "choice",
                "valueChoices": []
            },
            "4": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.width",
                "type": "choice",
                "label": "choice",
                "valueChoices": []
            },
            "5": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.height",
                "type": "choice",
                "label": "choice",
                "valueChoices": []
            }
        },
        "category": "Simple"
    },
    "7": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.Advanced.Windowpresets",
        "name": "Window Mover: Advanced Move Window by presets",
        "prefix": "plugin",
        "type": "communicate",
        "doc": "Pre programmed Presets allows user to move X window to Top Left, Bottom Middle, Center etc...",
        "tryInline": True,
        "format": "Move $[2] on Display:$[3] to $[1] Allow Resize:$[4]",
        "data": {
            "1": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Advanced.Presets",
                "type": "choice",
                "label": "choice",
                "default": "Top Left",
                "valueChoices": [
                    "Top Left",
                    "Top Right",
                    "Bottom Left",
                    "Bottom Right"
                ]
            },
            "2": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.Advanced.Windowpreset.Window",
                "label": "Window",
                "type": "text",
                "default": ""
            },
            "3": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Advanced.Displays",
                "type": "choice",
                "label": "choice",
                "valueChoices": []
            },
            "4": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.Windowpresets.Advanced.AllowResize",
                "type": "choice",
                "label": "choice",
                "default": "True",
                "valueChoices": [
                    "True",
                    "False"
                ]
            }
        },
        "category": "Advanced"
    },
    "8": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.Advanced.MoveByXandY",
        "name": "Window Mover: Advanced  Increase X, Y",
        "prefix": "plugin",
        "type": "communicate",
        "tryInline": True,
        "doc": "Allow user to move window by x or y amount",
        "hasHoldFunctionality": True,
        "format": "$[4] Window:$[1] by X:$[2] and Y:$[3]",
        "data": {
            "1": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.MoveByXandY.Advanced.Window",
                "label": "Window",
                "type": "text",
                "default": ""
            },
            "2": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.MoveByXandY.Advanced.X",
                "label": "Move By X",
                "type": "number",
                "allowDecimals": False,
                "default": 1
            },
            "3": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.MoveByXandY.Advanced.Y",
                "label": "Move By Y",
                "type": "number",
                "allowDecimals": False,
                "default": 1
            },
            "4": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.MoveByXandY.Advanced.Choice",
                "label": "Update Choice",
                "type": "choice",
                "default": "Increase",
                "valueChoices": [
                    "Increase",
                    "Decrease"
                ]
            }
        },
        "category": "Advanced"
    },
    "9": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeTo.Advanced",
        "name": "Window Mover: Advanced Resize Window",
        "prefix": "plugin",
        "type": "communicate",
        "doc": "Ability to Resize Window to specific size.",
        "tryInline": True,
        "format": "Set $[1] width:$[2] and Height:$[3]",
        "data": {
            "1": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeTo.Advanced.Window",
                "label": "Window",
                "type": "text",
                "default": ""
            },
            "2": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeTo.Advanced.width",
                "label": "Move By X",
                "type": "number",
                "allowDecimals": False,
                "default": 400
            },
            "3": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeTo.Advanced.height",
                "label": "Move By Y",
                "type": "number",
                "allowDecimals": False,
                "default": 400
            }
        },
        "category": "Advanced"
    },
    "10": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease.Advanced",
        "name": "Window Mover: Advanced Resize Increase Width, hight",
        "prefix": "plugin",
        "type": "communicate",
        "tryInline": True,
        "doc": "Increase or Decrease window current width and height",
        "hasHoldFunctionality": True,
        "format": "$[1]Window:$[2]by Width:$[3] and Height:$[4]",
        "data": {
            "1": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease.Advanced.In&Decre",
                "type": "choice",
                "label": "choice",
                "default": "Increase",
                "valueChoices": [
                    "Increase",
                    "Decrease"
                ]
            },
            "2": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease.Advanced.Window",
                "label": "Window",
                "type": "text",
                "default": ""
            },
            "3": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease.Advanced.width",
                "label": "Move By X",
                "type": "number",
                "allowDecimals": False,
                "default": 1
            },
            "4": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.ResizeIncrease.Advanced.height",
                "label": "Increase height",
                "type": "number",
                "allowDecimals": False,
                "default": 1
            }
        },
        "category": "Advanced"
    },
    "11": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.SysActions.Advanced",
        "name": "Window Mover: Advanced focus, restore, minimize, and restore",
        "prefix": "plugin",
        "type": "communicate",
        "doc": "Simple window action allows you to focus, restore, maximize, close and minimize.",
        "tryInline": True,
        "format": "$[1] Window:$[2]",
        "data": {
            "1": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.SysActions.Advanced.Choice",
                "type": "choice",
                "label": "choice",
                "default": "maximize",
                "valueChoices": [
                    "maximize",
                    "minimize",
                    "restore",
                    "focus",
                    "close"
                ]
            },
            "2": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.SysActions.Advanced.Window",
                "label": "Window",
                "type": "text",
                "default": ""
            }
        },
        "category": "Advanced"
    },
    "12": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.Advanced.customMove",
        "name": "Window Mover: Advanced Move Window by current data",
        "prefix": "plugin",
        "type": "communicate",
        "doc": "When selecting a window it'll auto populate x, y pos and width and height",
        "tryInline": True,
        "format": "Load $[1] with X:$[2]Y:$[3]Width:$[4]height:$[5]",
        "data": {
            "1": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.Advanced.Window",
                "label": "Window",
                "type": "text",
                "default": ""
            },
            "2": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.Advanced.X",
                "type": "number",
                "label": "choice",
                "default": 0,
                "allowDecimals": False
            },
            "3": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.Advanced.Y",
                "type": "number",
                "label": "choice",
                "default": 0,
                "allowDecimals": False
            },
            "4": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.Advanced.width",
                "type": "number",
                "label": "choice",
                "default": 0,
                "allowDecimals": False
            },
            "5": {
                "id": "KillerBOSS.TP.Plugins.WindowMover.customMove.Advanced.height",
                "type": "number",
                "label": "choice",
                "default": 0,
                "allowDecimals": False
            }
        },
        "category": "Advanced"
    }
}

TP_PLUGIN_STATES = {
    "0": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.states.ActiveWindow",
        "type": "text",
        "desc": "Window Mover: Current Active Window",
        "default": "None",
        "doc": "Get current focused Window. This is useful in `Advanced` actions since you can run any actions to current Window.",
        "category": "main"
    },
    "1": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.states.ActiveWindow.X",
        "type": "text",
        "desc": "Window Mover: Current Active Window X pos",
        "default": "None",
        "doc": "Get current active Window x position. (counts from Top left corner window)",
        "category": "main"
    },
    "2": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.states.ActiveWindow.Y",
        "type": "text",
        "desc": "Window Mover: Current Active Window Y pos",
        "doc": "Get current active Window y position. (counts from Top left corner window)",
        "default": "None",
        "category": "main"
    },
    "3": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.states.ActiveWindow.width",
        "type": "text",
        "desc": "Window Mover: Current Active Window Width",
        "doc": "Get current active window Width",
        "default": "None",
        "category": "main"
    },
    "4": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.states.ActiveWindow.height",
        "type": "text",
        "desc": "Window Mover: Current Active Window height",
        "doc": "Get current active Window height",
        "default": "None",
        "category": "main"
    },
    "5": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.states.isCurrentWindowMaximized",
        "type": "text",
        "desc": "Window Mover: is Current Window Maximized",
        "doc": "Let's you know if current Window is maximized or not. boolean True/False",
        "default": "False",
        "category": "main"
    },
    "6": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.states.isCurrentWindowminimize",
        "type": "text",
        "desc": "Window Mover: is Current Window minimized",
        "doc": "It let's you know if current Window is minimized or not. boolean True/False",
        "default": "False",
        "category": "main"
    },
    "7": {
        "id": "KillerBOSS.TP.Plugins.WindowMover.states.isCurrentWindowActive",
        "type": "text",
        "desc": "Window Mover: is Current Window Active",
        "doc": "It shows if current Window is active. boolean True/Faluse",
        "default": "False",
        "category": "main"
    }
}

TP_PLUGIN_EVENTS = {}

