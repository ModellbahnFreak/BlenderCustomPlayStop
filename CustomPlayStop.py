# scene_blend_info.py Copyright (C) 2020, ModellbahnFreak



bl_info = {
    "name": "Play/Stop Spacebar",
    "author": "ModellbahnFreak",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "3DView -> Side Panel -> Misc -> Playback",
    "description": "Changes playback behaviour of the spacebar to match other video software (play/stop instead of play/pause).\nAlso adds a Play/Stop button in the 3D views right panel",
    "warning": "",
    "doc_url": "https://github.com/ModellbahnFreak/BlenderCustomPlayStop/blob/master/README.md",
    "category": "Animation",
}

import bpy

print("Creating play button")

class PlayButton(bpy.types.Operator):
    bl_idname = "wm.play_custom"
    bl_label = "Play/Stop"
    bl_options = {'REGISTER'}

    @classmethod # Will never run when poll returns false
    def poll(cls, context):
        return (context.object is not None)

    def execute(self, context):
        if bpy.context.screen.is_animation_playing:
            bpy.ops.screen.animation_cancel()
            self.bl_label = "Play"
        else:
            bpy.ops.screen.animation_play()
            self.bl_label = "Stop"
        return {'FINISHED'}

class PlaybackPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_playback_controls"
    bl_label = "Playback"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
        
    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw_header(self, context):
        layout = self.layout
        #layout.label(text="My Select Panel")

    def draw(self, context):
        layout = self.layout

        box = layout
        box.operator("wm.play_custom")
        
def unregisterKeybinding():
    from bpy import context as ctx
    items = ctx.window_manager.keyconfigs.active.keymaps['Frames'].keymap_items
    for item in items:
        if item.idname=='screen.animation_play' and not item.any and not item.any and not item.ctrl and not item.alt and not item.oskey and item.type=='SPACE':
            item.active = True
        
    items = ctx.window_manager.keyconfigs.active.keymaps['Window'].keymap_items
    for item in items:
        if item.idname=='wm.play_custom' and not item.any and not item.any and not item.ctrl and not item.alt and not item.oskey and item.type=='SPACE':
            ctx.window_manager.keyconfigs.active.keymaps['Window'].keymap_items.remove(item.id)
        
def unregister():
    import bpy as bpy_active
    PanelClass = bpy_active.types.Panel.bl_rna_get_subclass_py('OBJECT_PT_playback_controls')
    if PanelClass:
        bpy_active.utils.unregister_class(PanelClass)
    OperatorClass = bpy_active.types.Panel.bl_rna_get_subclass_py('wm.play_custom')
    if OperatorClass:
        bpy_active.utils.unregister_class(OperatorClass)
    unregisterKeybinding()
        
def register():
    import bpy as bpy_active
    unregister()
    bpy_active.utils.register_class(PlaybackPanel)
    bpy_active.utils.register_class(PlayButton)
    registerKeybinding()
        
def registerKeybinding():
    from bpy import context as ctx
    items = ctx.window_manager.keyconfigs.active.keymaps['Frames'].keymap_items
    for item in items:
        if item.idname=='screen.animation_play' and not item.any and not item.any and not item.ctrl and not item.alt and not item.oskey and item.type=='SPACE':
            item.active = False
            print("Disabled other keybinding")
        
    found = False
    items = ctx.window_manager.keyconfigs.active.keymaps['Window'].keymap_items
    for item in items:
        if item.idname=='wm.play_custom' and not item.any and not item.any and not item.ctrl and not item.alt and not item.oskey and item.type=='SPACE':
            found = True
            item.active = True
            print("Found keybinding")

    if not found:
        ctx.window_manager.keyconfigs.active.keymaps['Window'].keymap_items.new('wm.play_custom',value='PRESS',type='SPACE',ctrl=False,alt=False,shift=False,oskey=False)
        print("Created keybinding")
    
    
if __name__ == "__main__":
    register()