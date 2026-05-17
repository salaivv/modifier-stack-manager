import bpy


class ModifierOperator(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        space_data = context.space_data
        if not space_data.type == 'PROPERTIES':
            return False

        obj = context.object

        supported_types = {
            'MESH', 'CURVE', 'CURVES', 'FONT', 'SURFACE',
            'LATTICE', 'GREASEPENCIL', 'VOLUME'
        }

        return (
            obj is not None \
                and obj.type in supported_types
                and len(context.object.modifiers) > 0
                and space_data.context == 'MODIFIER'
        )

    @staticmethod
    def get_modifier_index(modifier):
        obj = modifier.id_data
        return list(obj.modifiers).index(modifier)