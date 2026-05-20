from .modifiers import (
		ModifierMove, ModifierCopy, ModifierApply, ModifierApplyAll,
		ModifierRemove, ModifierExpandSelectedOnly, ModifierCollapseAll
	)


cls = (
	ModifierMove,
	ModifierCopy,
	ModifierApply,
	ModifierApplyAll,
	ModifierRemove,
	ModifierExpandSelectedOnly,
	ModifierCollapseAll
)


def register():
	import bpy
	for cl in cls:
		bpy.utils.register_class(cl)


def unregister():
	import bpy
	for cl in cls:
		bpy.utils.unregister_class(cl)