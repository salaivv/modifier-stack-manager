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
from .operators.modifiers import *
from .ui.modifier_list import MODIFIER_UL_modifier_stack
from .preferences import ModifierStackManagerPreferences

     
def draw(self, context):
    addon_prefs = bpy.context.preferences.addons[__package__]
    layout = self.layout
    
    ob = context.object
    
    if ob:
        row = layout.row()
        row.label(text='Modifiers')
        row = layout.row()
        col = row.column(align=True)

        col.template_list('MODIFIER_UL_modifier_stack', '', ob, 'modifiers', \
            ob, 'active_modifier_index', rows=addon_prefs.preferences.default_list_height)

        col.separator()
        col = col.row(align=True)
        col.operator('object.apply_all_modifiers', text='Apply All')
        col.operator('object.expand_collapse_modifiers', text='Expand/Collapse')
        
        layout.separator()
        
        col = row.column(align=True)

        if addon_prefs.preferences.use_add_remove:
            col.operator("object.modifier_add", text='', icon='ADD')
            col.operator("object.remove_modifier", icon='REMOVE', text="")
            col.separator()

        col.operator("object.copy_modifier", icon='DUPLICATE', text="")
        col.separator()
        col.operator("object.modifier_move", icon='TRIA_UP', text="").direction = 'UP'
        col.operator("object.modifier_move", icon='TRIA_DOWN', text="").direction = 'DOWN'


cls = (
    ModifierMove,
    ModifierCopy,
    ModifierRemove,
    ModifierApplyAll,
    ModifierExpandCollapse,
    ModifierStackManagerPreferences,
    MODIFIER_UL_modifier_stack
)

addon_keymaps = []


def register():
    from bpy.props import IntProperty
    from bpy.utils import register_class

    def sync_active_modifier(self, context):
        obj = context.active_object
        obj.modifiers.active = obj.modifiers[self.active_modifier_index]

    bpy.types.Object.active_modifier_index = IntProperty(
        default=0,
        min=0,
        update=sync_active_modifier
    )

    for cl in cls:
        register_class(cl)

    bpy.types.DATA_PT_modifiers.prepend(draw)        

    keymap_config = bpy.context.window_manager.keyconfigs.addon

    if keymap_config:
        km = keymap_config.keymaps.new(
            name='Object Mode', space_type='EMPTY'
        )

        kmi = km.keymap_items.new(
            "object.apply_all_modifiers", 'A', 'PRESS', \
                                ctrl=True, shift=True, alt=True
        )

        addon_keymaps.append((km, kmi))



def unregister():
    from bpy.utils import unregister_class

    for km, kmi_idname in addon_keymaps:
        for kmi in km.keymap_items:
            if kmi.idname == kmi_idname:
                km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    bpy.types.DATA_PT_modifiers.remove(draw)

    for cl in reversed(cls):
        unregister_class(cl)

    del(bpy.types.Object.active_modifier_index)


if __name__ == "__main__":
    register()
