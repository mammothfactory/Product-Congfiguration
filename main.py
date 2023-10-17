#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
 __contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "GPLv3"
__status__     = "Development
__deprecated__ = False
__version__    = "0.0.1"
__doc__        = "Generate Progressive Web App GUI to configure products for sale"
"""

# Standard Python libraries
import sys

# Browser base GUI framework to build and display a user interface mobile, PC, and Mac
# https://nicegui.io/
from nicegui import app, ui
from nicegui.events import MouseEventArguments
from nicegui.events import ValueChangeEventArguments

import GlobalConstants as GC                        # Global constants used across ??? files

try:  # Importing externally developed 3rd party modules / libraries

    # Create directory and URL for local storage of images
    if sys.platform.startswith('darwin'):
        app.add_static_files('/static/images', GC.LOCAL_MAC_CODE_DIRECTORY +'/static/images')
    elif sys.platform.startswith('linux'):
        app.add_static_files('/static/images', GC.LINODE_LINUX_CODE_DIRECTORY + '/static/images')
    elif sys.platform.startswith('win'):
        print("WARNING: Running main.py on Windows Server OS is NOT fully supported")
        app.add_static_files('/static/images', GC.WINDOWS_CODE_DIRECTORY + '/static/images')
    else:
        print("ERROR: Running on an unknown operating system")
        quit()
        
except ImportError:
    print("ERROR: Not all the required libraries are installed!")
    

finally:
    # Global Variables
    isDarkModeOn = False            # Application boots up in light mode
    darkMode = ui.dark_mode()
    darkMode.enable()
    currentImage = 'static/images/RedSiding.png'

def select_image(radioButtonEvent: ValueChangeEventArguments):
    if radioButtonEvent.value == 'White':
        print("WHITE")
        ii.set_source('static/images/WhiteSiding.png')
    elif radioButtonEvent.value == 'Red':
        print("RED")
        ii.set_source('static/images/RedSiding.png')
    elif radioButtonEvent.value == 'Brown':
        print("BROWN")
        ii.set_source('static/images/BrownSiding.png')
    else:
        ii.set_source('static/images/WhiteSiding.png')
        
    
if __name__ in {"__main__", "__mp_main__"}:
    darkMode.enable()
    ui.colors(primary=GC.MAMMOTH_BRIGHT_GRREN)
    
    with ui.row():
        ii = ui.interactive_image(currentImage, on_mouse=select_image, events=['mousedown', 'mouseup'], cross=False)
        ui.radio(['White', 'Red', 'Brown'], value='White', on_change=select_image).props('inline')
    
    ui.run(native=GC.RUN_ON_NATIVE_OS, port=GC.LOCAL_HOST_PORT_FOR_GUI)
"""
    with ui.grid(columns=1):
        ui.label(f'Click on image to toggle {tabNames[0]}').tailwind('mx-auto text-2xl')
        ii = ui.interactive_image(houseType, on_mouse=determine_room_light_mouse_handler, events=['mousedown'], cross=True)
        
""" 
    