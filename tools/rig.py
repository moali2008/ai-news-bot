import bpy,math,mathutils,os,sys
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.abspath('in/soldier.glb'))
src=[o for o in bpy.context.scene.objects if o.type=='ARMATURE'][0];src.name='SRC'
for o in list(bpy.context.scene.objects):
    if o.type=='MESH':bpy.data.objects.remove(o,do_unlink=True)
acts=[a for a in bpy.data.actions];print('ACTIONS',[a.name for a in acts])
# mesh
obj=[f for f in os.listdir('out/0') if f.endswith('.obj')][0]
try:bpy.ops.wm.obj_import(filepath=os.path.abspath('out/0/'+obj))
except Exception:bpy.ops.import_scene.obj(filepath=os.path.abspath('out/0/'+obj))
me=[o for o in bpy.context.scene.objects if o.type=='MESH'][0];me.name='Investigator'
bpy.context.view_layer.update()
def bbox(o):
    ws=[o.matrix_world@mathutils.Vector(c) for c in o.bound_box];return [min(v[i] for v in ws) for i in range(3)],[max(v[i] for v in ws) for i in range(3)]
print('MESH BBOX',bbox(me))
# make the tallest axis Z (Blender up)
mn,mx=bbox(me);ext=[mx[i]-mn[i] for i in range(3)];up=ext.index(max(ext));print('ext',ext,'up',up)
if up==1:me.rotation_euler[0]=math.radians(90)
elif up==0:me.rotation_euler[1]=math.radians(-90)
bpy.context.view_layer.update();bpy.ops.object.select_all(action='DESELECT');me.select_set(True);bpy.context.view_layer.objects.active=me;bpy.ops.object.transform_apply(location=False,rotation=True,scale=False)
mn,mx=bbox(me);H=mx[2]-mn[2];s=1.80/H;me.scale=(s,s,s);bpy.ops.object.transform_apply(scale=True)
mn,mx=bbox(me);me.location=(-(mn[0]+mx[0])/2,-(mn[1]+mx[1])/2,-mn[2]);bpy.ops.object.transform_apply(location=True)
print('MESH FIXED',bbox(me))
# rig copy of the source skeleton, arms rotated down into an A-pose, scaled to the mesh
bpy.ops.object.select_all(action='DESELECT');src.select_set(True);bpy.context.view_layer.objects.active=src
src.animation_data and setattr(src.animation_data,'action',None)
bpy.ops.object.duplicate();rig=bpy.context.active_object;rig.name='Rig';rig.animation_data_clear()
bpy.context.view_layer.update()
smn,smx=bbox(src) if False else (None,None)
bpy.ops.object.mode_set(mode='EDIT');eb=rig.data.edit_bones
def chain(root):
    out=[root];[out.extend(chain(c)) for c in root.children];return out
hip=[b for b in eb if b.name.endswith('Hips')][0];head=[b for b in eb if b.name.endswith('HeadTop_End') or b.name.endswith('Head')][-1]
ang=float(os.environ.get('APOSE','42'))
for side,sg in (('Left',1),('Right',-1)):
    arm=[b for b in eb if b.name.endswith(side+'Arm')][0];piv=arm.head.copy()
    # rotate about the forward axis so the arm points down at `ang` degrees
    vec=(arm.tail-arm.head);axis=mathutils.Vector((0,1,0))
    cur=math.degrees(math.atan2(vec.z,abs(vec.x)));R=mathutils.Matrix.Rotation(math.radians((-ang-cur))*(1 if vec.x>0 else -1),4,axis)
    for b in chain(arm):
        b.head=piv+R@(b.head-piv);b.tail=piv+R@(b.tail-piv);b.roll=b.roll
bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.update()
# scale the rig so the head top meets the mesh top
rmn,rmx=bbox(me);
import statistics
ht=max((rig.matrix_world@b.tail_local).z for b in rig.data.bones)
k=1.80/ht;rig.scale=(rig.scale[0]*k,rig.scale[1]*k,rig.scale[2]*k);bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.transform_apply(scale=True)
# bind
bpy.ops.object.select_all(action='DESELECT');me.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.parent_set(type='ARMATURE_AUTO')
print('GROUPS',len(me.vertex_groups))
# retarget: rig bones copy world rotation of same-name source bones, hips copy location; bake each action
src.scale=(k,k,k) if False else src.scale
srck=1.0
bpy.ops.object.select_all(action='DESELECT');src.select_set(True);bpy.context.view_layer.objects.active=src;bpy.context.view_layer.update()
sh=max((src.matrix_world@b.tail_local).z for b in src.data.bones);src.scale=tuple(v*1.80/sh for v in src.scale);bpy.context.view_layer.update()
for pb in rig.pose.bones:
    if pb.name in src.pose.bones:
        c=pb.constraints.new('COPY_ROTATION');c.target=src;c.subtarget=pb.name;c.target_space='WORLD';c.owner_space='WORLD'
        if pb.name.endswith('Hips'):
            c2=pb.constraints.new('COPY_LOCATION');c2.target=src;c2.subtarget=pb.name;c2.target_space='WORLD';c2.owner_space='WORLD'
baked=[]
for a in acts:
    if a.name.lower().startswith('tpose'):continue
    src.animation_data_create();src.animation_data.action=a
    f0,f1=[int(x) for x in a.frame_range];bpy.context.scene.frame_start=f0;bpy.context.scene.frame_end=f1
    bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='POSE');bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.nla.bake(frame_start=f0,frame_end=f1,only_selected=True,visual_keying=True,clear_constraints=False,use_current_action=False,bake_types={'POSE'})
    bpy.ops.object.mode_set(mode='OBJECT');na=rig.animation_data.action;na.name=a.name;baked.append(na);print('BAKED',a.name,f0,f1)
    tr=rig.animation_data.nla_tracks.new();tr.name=a.name;tr.strips.new(a.name,f0,na);rig.animation_data.action=None
for pb in rig.pose.bones:
    for c in list(pb.constraints):pb.constraints.remove(c)
bpy.data.objects.remove(src,do_unlink=True)
for a in list(bpy.data.actions):
    if a not in baked:bpy.data.actions.remove(a)
# vertex colours -> material
mat=bpy.data.materials.new('Skin');mat.use_nodes=True;nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF');vc=nt.nodes.new('ShaderNodeVertexColor');nt.links.new(vc.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.8
me.data.materials.clear();me.data.materials.append(mat)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=os.path.abspath('char.glb'),export_format='GLB',export_animations=True,export_nla_strips=True,export_apply=False)
print('EXPORTED',os.path.getsize('char.glb'))
