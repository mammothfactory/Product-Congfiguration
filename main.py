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
from time import sleep

import re

import tracemalloc
tracemalloc.start()


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
    currentInteriorImage = '/static/images/Interior/DarkKitchen.png'
    finalViewImage= '/static/images/FinalView.png'


def select_image(radioButtonEvent: ValueChangeEventArguments):
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
    if selection == GC.VIEWS[GC.FLOOR_PLAN_VIEW_NUM]:
        floorPlanRadioButtons.set_visibility(True)
        exteriorView.set_visibility(True)                # TODO replace with floor plans 
        exteriorRadioButtons.set_visibility(False)       # TODO replace with floor plans  
        interiorView.set_visibility(False) 
        interiorRadioButtons.set_visibility(False)
        finalView.set_visibility(False)

    elif selection == GC.VIEWS[GC.EXTERIOR_VIEW_NUM]:
        floorPlanRadioButtons.set_visibility(False)
        exteriorView.set_visibility(True)
        exteriorRadioButtons.set_visibility(True)
        interiorView.set_visibility(False)
        interiorRadioButtons.set_visibility(False) 
        finalView.set_visibility(False)
        
    elif selection == GC.VIEWS[GC.INTERIOR_VIEW_NUM]:
        floorPlanRadioButtons.set_visibility(False)
        exteriorView.set_visibility(False)
        exteriorRadioButtons.set_visibility(False)
        interiorView.set_visibility(True) 
        interiorRadioButtons.set_visibility(True)
        finalView.set_visibility(False)


def redirect():
    # Can an Iframe cause square space website containing it to redirect to a new page?
    # https://chat.openai.com/share/3ab29987-afe8-4a54-853f-bdb0c1f5ca92
    pass


async def is_valid_email(email: str):
    invalidEmailLabel.tailwind.font_weight('extrabold').text_color('red-600')
    emailPattern = r'^[\w\.-]+(\+[\w-]+)?@[\w\.-]+\.\w+$'
    valid = re.match(emailPattern, email) is not None
    if not valid:
        invalidEmailLabel.visible = True
        invalidEmailLabel.set_text(f"{email} is an INVALID email.") 
    else:
        invalidEmailLabel.visible = False
        await send_email(email)

async def send_email(email: str):
    
    exteriorView.set_visibility(False)
    interiorView.set_visibility(False)
    finalView.set_visibility(True)  
    sleep(3)
    await ui.run_javascript('top.location.href = "https://www.mammothfactory.co/deposit"', respond=True)
    #await ui.run_javascript(f'getElement({inputBox.id}).focus()', respond=False)
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

        finalView = ui.row()
        finalView.set_visibility(False) 
        with finalView:
            finalII = ui.interactive_image(finalViewImage, on_mouse=select_image, events=['mousedown', 'mouseup'], cross=False)
             

    dataForm = ui.grid(columns=2)
    with dataForm:    
        subsection = ui.select(GC.VIEWS, value=GC.VIEWS[0], on_change=lambda e: select_form(e.value)).classes('w-96')
        floorPlanRadioButtons = ui.radio(GC.FLOOR_PLAN_TYPES, value=GC.FLOOR_PLAN_TYPES[0], on_change=select_image).props('inline color=white').classes('w-max')
        
        exteriorRadioButtons = ui.radio(GC.EXTERIOR_MATERIALS, value=GC.EXTERIOR_MATERIALS[0], on_change=select_image).props('inline color=white').classes('w-max')
        exteriorRadioButtons.set_visibility(False)
        interiorRadioButtons = ui.radio(["Dark", "Light",], value="Dark").props('inline color=white').classes('w-max')
        interiorRadioButtons.set_visibility(False)

    userForm = ui.grid(columns=1)
    with userForm:
        sanitizedEmail = "blairg@mfc.us"
        emailTextBox = ui.input(label='Enter your email', placeholder='e.g. name@example.com', \
                                #on_change=lambda e: ???, \
                                validation={'ERROR: Your email is longer then 48 characters': lambda e: len(e) <= GC.MAX_EMAIL_LENGHT}).classes('w-96')
        invalidEmailLabel = ui.label()
        invalidEmailLabel.visible = False
        submitButton = ui.button("SUMBIT CONFIG", on_click=lambda e: is_valid_email(emailTextBox.value)).classes('w-96')

    ui.run(native=GC.RUN_ON_NATIVE_OS, port=GC.LOCAL_HOST_PORT_FOR_GUI)
