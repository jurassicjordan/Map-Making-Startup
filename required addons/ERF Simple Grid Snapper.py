bl_info = {
    "name": "ERF Simple Grid Snapper",
    "blender": (2, 80, 0),
    "category": "Mesh",
}

import bpy
import bmesh

class SimpleGridSnapperPanel(bpy.types.Panel):
    bl_label = "Simple Grid Snapper"
    bl_idname = "PT_SimpleGridSnapper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ERF Tools'
    bl_context = 'mesh_edit'

    def draw(self, context):
        layout = self.layout

        # Add properties for grid size in X, Y, and Z
        layout.prop(context.scene, "grid_size_x", text="Grid Size X")
        layout.prop(context.scene, "grid_size_y", text="Grid Size Y")
        layout.prop(context.scene, "grid_size_z", text="Grid Size Z")

        # Add an execute button
        layout.operator("mesh.simple_grid_snapper", text="Snap to Grid")

        # Add a toggle button for continuous snapping
        layout.operator("mesh.toggle_continuous_snap", text="Toggle Continuous Snap")

        # Display the status of continuous snapping
        layout.label(text=f"Continuous Snap: {'ON' if context.scene.continuous_snap else 'OFF'}")

class SimpleGridSnapperOperator(bpy.types.Operator):
    bl_idname = "mesh.simple_grid_snapper"
    bl_label = "Snap to Grid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Check if we are in Edit Mode
        if bpy.context.mode != 'EDIT_MESH':
            bpy.ops.object.mode_set(mode='EDIT')

        # Get the active object and its mesh data
        obj = bpy.context.active_object
        mesh = obj.data

        # Create a BMesh from the mesh data
        bm = bmesh.from_edit_mesh(mesh)

        # Get selected vertices
        selected_verts = [v for v in bm.verts if v.select]

        # Check if there are selected vertices
        if not selected_verts:
            self.report({'INFO'}, "No vertices selected.")
            return {'CANCELLED'}

        # Snap selected vertices to the specified grid size in X, Y, and Z
        grid_size_x = context.scene.grid_size_x
        grid_size_y = context.scene.grid_size_y
        grid_size_z = context.scene.grid_size_z
        snap_to_grid(selected_verts, grid_size_x, grid_size_y, grid_size_z)

        # Update the mesh with the modified BMesh
        bmesh.update_edit_mesh(mesh)

        self.report({'INFO'}, f"Snapped to grid: X={grid_size_x}, Y={grid_size_y}, Z={grid_size_z}")
        return {'FINISHED'}

class ToggleContinuousSnapOperator(bpy.types.Operator):
    bl_idname = "mesh.toggle_continuous_snap"
    bl_label = "Toggle Continuous Snap"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        context.scene.continuous_snap = not context.scene.continuous_snap

        if context.scene.continuous_snap:
            self.report({'INFO'}, "Continuous snapping ON.")
        else:
            self.report({'INFO'}, "Continuous snapping OFF.")

        return {'FINISHED'}

def snap_to_grid(selected_verts, grid_size_x, grid_size_y, grid_size_z):
    for v in selected_verts:
        v.co.x = round(v.co.x / grid_size_x) * grid_size_x
        v.co.y = round(v.co.y / grid_size_y) * grid_size_y
        v.co.z = round(v.co.z / grid_size_z) * grid_size_z

def continuous_snap_handler(scene):
    if bpy.context.mode == 'EDIT_MESH' and bpy.context.scene.continuous_snap:
        # Get the active object and its mesh data
        obj = bpy.context.active_object
        mesh = obj.data

        # Create a BMesh from the mesh data
        bm = bmesh.from_edit_mesh(mesh)

        # Get selected vertices
        selected_verts = [v for v in bm.verts if v.select]

        # Check if there are selected vertices
        if selected_verts:
            # Snap selected vertices to the specified grid size in X, Y, and Z
            grid_size_x = bpy.context.scene.grid_size_x
            grid_size_y = bpy.context.scene.grid_size_y
            grid_size_z = bpy.context.scene.grid_size_z
            snap_to_grid(selected_verts, grid_size_x, grid_size_y, grid_size_z)

            # Update the mesh with the modified BMesh
            bmesh.update_edit_mesh(mesh)

def register():
    bpy.utils.register_class(SimpleGridSnapperPanel)
    bpy.utils.register_class(SimpleGridSnapperOperator)
    bpy.utils.register_class(ToggleContinuousSnapOperator)
    bpy.types.Scene.grid_size_x = bpy.props.FloatProperty(name="Grid Size X", default=0.01, min=0.001, precision=3)
    bpy.types.Scene.grid_size_y = bpy.props.FloatProperty(name="Grid Size Y", default=0.01, min=0.001, precision=3)
    bpy.types.Scene.grid_size_z = bpy.props.FloatProperty(name="Grid Size Z", default=0.01, min=0.001, precision=3)
    bpy.types.Scene.continuous_snap = bpy.props.BoolProperty(name="Continuous Snap", default=False)
    bpy.app.handlers.depsgraph_update_post.append(continuous_snap_handler)

def unregister():
    bpy.utils.unregister_class(SimpleGridSnapperPanel)
    bpy.utils.unregister_class(SimpleGridSnapperOperator)
    bpy.utils.unregister_class(ToggleContinuousSnapOperator)
    del bpy.types.Scene.grid_size_x
    del bpy.types.Scene.grid_size_y
    del bpy.types.Scene.grid_size_z
    del bpy.types.Scene.continuous_snap
    bpy.app.handlers.depsgraph_update_post.remove(continuous_snap_handler)

if __name__ == "__main__":
    register()
