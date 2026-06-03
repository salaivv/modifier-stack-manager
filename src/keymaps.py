import bpy


keymaps = [
    {
        "idname": "object.msm_modifier_move",
        "type": 'UP_ARROW',
        "value": 'PRESS',
        "ctrl": True,
        "shift": True,
        "alt": False,
        "repeat": True,
        "properties": {
            "direction": 'UP'
        }
    },
    {
        "idname": "object.msm_modifier_move",
        "type": 'DOWN_ARROW',
        "value": 'PRESS',
        "ctrl": True,
        "shift": True,
        "alt": False,
        "repeat": True,
        "properties": {
            "direction": 'DOWN'
        }
    },
    {
        "idname": "object.msm_modifier_apply_all",
        "type": 'A',
        "value": 'PRESS',
        "ctrl": True,
        "shift": True,
        "alt": False,
        "repeat": False,
    },
    {
        "idname": "object.msm_modifier_remove",
        "type": 'X',
        "value": 'PRESS',
        "ctrl": True,
        "shift": True,
        "alt": False,
        "repeat": False,
        "properties": {
            "all": True
        }
    },
    {
        "idname": "object.msm_modifier_expand_selected_only",
        "type": 'E',
        "value": 'PRESS',
        "ctrl": False,
        "shift": True,
        "alt": False,
        "repeat": False,
    },
    {
        "idname": "object.msm_modifier_collapse_all",
        "type": 'C',
        "value": 'PRESS',
        "ctrl": False,
        "shift": True,
        "alt": False,
        "repeat": False,
    },
]


addon_keymaps = [ ]


def register():
    keymap_config = bpy.context.window_manager.keyconfigs.addon

    if keymap_config:
        km = keymap_config.keymaps.new(name="Property Editor", space_type='PROPERTIES')

        for keymap in keymaps:
            kmi = km.keymap_items.new(
                keymap["idname"], keymap["type"], keymap["value"],
                ctrl=keymap["ctrl"], shift=keymap["shift"], alt=keymap["alt"],
                repeat=keymap["repeat"]
            )

            if "properties" in keymap.keys():
                for property, value in keymap["properties"].items():
                    setattr(kmi.properties, property, value)

            addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()