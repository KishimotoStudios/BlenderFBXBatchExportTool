#
# Static FBX Batch Export
# (c) 2015-2017, Kishimoto Studios
#
# 1. Run this Python script inside Blender (open it in "Text Editor" then click the "Run script" button).
# 2. Select all static objects you want to export.
# 3. File | Export | KishiTech - Static FBX Batch Export.
# 4. Set a directory to copy *.fbx files or leave the field empty to skip the copy step.
# 5. Done! *.fbx files will be saved in the same directory of your .blend file, using each object's name.
#    (and will be copied to the directory you defined in step 4, if not empty).
#
# You can change the bpy.ops.export_scene.fbx() parameters (see call below) to add animation support and so on.
#

#
# Blender 2.78a to Unity 5.5.1f export process:
# 1. The object must be rotated X=90.
# 2. If you already created your model, enter Edit Mode and rotate everything X=-90 (so your model looks correct).
#


bl_info = {
	"name": "KishiTech - Static FBX Batch Export",
	"author": "Andre Kishimoto // Kishimoto Studios",
	"version": (0, 2),
	"blender": (2, 7, 8),
	"location": "Info > File",
	"description": "Export all selected [static] mesh objects to their own [object name].FBX file.",
	"category": "Import-Export"
}

import bpy
import os
import shutil

global_name = "KishiTech - Static FBX Batch Export"

class StaticFBXBatchExport(bpy.types.Operator):
	bl_idname = "export_scene.kishitech_static_fbx_batch_export"
	bl_label = global_name
	
	dest_folder = bpy.props.StringProperty(name="Copy *.fbx to this directory (leave blank to skip the copy step):", default="c:\\tmp")
	
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self, 1000)
	
	def execute(self, context):
		basedir = os.path.dirname(bpy.data.filepath)
		if not basedir:
			raise Exception("!!! ERROR: Please save the .blend file before batch exporting. !!!")
			
		objects = []
		selection = bpy.context.selected_objects
		
		if len(selection) == 0:
			self.report({"ERROR"}, "There are 0 objects selected - nothing exported.")
			return {"FINISHED"}		
		
		bpy.ops.object.select_all(action = "DESELECT")
		
		for object in selection:
			objects.append(object)
			print(object)

		bpy.ops.object.select_all(action = "DESELECT")
			
		for object in objects:
			object_name = object.name
			object.select = True
			final_name = bpy.path.clean_name(object_name)
			filename = os.path.join(basedir, final_name)
			bpy.ops.export_scene.fbx(
				filepath = filename + ".fbx",
				check_existing = True,
				axis_forward = "-Z",
				axis_up = "Y",
				filter_glob = "*.fbx",
				version = "BIN7400",
				use_selection = True,
				global_scale = 1.0,
				apply_unit_scale = False,
				bake_space_transform = False,
				object_types = { "MESH" },
				use_mesh_modifiers = True,
				mesh_smooth_type = "OFF",
				use_mesh_edges = False,
				use_tspace = True,
				use_custom_props = False,
				add_leaf_bones = False,
				primary_bone_axis = "Y",
				secondary_bone_axis = "X",
				use_armature_deform_only = False,
				bake_anim = False,
				bake_anim_use_all_bones = False,
				bake_anim_use_nla_strips = False,
				bake_anim_use_all_actions = False,
				bake_anim_step = 1.0,
				bake_anim_simplify_factor = 1.0,
				use_anim = False,
				use_anim_action_all = False,
				use_default_take = True,
				use_anim_optimize = True,
				anim_optimize_precision = 6.0,
				path_mode = "AUTO",
				embed_textures = False,
				batch_mode = "OFF",
				use_batch_own_dir = True,
				use_metadata = True)
			object.select = False
			
			if self.dest_folder != "":
				if os.path.isdir(self.dest_folder):
					shutil.copy2(filename + ".fbx", self.dest_folder)
				else:
					self.report({"ERROR"}, self.dest_folder + " does not exist! Object [" + object.name + "] exported but not copied to destination directory.")
			
		for object in selection:
			object.select = True
			
		self.report({"INFO"}, global_name + ": All done!")

		return {"FINISHED"}

def StaticFBXBatchExportUI(self, context):
	self.layout.operator(StaticFBXBatchExport.bl_idname, text = global_name, icon = "EXPORT")
	
def register():
	bpy.utils.register_class(StaticFBXBatchExport)
	bpy.types.INFO_MT_file_export.append(StaticFBXBatchExportUI)

def unregister():
	bpy.utils.unregister_class(StaticFBXBatchExport)
	bpy.types.INFO_MT_file_export.remove(StaticFBXBatchExportUI)
	 
if __name__ == "__main__":
	register()
