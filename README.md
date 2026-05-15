# Modifier Stack Manager

![Screenshot](screenshot.jpg)

A modifier stack manager for Blender.

This addon implements a UI List for the modifier stack similar to the ones used to manage Materials, UV Maps, Vertex Groups, etc.

The addon enables you to do the following actions directly from the list:

  - Add/Remove Modifiers
  - Duplicate Modifiers
  - Rearrange Modifiers
  - Rename Modifiers
  - Toggle Render/Viewport Visibility
  - Apply/Apply All Modifiers
  - Expand selected modifier only and collapse the rest

## Development

1. Clone this repository.
2. Create a new blend file named `testing.blend` in the repo's root directory.
3. Copy the code in `testing.py` to the Text Editor in `testing.blend`.
4. As you make changes to the code, press the _Run Script_ ▶️ button in the Text Editor to build and reinstall the addon.

_NOTE: If you have the addon previously installed from the [Extensions Platform](https://extensions.blender.org/add-ons/modifer-stack-manager/), temporarily disable/uninstall it during development. Otherwise, you'll see two modifier stacks in the modifier panel._