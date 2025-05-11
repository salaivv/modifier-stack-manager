from .modifier_list import MODIFIER_UL_modifier_stack


def register():
	import bpy
	bpy.utils.register_class(MODIFIER_UL_modifier_stack)


def unregister():
	import bpy
	bpy.utils.unregister_class(MODIFIER_UL_modifier_stack)


if __name__ == "__main__":
    register()