import bpy
from .common import ModifierOperator


class ModifierMove(ModifierOperator):
    bl_idname = 'object.modifier_move'
    bl_label = 'Modifier Move Up'
    
    direction: bpy.props.EnumProperty(
        items=[
            ("UP", "Up", "", 1),
            ("DOWN", "Down", "", 2),
        ],
    )
    
    def execute(self, context):
        obj = context.object

        if self.direction == 'UP':
            if obj.active_modifier_index == 0:
                return {'CANCELLED'}
            
            ret = bpy.ops.object.modifier_move_up(
                modifier=obj.modifiers[obj.active_modifier_index].name
            )

            if ret == {'CANCELLED'}:
                self.report({'WARNING'}, "Cannot move modifier up.")
                return {'CANCELLED'}

            obj.active_modifier_index -= 1

        elif self.direction == 'DOWN':
            if obj.active_modifier_index == len(obj.modifiers)-1:
                return {'CANCELLED'}
            
            ret = bpy.ops.object.modifier_move_down(
                modifier=obj.modifiers[obj.active_modifier_index].name
            )

            if ret == {'CANCELLED'}:
                self.report({'WARNING'}, "Cannot move modifier down.")
                return {'CANCELLED'}

            obj.active_modifier_index += 1
        
        return {'FINISHED'}
    

class ModifierCopy(ModifierOperator):
    bl_idname = 'object.copy_modifier'
    bl_label = 'Copy Modifier'
    
    def execute(self, context):
        obj = context.object
        modifier = obj.modifiers[obj.active_modifier_index]
        bpy.ops.object.modifier_copy(modifier=modifier.name)
        obj.active_modifier_index += 1
        
        return {'FINISHED'}


class ModifierApplyRemove(ModifierOperator):
    bl_idname = 'object.apply_remove_modifier'
    bl_label = 'Remove Modifier'

    mode: bpy.props.EnumProperty(
        items=[
            ("APPLY", "Apply", "", 1),
            ("REMOVE", "Remove", "", 2),
        ],
    )
    
    def execute(self, context):
        obj = context.object

        modifier = obj.modifiers[obj.active_modifier_index]

        if self.mode == 'APPLY':
            try:
                bpy.ops.object.modifier_apply(modifier=modifier.name)
            except Exception as e:
                print(str(e))
                self.report({'ERROR'}, "Cannot apply modifier.")
                return {'CANCELLED'}
        else:
            bpy.ops.object.modifier_remove(modifier=modifier.name)

        if obj.active_modifier_index == len(obj.modifiers):
            obj.active_modifier_index -= 1
            
        return {'FINISHED'}


class ModifierApplyAll(ModifierOperator):
    bl_idname = 'object.apply_all_modifiers'
    bl_label = 'Apply All'
    
    @classmethod
    def poll(cls, context):
        return (
            super().poll(context) \
                and context.mode == 'OBJECT'
        )
    
    def execute(self, context):
        obj = context.object

        failed = False
        for mod in obj.modifiers:
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                failed = True
                print(str(e))
                self.report({'WARNING'}, 'Failed to apply all modifiers.')

        if failed:
            active_mod = obj.modifiers.active
            obj.active_modifier_index = ModifierOperator.get_modifier_index(active_mod)

        return {'FINISHED'}
        

class ModifierExpandCollapse(ModifierOperator):
    bl_idname = 'object.expand_collapse_modifiers'
    bl_label = 'Expand/Collapse'
    
    def execute(self, context):
        obj = context.object

        mod = obj.modifiers[obj.active_modifier_index]
        mod.show_expanded = not mod.show_expanded
            
        for area in context.screen.areas:
            area.tag_redraw()
            
        return {'FINISHED'}