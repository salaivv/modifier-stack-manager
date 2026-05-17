import bpy
from .modifier_list import MODIFIER_UL_modifier_stack
from .menus import MODIFIER_MT_dropdown_menu


classes = [
	MODIFIER_UL_modifier_stack,
	MODIFIER_MT_dropdown_menu
]


def register():
	for cl in classes:
		bpy.utils.register_class(cl)


def unregister():
	for cl in reversed(classes):
		bpy.utils.unregister_class(cl)