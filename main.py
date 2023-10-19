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
    currentFloorPlanImage = 'static/images/FloorPlan/LiteHouseV1_00000.png'
    currentExteriorImage = 'static/images/Exterior/BrickFaceWoodCladding.png'  
    currentInteriorImage = '/static/images/Interior/DarkKitchen.png'
    finalViewImage= '/static/images/FinalView.png'


def select_floor_plan_image(radioButtonEvent: ValueChangeEventArguments):
    global currentFloorPlanImage
    
    floorplanII.set_source(currentFloorPlanImage)
    purchaseConfiguration[GC.FLOOR_PLAN_VIEW_NUM] = GC.FLOOR_PLAN_TYPES[0]


def select_exterior_image(radioButtonEvent: ValueChangeEventArguments):
    global currentExteriorImage
    
    exteriorII.set_source(currentExteriorImage)
    if radioButtonEvent.value == GC.EXTERIOR_MATERIALS[0]:
        exteriorII.set_source('static/images/Exterior/BrickFaceWoodCladding.png')
        purchaseConfiguration[GC.EXTERIOR_VIEW_NUM] = GC.EXTERIOR_MATERIALS[0]
        
    elif radioButtonEvent.value == GC.EXTERIOR_MATERIALS[1]:
        exteriorII.set_source('static/images/Exterior/DarkWoodCladding.png')
        purchaseConfiguration[GC.EXTERIOR_VIEW_NUM] = GC.EXTERIOR_MATERIALS[1]
        
    elif radioButtonEvent.value == GC.EXTERIOR_MATERIALS[2]:
        exteriorII.set_source('static/images/Exterior/WeatheredCladding.png')
        purchaseConfiguration[GC.EXTERIOR_VIEW_NUM] = GC.EXTERIOR_MATERIALS[2]
        
    elif radioButtonEvent.value == GC.EXTERIOR_MATERIALS[3]:
        exteriorII.set_source('static/images/Exterior/WhiteCladding.png')
        purchaseConfiguration[GC.EXTERIOR_VIEW_NUM] = GC.EXTERIOR_MATERIALS[3]
        
    elif radioButtonEvent.value == GC.EXTERIOR_MATERIALS[4]:
        exteriorII.set_source('static/images/Exterior/WoodCladding.png')
        purchaseConfiguration[GC.EXTERIOR_VIEW_NUM] = GC.EXTERIOR_MATERIALS[4]


def select_interior_image(radioButtonEvent: ValueChangeEventArguments):
    global currentInteriorImage
    print('Changing interior color')
    interiorII.set_source(currentInteriorImage)
    if radioButtonEvent.value == GC.INTERIOR_COLOR[0]:
        interiorII.set_source('static/images/Interior/DarkKitchen.png')
        purchaseConfiguration[GC.INTERIOR_VIEW_NUM] = GC.INTERIOR_COLOR[0]
        
    elif radioButtonEvent.value == GC.INTERIOR_COLOR[1]:
        interiorII.set_source('static/images/Interior/BlueKitchen.png')
        purchaseConfiguration[GC.INTERIOR_VIEW_NUM] = GC.INTERIOR_COLOR[1]
        

def select_form(selection):
    print(f"Dropdown changed: {selection}")
    if selection == GC.VIEWS[GC.FLOOR_PLAN_VIEW_NUM]:
        floorplanView.set_visibility(True)
        floorplanRadioButtons.set_visibility(True)
        exteriorView.set_visibility(False)                # TODO replace with floor plans 
        exteriorRadioButtons.set_visibility(False)       # TODO replace with floor plans  
        interiorView.set_visibility(False) 
        interiorRadioButtons.set_visibility(False)
        
        finalView.set_visibility(False)

    elif selection == GC.VIEWS[GC.EXTERIOR_VIEW_NUM]:
        floorplanView.set_visibility(False)
        floorplanRadioButtons.set_visibility(False)
        exteriorView.set_visibility(True)
        exteriorRadioButtons.set_visibility(True)
        interiorView.set_visibility(False)
        interiorRadioButtons.set_visibility(False) 
        
        finalView.set_visibility(False)
        
    elif selection == GC.VIEWS[GC.INTERIOR_VIEW_NUM]:
        floorplanView.set_visibility(False)
        floorplanRadioButtons.set_visibility(False)
        exteriorView.set_visibility(False)
        exteriorRadioButtons.set_visibility(False)
        interiorView.set_visibility(True) 
        interiorRadioButtons.set_visibility(True)
       
        finalView.set_visibility(False)


def is_valid_email(email: str):
    invalidEmailLabel.tailwind.font_weight('extrabold').text_color('red-600')
    emailPattern = r'^[\w\.-]+(\+[\w-]+)?@[\w\.-]+\.\w+$'
    valid = re.match(emailPattern, email) is not None
    if not valid:
        invalidEmailLabel.visible = True
        invalidEmailLabel.set_text(f"{email} is an INVALID email.") 
        return False
    else:
        invalidEmailLabel.visible = False
        return True
        
async def redirect(url):
    await ui.run_javascript(f'top.location.href = "{url}"', respond=True)


async def send_email(email: str):
    if is_valid_email(email):
        floorplanView.set_visibility(False)
        exteriorView.set_visibility(False)
        interiorView.set_visibility(False)
        finalView.set_visibility(True)
        print(purchaseConfiguration)
        await redirect("https://www.mammothfactory.co/deposit")


if __name__ in {"__main__", "__mp_main__"}:
    darkMode.enable()
    ui.colors(primary=GC.MAMMOTH_BRIGHT_GRREN)

    purchaseConfiguration = [GC.FLOOR_PLAN_TYPES[0], GC.EXTERIOR_MATERIALS[0], GC.INTERIOR_COLOR[0], GC.ROOF_STYLE[0], GC.EXTRAS[0]]

    imageGrid = ui.grid(columns=1)
    with imageGrid:
        floorplanView= ui.row()
        with floorplanView:
            floorplanII = ui.interactive_image(currentFloorPlanImage, cross=False)
        
        
        exteriorView = ui.row()
        exteriorView.set_visibility(False)  
        with exteriorView:
            exteriorII = ui.interactive_image(currentExteriorImage, cross=False)

        interiorView = ui.row()
        interiorView.set_visibility(False)   
        with interiorView:
            interiorII = ui.interactive_image(currentInteriorImage, cross=False)

        finalView = ui.row()
        finalView.set_visibility(False) 
        with finalView:
            finalII = ui.interactive_image(finalViewImage, cross=False)   # on_mouse=await ui.run_javascript('top.location.href = "https://www.mammothfactory.co/deposit"', respond=True)
             

    dataForm = ui.grid(columns=2).classes('w-full')   # 'w-full' or max-w-2xl' with iframe size of ~1145
    with dataForm:    
        with ui.column():
            subsection = ui.select(GC.VIEWS, value=GC.VIEWS[0], on_change=lambda e: select_form(e.value)).classes('w-80')
        
        
        with ui.column():
            floorplanRadioButtons = ui.radio(GC.FLOOR_PLAN_TYPES, value=GC.FLOOR_PLAN_TYPES[0], on_change=select_floor_plan_image).props('inline color=white')
            exteriorRadioButtons = ui.radio(GC.EXTERIOR_MATERIALS, value=GC.EXTERIOR_MATERIALS[0], on_change=select_exterior_image).props('inline color=white')
            exteriorRadioButtons.set_visibility(False)
            interiorRadioButtons = ui.radio(["Dark", "Light"], value=GC.INTERIOR_COLOR[0], on_change=select_interior_image).props('inline color=white')
            interiorRadioButtons.set_visibility(False)
        


    userForm = ui.grid(columns=1)
    with userForm:
        sanitizedEmail = "blairg@mfc.us"
        emailTextBox = ui.input(label='Enter your email', placeholder='e.g. name@example.com', \
                                on_change=lambda e: is_valid_email(emailTextBox.value), \
                                validation={'ERROR: Your email is longer then 48 characters': lambda e: len(e) <= GC.MAX_EMAIL_LENGHT}).classes('w-80')
        invalidEmailLabel = ui.label()
        invalidEmailLabel.visible = False
        submitButton = ui.button("SUMBIT CONFIG", on_click=lambda e: send_email(emailTextBox.value)).classes('w-80')

    ui.run(native=GC.RUN_ON_NATIVE_OS, port=GC.LOCAL_HOST_PORT_FOR_GUI)
