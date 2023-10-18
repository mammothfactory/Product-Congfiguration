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
# Disable PyLint linting messages that seem unuseful
# https://pypi.org/project/pylint/
# pylint: disable=invalid-name
# pylint: disable=global-statement


# Standard Python libraries
import sys

# Browser base GUI framework to build and display a user interface mobile, PC, and Mac
# https://nicegui.io/
from nicegui import app, ui
# TODO REMOVE IF MOUSE CLICKS ON INTERACTIVE IMAGE IS NOT NEEDED? from nicegui.events import MouseEventArguments
from nicegui.events import ValueChangeEventArguments

import GlobalConstants as GC                        # Global constants used across ??? files

try:  # Importing externally developed 3rd party modules / libraries

    # Create directory and URL for local storage of images
    if sys.platform.startswith('darwin'):
        app.add_static_files('/static/images', GC.LOCAL_MAC_CODE_DIRECTORY + '/static/images')
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
    currentExteriorImage = 'static/images/WhiteSiding.png'
    currentInteriorImage = 'static/images/INTERIOR.png'


def select_image(radioButtonEvent: ValueChangeEventArguments):
    subsection.classes('w-128')
    if radioButtonEvent.value == GC.EXTERIOR_MATERIALS[0]:
        exteriorRadioButtons.props('inline color=white')
        exteriorII.set_source('static/images/WhiteSiding.png')
        configuration[0] = GC.EXTERIOR_MATERIALS[0]
    elif radioButtonEvent.value == "Red":
        exteriorRadioButtons.props('inline color=red')
        exteriorII.set_source('static/images/RedSiding.png')
        configuration[0] = GC.EXTERIOR_MATERIALS[1]
    elif radioButtonEvent.value == "Brown":
        exteriorRadioButtons.props('inline color=brown')
        exteriorII.set_source('static/images/BrownSiding.png')
        configuration[0] = GC.EXTERIOR_MATERIALS[2]
    else:
        exteriorII.set_source('static/images/WhiteSiding.png')
        configuration[0] = GC.EXTERIOR_MATERIALS[0]


def select_form(selection):
    print(f"Dropdown changed: {selection}")
    if selection == GC.VIEWS[0]:
        floorPlanRadioButtons.set_visibility(True)
        exteriorView.set_visibility(True)                # TODO replace with floor plans 
        exteriorRadioButtons.set_visibility(False)       # TODO replace with floor plans  
        interiorView.set_visibility(False) 
        interiorRadioButtons.set_visibility(False)
        finalScreen.set_visibility(False)

    elif selection == GC.VIEWS[1]:
        floorPlanRadioButtons.set_visibility(False)
        exteriorView.set_visibility(True)
        exteriorRadioButtons.set_visibility(True)
        interiorView.set_visibility(False)
        interiorRadioButtons.set_visibility(False) 
        finalScreen.set_visibility(False)
        
    elif selection == GC.VIEWS[2]:
        floorPlanRadioButtons.set_visibility(False)
        exteriorView.set_visibility(False)
        exteriorRadioButtons.set_visibility(False)
        interiorView.set_visibility(True) 
        interiorRadioButtons.set_visibility(True)
        finalScreen.set_visibility(False)


def redirect():
    # Can an Iframe cause square space website containing it to redirect to a new page?
    # https://chat.openai.com/share/3ab29987-afe8-4a54-853f-bdb0c1f5ca92
    pass


def sanitized_email(text: str):
    pass


def send_email():
    pass


if __name__ in {"__main__", "__mp_main__"}:
    darkMode.enable()
    ui.colors(primary=GC.MAMMOTH_BRIGHT_GRREN)

    configuration = ["White", "Litehouse", "?"]

    imageGrid = ui.grid(columns=1)
    with imageGrid:
        exteriorView = ui.row()
        with exteriorView:
            exteriorII = ui.interactive_image(currentExteriorImage, on_mouse=select_image, events=['mousedown', 'mouseup'], cross=False)

        interiorView = ui.row()
        interiorView.set_visibility(False)   
        with interiorView:
            interiorII = ui.interactive_image(currentInteriorImage, on_mouse=select_image, events=['mousedown', 'mouseup'], cross=False)

        finalScreen = ui.row()
        finalScreen.set_visibility(False)   

    dataForm = ui.grid(columns=2)
    with dataForm:    
        subsection = ui.select(GC.VIEWS, value=GC.VIEWS[0], on_change=lambda e: select_form(e.value)).classes('w-96')
        print("Width of dropdown is w-128")
        floorPlanRadioButtons = ui.radio(GC.FLOOR_PLAN_TYPES, value=GC.FLOOR_PLAN_TYPES[0], on_change=select_image).props('inline color=white').classes('w-max')
        
        exteriorRadioButtons = ui.radio(GC.EXTERIOR_MATERIALS, value=GC.EXTERIOR_MATERIALS[0], on_change=select_image).props('inline color=white').classes('w-max')
        exteriorRadioButtons.set_visibility(False)
        interiorRadioButtons = ui.radio(["Light", "Dark",], value="Item 1").props('inline color=white').classes('w-max')
        interiorRadioButtons.set_visibility(False)

    userForm = ui.grid(columns=1)
    with userForm:
        sanitizedEmail = "blairg@mfc.us"
        emailTextBox = ui.input(label='Enter your email', placeholder='e.g. name@example.com', \
                                on_change=lambda e: invalidEmailLabel.set_text(sanitized_email(e.value)), \
                                validation={'Your email is too long, should be 320 characters or less': lambda value: len(sanitizedEmail) <= GC.MAX_EMAIL_LENGHT}).classes('w-full')
        invalidEmailLabel = ui.label("BAD EMAIL")
        invalidEmailLabel.visible = False
        submitButton = ui.button("SUMBIT CONFIG").classes('w-96')

    ui.run(native=GC.RUN_ON_NATIVE_OS, port=GC.LOCAL_HOST_PORT_FOR_GUI)
