# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
from . import preferences
from . import operators
from . import ui


def draw(self, context):
    addon_prefs = bpy.context.preferences.addons[__package__]

    layout = self.layout
    
    obj = context.object
    
    row = layout.row()
    col = row.column(align=True)

    col.template_list(
        'MODIFIER_UL_modifier_stack', '', obj, 'modifiers', obj,
        'active_modifier_index', rows=addon_prefs.preferences.default_list_height
    )

    col.separator()


    if addon_prefs.preferences.use_apply_buttons:
        row_apply = col.row(align=True)

        row_apply.operator("object.msm_modifier_apply", text="Apply")
        row_apply.operator("object.msm_modifier_apply_all", text='Apply All')
    
        layout.separator()
    
    col = row.column(align=True)

    if addon_prefs.preferences.use_add_remove_buttons:
        if addon_prefs.preferences.use_modifier_search:
            col.operator("wm.search_single_menu", text='', icon='ADD').menu_idname = "OBJECT_MT_modifier_add"
        else:
            col.operator("wm.call_menu", text='', icon='ADD').name = "OBJECT_MT_modifier_add"
            
        col.operator("object.msm_modifier_remove", icon='REMOVE', text="")

        if addon_prefs.preferences.use_duplicate_button:
            col.separator()

            col.operator("object.msm_modifier_copy", icon='DUPLICATE', text="")

        col.separator()

        col.operator("object.msm_modifier_move", icon='TRIA_UP', text="").direction = 'UP'
        col.operator("object.msm_modifier_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

    else:
        col.operator("object.msm_modifier_move", icon='TRIA_UP', text="").direction = 'UP'
        col.operator("object.msm_modifier_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

        if addon_prefs.preferences.use_duplicate_button:
            col.separator()

            col.operator("object.msm_modifier_copy", icon='DUPLICATE', text="")

    col.separator()
    
    col.menu("MODIFIER_MT_dropdown_menu", icon='DOWNARROW_HLT', text="")


cls = (
    operators,
    preferences,
    ui
)

addon_keymaps = []


def register():
    def update_active_modifier(self, context):
        obj = context.object

        if len(obj.modifiers) > 0:
            obj.modifiers.active = obj.modifiers[self.active_modifier_index]

    bpy.types.Object.active_modifier_index = bpy.props.IntProperty(
        default=0,
        min=0,
        update=update_active_modifier
    )

    for cl in cls:
        cl.register()

    bpy.types.DATA_PT_modifiers.prepend(draw)        

    keymaps = [
        {
            "idname": "object.msm_modifier_move",
            "type": 'UP_ARROW',
            "value": 'PRESS',
            "ctrl": True,
            "shift": True,
            "alt": False,
            "properties": {
                "direction": 'UP'
            }
        },
        {
            "idname": "object.msm_modifier_move",
            "type": 'DOWN_ARROW',
            "value": 'PRESS',
            "ctrl": True,
            "shift": True,
            "alt": False,
            "properties": {
                "direction": 'DOWN'
            }
        },
        {
            "idname": "object.msm_modifier_apply_all",
            "type": 'A',
            "value": 'PRESS',
            "ctrl": True,
            "shift": True,
            "alt": False,
        },
        {
            "idname": "object.msm_modifier_remove",
            "type": 'X',
            "value": 'PRESS',
            "ctrl": True,
            "shift": True,
            "alt": False,
            "properties": {
                "all": True
            }
        },
        {
            "idname": "object.msm_modifier_expand_selected_only",
            "type": 'E',
            "value": 'PRESS',
            "ctrl": False,
            "shift": True,
            "alt": False,
        },
        {
            "idname": "object.msm_modifier_collapse_all",
            "type": 'C',
            "value": 'PRESS',
            "ctrl": False,
            "shift": True,
            "alt": False,
        },
    ]

    keymap_config = bpy.context.window_manager.keyconfigs.addon

    if keymap_config:
        km = keymap_config.keymaps.new(name="Property Editor", space_type='PROPERTIES')

        for keymap in keymaps:
            kmi = km.keymap_items.new(
                keymap["idname"], keymap["type"], keymap["value"],
                ctrl=keymap["ctrl"], shift=keymap["shift"], alt=keymap["alt"]
            )

            if "properties" in keymap.keys():
                for property, value in keymap["properties"].items():
                    setattr(kmi.properties, property, value)

            addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    bpy.types.DATA_PT_modifiers.remove(draw)

    for cl in reversed(cls):
        cl.unregister()

    del(bpy.types.Object.active_modifier_index)


if __name__ == "__main__":
    register()
