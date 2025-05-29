import bpy
from collections import Counter


class ModifierOperator(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object

        supported_types = {
            'MESH', 'CURVE', 'CURVES', 'FONT', 'SURFACE',
            'LATTICE', 'GREASEPENCIL', 'VOLUME'
        }

        return (
            obj is not None \
                and obj.type in supported_types
                and len(context.object.modifiers) > 0
        )

    @staticmethod
    def get_modifier_index(modifier):
        obj = modifier.id_data
        return list(obj.modifiers).index(modifier)

    @staticmethod
    def get_expand_state_count(modifiers):
        expand_states = [True if modifier.show_expanded else False \
                                    for modifier in modifiers]

        return Counter(expand_states)