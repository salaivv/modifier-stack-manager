import bpy


class ModifierStackManagerPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    use_add_remove: bpy.props.BoolProperty(
        name="Show +/- buttons",
        description="Show +/- buttons to add/remove modifiers",
        default=True
    )

    default_list_height: bpy.props.IntProperty(
        name="Default List Height",
        description="Default list height in number of modifier items to display",
        default=5
    )

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        col.label(text="Preferences")
        col.prop(self, "use_add_remove")
        col.prop(self, "default_list_height")


def register():
    bpy.utils.register_class(ModifierStackManagerPreferences)


def unregister():
    bpy.utils.unregister_class(ModifierStackManagerPreferences)


if __name__ == "__main__":
    register()