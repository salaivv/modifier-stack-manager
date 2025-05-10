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
from bpy.types import Panel, UIList, Operator
from bpy.props import IntProperty


class ModifierMove(bpy.types.Operator):
    bl_idname = 'object.modifier_move'
    bl_label = 'Modifier Move Up'
    bl_options = {'REGISTER', 'UNDO'}
    
    direction: bpy.props.EnumProperty(
        items=[
            ("UP", "Up", "", 1),
            ("DOWN", "Down", "", 2),
        ],
    )
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None \
            and len(context.object.modifiers) > 0
    
    def execute(self, context):
        obj = context.active_object

        if self.direction == 'UP':
            if obj.active_modifier_index == 0:
                return {'CANCELLED'}
            
            bpy.ops.object.modifier_move_up(
                modifier=obj.modifiers[obj.active_modifier_index].name
            )

            obj.active_modifier_index -= 1

        elif self.direction == 'DOWN':
            if obj.active_modifier_index == len(obj.modifiers)-1:
                return {'CANCELLED'}
            
            bpy.ops.object.modifier_move_down(
                modifier=obj.modifiers[obj.active_modifier_index].name
            )

            obj.active_modifier_index += 1
        
        return {'FINISHED'}
    

class ModifierCopy(Operator):
    bl_idname = 'object.copy_modifier'
    bl_label = 'Copy Modifier'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None \
            and len(context.object.modifiers) > 0
    
    def execute(self, context):
        obj = context.active_object
        modifier = obj.modifiers[obj.active_modifier_index]
        bpy.ops.object.modifier_copy(modifier=modifier.name)
        obj.active_modifier_index += 1
        
        return {'FINISHED'}


class ModifierRemove(Operator):
    bl_idname = 'object.remove_modifier'
    bl_label = 'Remove Modifier'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None \
            and len(context.object.modifiers) > 0
    
    def execute(self, context):
        obj = context.active_object

        modifier = obj.modifiers[obj.active_modifier_index]

        bpy.ops.object.modifier_remove(modifier=modifier.name)

        if obj.active_modifier_index != 0:
            obj.active_modifier_index -= 1
            
        return {'FINISHED'}


class ModifierApplyAll(Operator):
    bl_idname = 'object.apply_all_modifiers'
    bl_label = 'Apply All'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None \
            and len(context.object.modifiers) > 0 \
            and context.mode == 'OBJECT'
    
    def execute(self, context):
        obj = context.active_object

        for mod in obj.modifiers:
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                print(str(e))
                self.report({'INFO'}, 'Failed to apply all modifiers.')

        return {'FINISHED'}
        

class ModifierExpandCollapse(Operator):
    bl_idname = 'object.expand_collapse_modifiers'
    bl_label = 'Expand/Collapse'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None \
            and len(context.object.modifiers) > 0
    
    def execute(self, context):
        obj = context.active_object

        mod = obj.modifiers[obj.active_modifier_index]
        mod.show_expanded = not mod.show_expanded
            
        for area in context.screen.areas:
            area.tag_redraw()
            
        return {'FINISHED'}


class MODIFIER_UL_modifier_stack(UIList):
    def draw_item(
        self, context, layout, data, item, 
        icon, active_data, active_propname, index
    ):
        md = item
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            
            row.prop(md, 'name', text="", emboss=False, icon_value=1, icon = self.get_mod_icon(md))
            row.prop(md, 'show_render', text="", emboss=False, icon_only=True)
            row.prop(md, 'show_viewport', text="", emboss=False, icon_only=True)

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='', icon_value=icon)
            
    def get_mod_icon(self, md):
        md_icon = bpy.types.Modifier.bl_rna.properties['type'].enum_items[md.type].icon
        return md_icon
     
    
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
                

class ModiferStackManagerPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    use_add_remove: bpy.props.BoolProperty(
        name="Show +/- buttons",
        description="Show +/- buttons to add/remove modifiers",
        default=True)

    default_list_height: bpy.props.IntProperty(
        name="Default List Height",
        description="Default list height in number of modifier items to display",
        default=5)

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        col.label(text="Preferences")
        col.prop(self, "use_add_remove")
        col.prop(self, "default_list_height")


cls = (
    ModifierMove,
    ModifierCopy,
    ModifierRemove,
    ModifierApplyAll,
    ModifierExpandCollapse,
    ModiferStackManagerPreferences,
    MODIFIER_UL_modifier_stack
)

addon_keymaps = []


def register():
    def sync_active_modifier(self, context):
        obj = context.active_object
        obj.modifiers.active = obj.modifiers[self.active_modifier_index]

    bpy.types.Object.active_modifier_index = IntProperty(
        default=0,
        min=0,
        update=sync_active_modifier
    )

    from bpy.utils import register_class
    for cl in cls:
        register_class(cl)

    keymap_config = bpy.context.window_manager.keyconfigs.addon

    if keymap_config:
        km = keymap_config.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("object.apply_all_modifiers", 'A', 'PRESS', \
                                    ctrl=True, shift=True, alt=True)
        addon_keymaps.append((km, kmi))

    bpy.types.DATA_PT_modifiers.prepend(draw)        


def unregister():
    from bpy.utils import unregister_class

    for km, kmi_idname in addon_keymaps:
        for kmi in km.keymap_items:
            if kmi.idname == kmi_idname:
                km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    for cl in reversed(cls):
        unregister_class(cl)

    bpy.types.DATA_PT_modifiers.remove(draw)

    del(bpy.types.Object.active_modifier_index)


if __name__ == "__main__":
    register()
