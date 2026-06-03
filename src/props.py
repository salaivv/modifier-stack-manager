import bpy


def get_active_modifier_index(self):
    if self.modifiers:
        return self.modifiers.find(self.modifiers.active.name)
    
    return 0


def set_active_modifier_index(self, value):
    if self.modifiers:
        self.modifiers[value].is_active = True


def register():
    bpy.types.Object.active_modifier_index = bpy.props.IntProperty(
        default=0,
        min=0,
        get=get_active_modifier_index,
        set=set_active_modifier_index
    )

def unregister():
    del bpy.types.Object.active_modifier_index