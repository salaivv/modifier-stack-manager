import bpy


class ModifierOperator(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (
            context.object is not None \
                and len(context.object.modifiers) > 0
        )