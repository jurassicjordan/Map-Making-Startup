# SPDX-FileCopyrightText: 2020-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

# Custom template works best with lockview, ERF-levelbuddy and ERF-Gridsnapper
#link to lockview https://gist.github.com/Fweeb/bb61c15139bff338cb17
#link to ERF-levelbuddy https://github.com/EvilReFlex/ERF_LevelBuddyBlender
#link to ERF-Gridsnapper https://discord.gg/bGmQvbKV
import bpy
from bpy.app.handlers import persistent


def update_factory_startup_screens():
    # Map Making kinda like the hammer editor
    screen = bpy.data.screens["Map Making"]

@persistent
def load_handler(dummy):
    pass


def register():
    bpy.app.handlers.load_factory_startup_post.append(load_handler)


def unregister():
    bpy.app.handlers.load_factory_startup_post.remove(load_handler)
'''    for area in screen.areas:
        if area.type == 'PROPERTIES':
            # Set Tool settings as default in properties panel.
            space = area.spaces.active
            space.context = 'TOOL'
        elif area.type == 'DOPESHEET_EDITOR':
            # Open sidebar in Dope-sheet.
            space = area.spaces.active
            space.show_region_ui = True

    # 2D Full Canvas.
    screen = bpy.data.screens["2D Full Canvas"]
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            space.shading.type = 'MATERIAL'
            space.shading.use_scene_world = True


def update_factory_startup_scenes():
    for scene in bpy.data.scenes:
        scene.tool_settings.use_keyframe_insert_auto = True
        scene.tool_settings.gpencil_sculpt.use_scale_thickness = True


def update_factory_startup_grease_pencils():
    for gpd in bpy.data.grease_pencils:
        gpd.onion_keyframe_type = 'ALL'


@persistent
def load_handler(_):
    update_factory_startup_screens()
    update_factory_startup_scenes()
    update_factory_startup_grease_pencils()


def register():
    bpy.app.handlers.load_factory_startup_post.append(load_handler)


def unregister():
    bpy.app.handlers.load_factory_startup_post.remove(load_handler)
'''
