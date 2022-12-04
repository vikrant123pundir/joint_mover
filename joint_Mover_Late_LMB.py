bl_info = {
    "name": "Joint_mover_Late_LMB",
    "author": "Vikrant Pundir",
    "version": (0, 1),
    "blender" : (3, 00, 0),
    "category": "Rigging"
}

import bpy


def main(context):
    global c
    c = bpy.context
    
    global rig
    rig = c.view_layer.objects.active.name
    
    global bone
    bone = c.active_bone.name
    
    global boneList
    boneList = bpy.data.armatures[rig].bones

    global act_Head
    act_Head = bpy.data.armatures[rig].bones[bone].head_local
    
    global act_Tail
    act_Tail = bpy.data.armatures[rig].bones[bone].tail_local

    
def selector(locBoneVar):
    for i in boneList:
        if locBoneVar == boneList[i.name].head_local:
            bpy.data.armatures[rig].bones[i.name].select = False
            bpy.data.armatures[rig].bones[i.name].select_head = True
            print("in head")
            
        if locBoneVar == boneList[i.name].tail_local:
            bpy.data.armatures[rig].bones[i.name].select = False
            bpy.data.armatures[rig].bones[i.name].select_tail = True
            print("in tail")
            
    print ("-----")
    
def sel_init():

    
    if boneList[bone].select_head == True:
        selector(act_Head)
        
    if boneList[bone].select_tail == True:
        selector(act_Tail)


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):
        print("hey")
        
        active_object = bpy.context.view_layer.objects.active.type
        mode = context.active_object.mode
        if (active_object == 'ARMATURE') and (mode == 'EDIT'):
        
            bpy.ops.object.mode_set(mode='OBJECT')
        
            main(context)
            sel_init()
        
            bpy.ops.object.mode_set(mode='EDIT')
        
        #invoke grab afe edit mode, else it will move the whole object
            bpy.ops.transform.translate('INVOKE_DEFAULT')
        else: bpy.ops.transform.translate('INVOKE_DEFAULT')
        return {'FINISHED'}



addon_keymaps = []
# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(SimpleOperator)
    

    # Add the hotkey
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(SimpleOperator.bl_idname, type='LEFTMOUSE', value='CLICK_DRAG')
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
