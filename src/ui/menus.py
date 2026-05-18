import bpy
from bpy.types import Menu


class MODIFIER_MT_dropdown_menu(Menu):
    bl_label = "Modifier Specials"
    bl_idname = "MODIFIER_MT_dropdown_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.msm_modifier_apply", icon='CHECKMARK')
        layout.operator("object.msm_modifier_apply_all")

        layout.separator()

        layout.operator("object.msm_modifier_expand_selected_only")
        layout.operator("object.msm_modifier_collapse_all")

        layout.separator()

        layout.operator("object.msm_modifier_copy", text="Duplicate Modifier", icon='DUPLICATE')

        layout.separator()

        op = layout.operator("object.msm_modifier_remove", text="Remove All Modifiers", icon='TRASH')
        op.all = True