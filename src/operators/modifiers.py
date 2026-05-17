import bpy
from .common import ModifierOperator


class ModifierMove(ModifierOperator):
    bl_idname = "object.msm_modifier_move"
    bl_label = "Modifier Move"
    
    direction: bpy.props.EnumProperty(
        items=[
            ("UP", "Up", "", 1),
            ("DOWN", "Down", "", 2),
        ],
    )

    move_to_end: bpy.props.BoolProperty(
        name="Move to End",
        default=False
    )

    def invoke(self, context, event):
        self.move_to_end = event.shift and event.ctrl is False
        return self.execute(context)
    
    def execute(self, context):
        obj = context.object

        to_index = None

        if self.direction == 'UP':
            if obj.active_modifier_index == 0:
                return {'CANCELLED'}

            to_index = 0 if self.move_to_end else obj.active_modifier_index - 1

        elif self.direction == 'DOWN':
            if obj.active_modifier_index == len(obj.modifiers)-1:
                return {'CANCELLED'}

            to_index = len(obj.modifiers)-1 if self.move_to_end else obj.active_modifier_index + 1

        try:
            obj.modifiers.move(
                obj.active_modifier_index,
                to_index
            )

            obj.active_modifier_index = to_index

        except RuntimeError as e:
            self.report({'WARNING'}, str(e))
            return {'CANCELLED'}
        
        return {'FINISHED'}
    

class ModifierCopy(ModifierOperator):
    bl_idname = "object.msm_modifier_copy"
    bl_label = "Copy Modifier"
    
    def execute(self, context):
        obj = context.object
        modifier = obj.modifiers[obj.active_modifier_index]
        bpy.ops.object.modifier_copy(modifier=modifier.name)
        obj.active_modifier_index += 1
        
        return {'FINISHED'}


class ModifierApply(ModifierOperator):
    bl_idname = "object.msm_modifier_apply"
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


class ModifierApplyAll(ModifierOperator):
    bl_idname = "object.msm_modifier_apply_all"
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

        self.report({'INFO'}, "Applied all modifiers.")

        return {'FINISHED'}


class ModifierRemove(ModifierOperator):
    bl_idname = "object.msm_modifier_remove"
    bl_label = "Remove Modifier"

    all: bpy.props.BoolProperty(
        name="Remove All",
        default=False
    )
    
    def execute(self, context):
        obj = context.object

        if self.all:
            obj.modifiers.clear()
            obj.active_modifier_index = 0
            self.report({'INFO'}, "Removed all modifiers.")

            return {'FINISHED'}

        modifier = obj.modifiers[obj.active_modifier_index]

        bpy.ops.object.modifier_remove(modifier=modifier.name)

        if obj.active_modifier_index == len(obj.modifiers):
            obj.active_modifier_index -= 1
            
        return {'FINISHED'}


class ModifierExpandSelectedOnly(ModifierOperator):
    bl_idname = "object.msm_modifier_expand_selected_only"
    bl_label = "Expand Selected Modifier Only"
    bl_description = "Expand the selected modifier and collapse the rest"

    def execute(self, context):
        obj = context.object

        active_modifier = obj.modifiers[obj.active_modifier_index]

        for modifier in obj.modifiers:
            if not modifier is active_modifier:
                modifier.show_expanded = False
        
        active_modifier.show_expanded = True

        return {'FINISHED'}