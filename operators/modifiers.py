import bpy
from bpy.types import Operator


class ModifierMove(Operator):
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