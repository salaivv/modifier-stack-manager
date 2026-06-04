import bpy
from bpy.types import UIList

from .. import __package__ as base_package


addon_prefs = bpy.context.preferences.addons[base_package]


class MODIFIER_UL_modifier_stack(UIList):
    def draw_item(
        self, context, layout, data, item, 
        icon, active_data, active_propname, index
    ):
        modifier = item
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(modifier, "name", text="", emboss=False, icon_value=layout.icon(modifier))

            if addon_prefs.preferences.use_show_viewport_toggle:
                layout.prop(modifier, "show_viewport", text="", emboss=False, icon_only=True)

            if addon_prefs.preferences.use_show_render_toggle:
                layout.prop(modifier, "show_render", text="", emboss=False, icon_only=True)

            if addon_prefs.preferences.use_show_in_editmode_toggle:
                layout.prop(modifier, "show_in_editmode", text="", emboss=False, icon_only=True)

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='', icon_value=icon)