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

bl_info = {
    "name": "Modifier Stack Manager",
    "author": "Salai Vedha Viradhan",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "Properties > Modifiers",
    "description": "Implements a UIList for a modifier stack operations",
    "warning": "Work in progess",
    "category": "3D View"
    }


import bpy
from bpy.types import Panel, UIList, Operator
from bpy.props import IntProperty

class ModifierMoveUp(Operator):
    bl_idname = 'object.modifier_moveup'
    bl_label = 'Modifier Move Up'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        obj = context.active_object
        if len(obj.modifiers) == 0 or obj.active_modifier_index == 0:
            return {'CANCELLED'}
        else:
            bpy.ops.object.modifier_move_up(modifier=obj.modifiers[obj.active_modifier_index].name)
            obj.active_modifier_index -= 1
        
        return {'FINISHED'}


class ModifierMoveDown(Operator):
    bl_idname = 'object.modifier_movedown'
    bl_label = 'Modifier Move Down'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        obj = context.active_object
        if len(obj.modifiers) == 0 or obj.active_modifier_index == len(obj.modifiers)-1:
            return {'CANCELLED'}
        else:
            bpy.ops.object.modifier_move_down(modifier=obj.modifiers[obj.active_modifier_index].name)
            obj.active_modifier_index += 1
        
        return {'FINISHED'}
    

class ModifierCopy(Operator):
    bl_idname = 'object.copy_modifier'
    bl_label = 'Copy Modifier'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        obj = context.active_object
        if len(obj.modifiers) == 0:
            return {'CANCELLED'}
        else:
            bpy.ops.object.modifier_copy(modifier=obj.modifiers[obj.active_modifier_index].name)
            obj.active_modifier_index += 1
        
        return {'FINISHED'}


class ModifierRemove(Operator):
    bl_idname = 'object.remove_modifier'
    bl_label = 'Remove Modifier'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        obj = context.active_object
        if len(obj.modifiers) == 0:
            self.report({'INFO'}, 'No modifiers to remove.')
            return {'CANCELLED'}
        else:
            if obj.active_modifier_index == 0:
                bpy.ops.object.modifier_remove(modifier=obj.modifiers[obj.active_modifier_index].name)
            else:
                bpy.ops.object.modifier_remove(modifier=obj.modifiers[obj.active_modifier_index].name)
                obj.active_modifier_index -= 1
            
        return {'FINISHED'}


class ModifierApplyAll(Operator):
    bl_idname = 'object.apply_all_modifiers'
    bl_label = 'Apply All'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        obj = context.active_object
        if len(obj.modifiers) == 0:
            self.report({'INFO'}, 'No modifiers to apply.')
            return {'CANCELLED'}
        elif context.mode == 'EDIT_MESH':
            self.report({'INFO'}, 'Modifiers cannot be applied in edit mode.')
            return {'CANCELLED'}
        else:
            for mod in obj.modifiers:
                try:
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
                except:
                    self.report({'INFO'}, 'Failed to apply all modifiers.')
        return {'FINISHED'}
        

class ModifierExpandCollapse(Operator):
    bl_idname = 'object.expand_collapse_modifiers'
    bl_label = 'Expand/Collapse'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        obj = context.active_object
        if (len(obj.modifiers)):
            vs = 0
            for mod in obj.modifiers:
                if (mod.show_expanded):
                    vs += 1
                else:
                    vs -= 1
            is_close = False
            if (0 < vs):
                is_close = True
            for mod in obj.modifiers:
                mod.show_expanded = not is_close
        else:
            self.report({'INFO'}, "No modifiers to Expand/Collapse")
            return {'CANCELLED'}
            
        for area in context.screen.areas:
            area.tag_redraw()
            
        return {'FINISHED'}


class MODIFIER_UL_modifier_stack(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        ob = data
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
        md_type = md.type
        md_icon = bpy.types.Modifier.bl_rna.properties['type'].enum_items[md_type].icon
        return md_icon
     
    
def draw(self, context):
    layout = self.layout
    
    ob = context.object
    
    if ob:
        row = layout.row()
        row.label(text='Modifiers')
        row = layout.row()
        col = row.column(align=True)
        col.template_list('MODIFIER_UL_modifier_stack', '', ob, 'modifiers', ob, 'active_modifier_index')
        col.separator()
        col = col.row(align=True)
        col.operator('object.apply_all_modifiers', text='Apply All')
        col.operator('object.expand_collapse_modifiers', text='Expand/Collapse')
        
        layout.separator()
        
        col = row.column(align=True)
        col.operator("object.modifier_add", text='', icon='ADD')
        col.operator("object.remove_modifier", icon='REMOVE', text="")
        col.separator()
        col.operator("object.copy_modifier", icon='DUPLICATE', text="")
        col.separator()
        col.operator("object.modifier_moveup", icon='TRIA_UP', text="")
        col.operator("object.modifier_movedown", icon='TRIA_DOWN', text="")
                

cls = (
    ModifierMoveUp,
    ModifierMoveDown,
    ModifierRemove,
    ModifierApplyAll,
    ModifierCopy,
    ModifierExpandCollapse,
    MODIFIER_UL_modifier_stack
)
  
def register():
    bpy.types.Object.active_modifier_index = IntProperty(default=0)
    from bpy.utils import register_class
    for cl in cls:
        register_class(cl)
    bpy.types.DATA_PT_modifiers.prepend(draw)        

def unregister():
    from bpy.utils import unregister_class
    for cl in reversed(cls):
        unregister_class(cl)
    bpy.types.DATA_PT_modifiers.remove(draw)
    del(bpy.types.Object.active_modifier_index)


if __name__ == "__main__":
    register()
