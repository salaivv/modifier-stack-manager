import bpy
from bpy.types import UIList


class MODIFIER_UL_modifier_stack(UIList):
    def draw_item(
        self, context, layout, data, item, 
        icon, active_data, active_propname, index
    ):
        md = item
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            
            row.prop(md, 'name', text="", emboss=False, icon_value=1, icon = self.get_mod_icon(md))
            row.prop(md, 'show_render', text="", emboss=False, icon_only=True)
            row.prop(md, 'show_viewport', text="", emboss=False, icon_only=True)

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='', icon_value=icon)
            
    def get_mod_icon(self, md):
        md_icon = bpy.types.Modifier.bl_rna.properties['type'].enum_items[md.type].icon
        return md_icon