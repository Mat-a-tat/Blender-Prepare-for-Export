import bpy

class ResetTransformsOperator(bpy.types.Operator):
    bl_idname = "object.reset_transforms"
    bl_label = "Reset Transforms"

    def execute(self, context):
        for obj in context.selected_objects:
            # Scale object origin
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            bpy.ops.transform.resize(value=(1, 1, 1))
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')

            # Reset rotation and location
            obj.rotation_euler = (0, 0, 0)
            obj.location = (0, 0, 0)

            # Reset origin point to world axis
            # This line has some funky nonsense that requires further testing. 
            obj.data.transform(obj.matrix_world)
            obj.matrix_world.identity()
            obj.data.update()
            
            # Set origin point to geometry
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            
            # Recaulcuate normals
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}

class ResetTransformsPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_reset_transforms"
    bl_label = "Reset Transforms"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.reset_transforms")

def register():
    bpy.utils.register_class(ResetTransformsOperator)
    bpy.utils.register_class(ResetTransformsPanel)

def unregister():
    bpy.utils.unregister_class(ResetTransformsOperator)
    bpy.utils.unregister_class(ResetTransformsPanel)

if __name__ == "__main__":
    register()