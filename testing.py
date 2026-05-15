import os
import bpy
import subprocess


blender_path = bpy.app.binary_path

this_dir = os.path.dirname(bpy.data.filepath)
source_dir = os.path.join(this_dir, "src")
extension = os.path.join(this_dir, "modifier_stack_manager.zip")

subprocess.run([
    blender_path,
    "--command",
    "extension",
    "build",
    "--source-dir",
    source_dir,
    "--output-filepath",
    extension
])

bpy.ops.extensions.package_uninstall(
    repo_index=1, 
    pkg_id="modifier_stack_manager"
)

bpy.ops.extensions.package_install_files(
    filepath=extension,
    repo="user_default"
)