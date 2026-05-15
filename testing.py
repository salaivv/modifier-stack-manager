import os
import bpy
import subprocess


this_dir = os.path.dirname(bpy.data.filepath)
build_script = os.path.join(this_dir, "build.sh")
extension = os.path.join(this_dir, "modifier_stack_manager.zip")

subprocess.run([build_script, "bd"])

bpy.ops.extensions.package_uninstall(
    repo_index=1, 
    pkg_id="modifier_stack_manager"
)

bpy.ops.extensions.package_install_files(
    filepath=extension,
    repo="user_default"
)