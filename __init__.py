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


ops_category = "mod_stack_man"


import bpy
from . import preferences
from . import operators
from . import ui


def draw(self, context):
    addon_prefs = bpy.context.preferences.addons[__package__]
    layout = self.layout
    
    obj = context.object
    
    if obj:
        row = layout.row()
        col = row.column(align=True)

        col.template_list(
            'MODIFIER_UL_modifier_stack', '', obj, 'modifiers', obj,
            'active_modifier_index', rows=addon_prefs.preferences.default_list_height
        )

        col.separator()
        col = col.row(align=True)
        col.operator(f"{ops_category}.apply_remove_modifier", text="Apply").mode = 'APPLY'
        col.operator(f"{ops_category}.apply_all_modifiers", text='Apply All')
        
        layout.separator()
        
        col = row.column(align=True)

        if addon_prefs.preferences.use_add_remove:
            col.operator("object.modifier_add", text='', icon='ADD')
            col.operator(f"{ops_category}.apply_remove_modifier", icon='REMOVE', text="").mode = 'REMOVE'
            col.separator()

        col.operator(f"{ops_category}.copy_modifier", icon='DUPLICATE', text="")
        col.separator()
        col.operator(f"{ops_category}.modifier_move", icon='TRIA_UP', text="").direction = 'UP'
        col.operator(f"{ops_category}.modifier_move", icon='TRIA_DOWN', text="").direction = 'DOWN'


cls = (
    operators,
    preferences,
    ui
)

addon_keymaps = []


def register():
    from bpy.props import IntProperty
    from bpy.utils import register_class

    def update_active_modifier(self, context):
        obj = context.object
        obj.modifiers.active = obj.modifiers[self.active_modifier_index]

    bpy.types.Object.active_modifier_index = IntProperty(
        default=0,
        min=0,
        update=update_active_modifier
    )

    for cl in cls:
        cl.register()

    bpy.types.DATA_PT_modifiers.prepend(draw)        

    keymap_config = bpy.context.window_manager.keyconfigs.addon

    if keymap_config:
        km = keymap_config.keymaps.new(name='Object Mode')

        kmi = km.keymap_items.new(
            "object.apply_all_modifiers", 'A', 'PRESS',
            ctrl=True, shift=True
        )

        addon_keymaps.append((km, kmi))


def unregister():
    from bpy.utils import unregister_class

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    bpy.types.DATA_PT_modifiers.remove(draw)

    for cl in reversed(cls):
        cl.unregister()

    del(bpy.types.Object.active_modifier_index)


if __name__ == "__main__":
    register()
