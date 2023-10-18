#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "GPLv3"
__status__     = "Development
__deprecated__ = False
__version__    = "0.0.1"
__doc__        = "CONSTANTS for both LiteHouse and Lustron home configurations"
"""
TODO = -1  

# Disable PyLint linting messages
# https://pypi.org/project/pylint/
# pylint: disable=invalid-name

LITEHOUSE = 'LITEHOUSE'
LUSTRON = 'LUSTRON'

RUN_ON_NATIVE_OS = False
TUNNEL_TO_INTERNET = True
LOCAL_HOST_PORT_FOR_GUI = 8181

LOCAL_MAC_CODE_DIRECTORY   = '/Users/venus/GitRepos/Product-Congfiguration'
LINODE_LINUX_CODE_DIRECTORY = '/root/Product-Congfiguration/'
WINDOWS_CODE_DIRECTORY = 'C:/Users/Framecad/HomeControlGUIs'

MAMMOTH_BRIGHT_GRREN = '#03C04A'

VIEWS = ['Floor Plan', 'Exterior', 'Interior', 'Roof', 'Extras']
FLOOR_PLAN_VIEW_NUM = 0
EXTERIOR_VIEW_NUM = 1
INTERIOR_VIEW_NUM = 2
ROOF_VIEW_NUM = 3
EXTRAS_VIEW_NUM = 4


FLOOR_PLAN_TYPES = ['LiteHouse', 'Lustron', 'POD']
EXTERIOR_MATERIALS = ['White', 'Red', 'Brown']


MAX_EMAIL_LENGHT = 47