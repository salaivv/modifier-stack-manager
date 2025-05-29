import bpy
from .common import ModifierOperator
from collections import Counter


class ModifierMove(ModifierOperator):
    bl_idname = f"object.modifier_move"
    bl_label = "Modifier Move Up"
    
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
    bl_idname = f"object.copy_modifier"
    bl_label = "Copy Modifier"
    
    def execute(self, context):
        obj = context.object
        modifier = obj.modifiers[obj.active_modifier_index]
        bpy.ops.object.modifier_copy(modifier=modifier.name)
        obj.active_modifier_index += 1
        
        return {'FINISHED'}


class ModifierApply(ModifierOperator):
    bl_idname = f"object.apply_modifier"
    bl_label = "Apply Modifier"

    @classmethod
    def poll(cls, context):
        return (
            super().poll(context) \
                and context.mode == 'OBJECT'
                and context.object.type in {
                    'MESH', 'CURVES', 'LATTICE', 'GREASEPENCIL'
                }
        )
    
    def execute(self, context):
        obj = context.object
        modifier = obj.modifiers[obj.active_modifier_index]

        try:
            bpy.ops.object.modifier_apply(modifier=modifier.name)
        except Exception as e:
            print(str(e))
            self.report({'ERROR'}, "Cannot apply this modifier.")
            return {'CANCELLED'}

        if obj.active_modifier_index == len(obj.modifiers):
            obj.active_modifier_index -= 1
            
        return {'FINISHED'}


class ModifierRemove(ModifierOperator):
    bl_idname = f"object.remove_modifier"
    bl_label = "Remove Modifier"
    
    def execute(self, context):
        obj = context.object
        modifier = obj.modifiers[obj.active_modifier_index]

        bpy.ops.object.modifier_remove(modifier=modifier.name)

        if obj.active_modifier_index == len(obj.modifiers):
            obj.active_modifier_index -= 1
            
        return {'FINISHED'}


class ModifierApplyAll(ModifierOperator):
    bl_idname = f"object.apply_all_modifiers"
    bl_label = "Apply All"
    
    @classmethod
    def poll(cls, context):
        return (
            super().poll(context) \
                and context.mode == 'OBJECT'
                and context.object.type in {
                    'MESH', 'CURVE', 'CURVES', 'FONT',
                    'SURFACE', 'LATTICE', 'GREASEPENCIL'
                }
        )
    
    def execute(self, context):
        obj = context.object

        failed = False

        if obj.type in {'MESH', 'CURVE', 'FONT', 'SURFACE'}:
            bpy.ops.object.convert(target='MESH')

        elif obj.type == 'CURVES':
            bpy.ops.object.convert(target='CURVES')

        elif obj.type in {'LATTICE', 'GREASEPENCIL'}:
            for mod in obj.modifiers:
                try:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
                except Exception as e:
                    failed = True
                    print(str(e))
                    self.report({'WARNING'}, "Failed to apply all modifiers.")

        if failed:
            active_mod = obj.modifiers.active
            obj.active_modifier_index = ModifierOperator.get_modifier_index(active_mod)

        return {'FINISHED'}
        

class ModifierExpandCollapse(ModifierOperator):
    bl_idname = f"object.expand_collapse_modifiers"
    bl_label = "Expand/Collapse Modifiers"
    
    affect: bpy.props.EnumProperty(
        name="Affect",
        items=[
            ('ACTIVE', "Active", "", 1),
            ('ALL', "All", "", 2)
        ],
        default=1,
        options={'SKIP_SAVE'}
    )

    def execute(self, context):
        obj = context.object

        if self.affect == 'ACTIVE':
            mod = obj.modifiers[obj.active_modifier_index]
            mod.show_expanded = not mod.show_expanded
        else:
            state_count = ModifierOperator.get_expand_state_count(obj.modifiers)

            expand = True
            if state_count[True] > state_count[False]:
                expand = False

            for modifier in obj.modifiers:
                modifier.show_expanded = expand
            
        for area in context.screen.areas:
            area.tag_redraw()
            
        return {'FINISHED'}