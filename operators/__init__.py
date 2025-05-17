from .modifiers import *


cls = (
	ModifierMove,
	ModifierCopy,
	ModifierApplyRemove,
	ModifierApplyAll,
	ModifierExpandCollapse
)


def register():
	import bpy
	for cl in cls:
		bpy.utils.register_class(cl)


def unregister():
	import bpy
	for cl in cls:
		bpy.utils.unregister_class(cl)


if __name__ == "__main__":
    register()