import bpy
from .modifier_list import MODIFIER_UL_modifier_stack


classes = [
	MODIFIER_UL_modifier_stack,
]


def register():
	for cl in classes:
		bpy.utils.register_class(cl)


def unregister():
	for cl in reversed(classes):
		bpy.utils.unregister_class(cl)