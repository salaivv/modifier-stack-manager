import bpy


class ModifierStackManagerPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    use_add_remove_buttons: bpy.props.BoolProperty(
        name="Show +/- Buttons",
        description="Show +/- buttons to add/remove modifiers",
        default=True
    )

    use_duplicate_button: bpy.props.BoolProperty(
        name="Show Duplicate Button",
        description="Show Duplicate Modifier button next to the modifier list",
        default=True
    )

    use_apply_buttons: bpy.props.BoolProperty(
        name="Show Apply/Apply All Buttons",
        description="Show Apply/Apply All buttons below the modifier list",
        default=False
    )

    use_modifier_search: bpy.props.BoolProperty(
        name="Use Modifier Search",
        description="On pressing the + button, show modifier search instead of menu with categories",
        default=True
    )

    default_list_height: bpy.props.IntProperty(
        name="Default List Height",
        description="Default list height in number of modifier items to display",
        default=6,
        min=6
    )

    use_show_viewport_toggle: bpy.props.BoolProperty(
        name="Show Viewport Toggle",
        description="Show the Viewport Toggle icon for each modifier in the list",
        default=True
    )

    use_show_render_toggle: bpy.props.BoolProperty(
        name="Show Render Toggle",
        description="Show the Render Toggle icon for each modifier in the list",
        default=True
    )

    use_show_in_editmode_toggle: bpy.props.BoolProperty(
        name="Show Edit Mode Toggle",
        description="Show the Edit Mode Toggle icon for each modifier in the list",
        default=False
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        header, body = layout.panel("modifier_list")
        header.label(text="Modifier List")
        
        if body:
            body.prop(self, "default_list_height")
            body.prop(self, "use_show_viewport_toggle")
            body.prop(self, "use_show_render_toggle")
            body.prop(self, "use_show_in_editmode_toggle")

        header, body = layout.panel("operators")
        header.label(text="Operators")

        if body:
            row = body.row()
            row.prop(self, "use_add_remove_buttons")

            col = row.column()
            col.enabled = self.use_add_remove_buttons
            col.prop(self, "use_modifier_search")

            body.prop(self, "use_duplicate_button")
            body.prop(self, "use_apply_buttons")


def register():
    bpy.utils.register_class(ModifierStackManagerPreferences)


def unregister():
    bpy.utils.unregister_class(ModifierStackManagerPreferences)


if __name__ == "__main__":
    register()