import bpy
from bpy.types import Menu


class MODIFIER_MT_dropdown_menu(Menu):
    bl_label = "Modifier Specials"
    bl_idname = "MODIFIER_MT_dropdown_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.msm_modifier_copy", text="Duplicate Modifier", icon='DUPLICATE')
        layout.operator("object.msm_modifier_apply_all", text="Apply All Modifiers", icon='CHECKMARK')

        layout.separator()

        op = layout.operator(
            "object.msm_modifier_remove",
            text="Remove All Modifiers",
            icon='TRASH'
        )

        op.all = True