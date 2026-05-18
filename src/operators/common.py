import bpy


def is_instanced(obj):
    user_map = bpy.data.user_map(subset=[obj.data])
    users = [user for user in user_map[obj.data] if user.id_type == 'OBJECT']
    
    if len(users) > 1:
        return True
    
    return False


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


class ModifierApplyOperator(ModifierOperator):
    def invoke(self, context, event):
        self.data_is_instanced = False

        if is_instanced(context.object):
            self.data_is_instanced = True

            return context.window_manager.invoke_confirm(
                self, event, title=self.bl_label, confirm_text="Yes", icon='WARNING',
                message=("The active object is an instance. Make object data single-user "
                         "and then apply?")
            )
        
        return self.execute(context)