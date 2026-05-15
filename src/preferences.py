import bpy


class ModifierStackManagerPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    use_add_remove: bpy.props.BoolProperty(
        name="Show +/- buttons",
        description="Show +/- buttons to add/remove modifiers",
        default=True
    )

    use_modifier_search: bpy.props.BoolProperty(
        name="Use Modifier Search",
        description="On pressing the + button, show modifier search instead of menu with categories",
        default=True
    )

    default_list_height: bpy.props.IntProperty(
        name="Default List Height",
        description="Default list height in number of modifier items to display",
        default=5,
        min=5
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        layout.prop(self, "use_add_remove")
        layout.prop(self, "use_modifier_search")
        layout.prop(self, "default_list_height")


def register():
    bpy.utils.register_class(ModifierStackManagerPreferences)


def unregister():
    bpy.utils.unregister_class(ModifierStackManagerPreferences)


if __name__ == "__main__":
    register()