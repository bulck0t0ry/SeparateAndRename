import bpy

bl_info = {
    "name": "Separate and Rename",
    "author": "bulk0vich",
    "version": (1, 0, 2),
    "blender": (3, 0, 0 ),
    "location": "Edit mode / Ctrl+U",
    "description": "Separate selected vertex in edit mode and rename result object in one(two?) click!",
    "category": "Mesh"
}

class SeparateAndRename(bpy.types.Operator):
    bl_idname = "mesh.separate_and_rename"
    bl_label = "Separate selected and rename it"

    re_name: bpy.props.StringProperty(name = "Name")
    
    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return context.mode == 'EDIT_MESH'
    
    
    def execute(self, context):
        bpy.ops.mesh.separate( type = 'SELECTED' )
        bpy.ops.object.mode_set( mode = 'OBJECT' )
        v = bpy.context.selected_objects[0]
        o = bpy.context.selected_objects[1]
        o.name = self.re_name
        o.data.name = self.re_name
        o.select_set(False)
        bpy.ops.object.mode_set( mode = 'EDIT' )
        return {'FINISHED'}

    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Rename separate object to:")
        row = col.row()
        row.activate_init = True
        row.prop(self, "re_name")


addon_keymaps = []


def register():
    bpy.utils.register_class(SeparateAndRename)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new(SeparateAndRename.bl_idname, 'U', 'PRESS', ctrl=True, shift=False)
    addon_keymaps.append((km, kmi))
    
    
def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(SeparateAndRename)

    
if __name__ == "__main__":
    register()
