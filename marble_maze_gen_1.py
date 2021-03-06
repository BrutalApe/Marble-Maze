import bpy, bmesh
from bpy import data as D
from bpy import context as C
from bpy import ops as O
from mathutils import Vector

# Gets object of given name
# ParamsL
#   obj_name - name of object required
# Return:
#   Object of name given
def get_object(obj_name):
    for obj in C.scene.objects:
        if obj.name == obj_name:
            return obj
    
    # If not found
    print("Object named", obj_name, "not found.")
    return 0

# Selects object of given name
# Params:
#   obj_name - name of object to be selected
# Return:
#   Object selected
def select_object(obj_name):
    obj = get_object(obj_name)
    obj.select_set(True)
    return obj

# Creates a plane using given parameters
# Params:
#   name - name of plane
#   loc_vec - location of plane
#   x,y_scl - scale of plane
# Return:
#   Created plane object 
def create_plane(name, loc_vec, x_scl, y_scl):
    print("Creating plane...")
    z_mod = (loc_vec[2] * 1.5) + 0.75
    loc_vec_modded = [loc_vec[0], loc_vec[1], z_mod]
    O.mesh.primitive_plane_add(location=loc_vec_modded)
    O.transform.resize(value=(x_scl, y_scl, 0))
    
    # Set plane's name to name
    for obj in C.selected_objects:
        if (obj.type == "MESH") and (obj.name == "Plane"):
            obj.name = name
            break

    return obj

# Creates a circle using given parameters
# Params:
#   name - name of circle
#   loc_vec - location of circle
#   x,y_scl - scale of circle
# Return:
#   Created circle object 
def create_circle(name, loc_vec, x_scl, y_scl):
    print("Creating circle...")
    z_mod = (loc_vec[2] * 1.5) + 0.75
    loc_vec_modded = [loc_vec[0], loc_vec[1], z_mod]
    O.mesh.primitive_circle_add(location=loc_vec_modded)
    O.transform.resize(value=(x_scl, y_scl, 0))
    
    # Set circle's name to name
    for obj in C.selected_objects:
        if (obj.type == "MESH") and (obj.name == "Circle"):
            obj.name = name
            break

    return obj

# Creates a camera in the scene
# Params:
#   camera_name - name of camera to be created
#   loc_vec - location of camera
# Return:
#   camera object created
def add_camera(camera_name, loc_vec):
    print("Adding camera", camera_name, "; loc =", loc_vec)
    scn = C.scene

    # create the camera
    cam = bpy.data.cameras.new(camera_name)
    cam.lens = 18

    # create the camera object
    cam_obj = bpy.data.objects.new(camera_name, cam)
    cam_obj.location = (loc_vec[0], loc_vec[1], loc_vec[2])
    scn.collection.objects.link(cam_obj)
    return cam_obj

# Points camera at specific location
# https://blender.stackexchange.com/questions/5210/pointing-the-camera-in-a-particular-direction-programmatically
# Params:
#   obj_camera - camera object to rotate
#   point - x,y,z coordinates to look at
# Return:
#   Nothing
def look_at(obj_camera, point):
    loc_camera = obj_camera.matrix_world.to_translation()

    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()

# Selects all meshes in scene
# Params:
#   Nothing
# Return:
#   Nothing
def select_all_meshes():
    for obj in C.scene.objects:
        if obj.type == "MESH":
            obj.select_set(True)

# Deelects all meshes in scene
# Params:
#   Nothing
# Return:
#   Nothing
def deselect_all_meshes():
    for obj in C.scene.objects:
        if obj.type == "MESH":
            obj.select_set(False)

# Removes all meshes in scene
# Params:
#   Nothing
# Return:
#   Nothing
def remove_all_meshes():
    select_all_meshes()
    O.object.delete()

    return

# Adds boolean operator between two meshes in a scene
# Params:
#   mesh_1 - mesh object to receive boolean modifier
#   mesh_2 - mesh object used as boolean modifier
#   bool_op - boolean operator to add
# Return:
#   Result of bool operation
def bool_meshes(mesh_1, mesh_2, bool_op):
    name_1 = mesh_1.name
    name_2 = mesh_2.name
    mod = D.objects[name_1].modifiers.new('Boolean', type='BOOLEAN')
    mod.operation = bool_op
    mod.object = D.objects[name_2]
    C.view_layer.objects.active = bpy.data.objects[name_1]
    # Apply the modifier.
    res = O.object.modifier_apply(modifier = 'Boolean')

    return res

# Unionizes 2 meshes, deletes mesh that was unioned in
# Params:
#   mesh_1 - main mesh object
#   mesh_2 - mesh object to unioned onto mesh_1
# Return:
#   Result of union
def unionize_meshes(mesh_1, mesh_2):
    select_object(mesh_1.name)
    bool_meshes(mesh_1, mesh_2, 'UNION')
    deselect_all_meshes()
    select_object(mesh_2.name)
    O.object.delete()
    return mesh_1

# Creates a marble using given parameters
# Params:
#   name - name of marble
#   loc_vec - initial location of marble
#   scl - scale of marble
# Return:
#   Created marble object 
def create_marble(name, loc_vec, scl):
    z_mod = (loc_vec[2] * 1.5) + 0.75
    loc_vec_modded = [loc_vec[0], loc_vec[1], z_mod]
    O.mesh.primitive_uv_sphere_add(location=loc_vec_modded)
    O.transform.resize(value=(scl, scl, scl))
    
    # Set plane's name to name
    for obj in C.selected_objects:
        if (obj.type == "MESH") and (obj.name == "Sphere"):
            obj.name = name
            break

    O.rigidbody.object_add(type='ACTIVE')

    return obj

# Creates cylinder at given location
# Params:
#   name - name for object
#   loc_vec - location of object
# Return:
#   created object
def create_cylinder(name, loc_vec):
    z_mod = (loc_vec[2] * 1.5) + 0.75
    loc_vec_modded = [loc_vec[0], loc_vec[1], z_mod]
    O.mesh.primitive_cylinder_add(location=loc_vec_modded)

    # Set name
    for obj in C.selected_objects:
        if (obj.type == "MESH") and (obj.name == "Cylinder"):
            obj.name = name
            break
    
    return obj

# Creates support tube as hollow cylinder at given location
# Params:
#   name - name for object
#   loc_vec - location of object
# Return:
#   created object
# https://stackoverflow.com/questions/37808840/selecting-a-face-and-extruding-a-cube-in-blender-via-python-api
# https://blender.stackexchange.com/questions/121123/using-python-and-bmesh-to-scale-resize-a-face-in-place
def create_support(name, loc_vec):

    # If an object were named the name of the mesh created, undesired behavior 
    # would occur next time that mesh was created (Mesh.001 would be made, Mesh would be modified)
    if (name == "Cylinder"):
        print("Use a different name for the object.")
        return 0

    obj = create_cylinder(name, loc_vec)

    O.transform.resize(value=(0.5, 0.5, 0.75))

    O.object.mode_set(mode = 'EDIT')
    O.mesh.select_mode(type = 'FACE')
    O.mesh.select_all(action = 'DESELECT')
    
    # Get a BMesh representation
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    # Inset faces
    for f in bm.faces:
        if ((f.index == 30) or (f.index == 33)): # Top and Bottom
            f.select = True
            O.mesh.inset(thickness=0.125) # Do it once to actually inset
            O.mesh.inset(thickness=0) # Do it 2nd time so faces can be deleted
            if (f.index == 30): # Top only 
                O.transform.translate(value=(0, 0, -1.5))
            f.select = False

    O.mesh.select_all(action = 'DESELECT')

    for f in bm.faces:
        if ((f.index == 30) or (f.index == 33)):
            f.select = True    

    O.mesh.delete(type='FACE')    
    
    O.object.mode_set(mode = 'OBJECT')
    O.rigidbody.object_add(type='PASSIVE')
    C.object.rigid_body.collision_shape = 'MESH'
    C.object.rigid_body.friction = 0.1

    deselect_all_meshes()

    return obj

# Creates beginning funnel of maze at given location
# Params:
#   name - name for object
#   loc_vec - location of object
# Return:
#   created object
def create_start_funnel(name, loc_vec):
    
    # Create support as basis of funnel shape
    funnel = create_support(name, loc_vec)

    # Scale top out to create basic funnel shape
    polygon_index_list = list(range(32, 64))
    O.object.mode_set(mode="OBJECT")
    for p_i in polygon_index_list:
        funnel.data.polygons[p_i].select = True
    O.object.mode_set(mode = 'EDIT')
    O.transform.resize(value=(1.5, 1.5, 1))
    O.object.mode_set(mode="OBJECT")

    return funnel

# Creates collector for end of maze at given location
# Params:
#   name - name for object
#   loc_vec - location of object
# Return:
#   created object
def create_end_collector(name, loc_vec):

    # Create support as basis of collector shape
    collector  = create_support(name, loc_vec)

    # will use this to cut exit hole into support for marble to roll out of
    hole_cutter = create_cylinder(name+"_hole_cutter", loc_vec)
    select_object(hole_cutter.name)
    O.transform.rotate(value=1.65, orient_axis='X', orient_type='GLOBAL')
    O.transform.resize(value=(0.375,0.375,0.375))
    O.transform.translate(value=(0,0.2,-0.15))
    deselect_all_meshes()

    select_object(hole_cutter.name)
    bool_meshes(collector, hole_cutter, 'DIFFERENCE')
    deselect_all_meshes()
    select_object(hole_cutter.name)
    O.object.delete()

    # Add small plane at an angle to make marble exit into collector base
    p0 = create_plane(name+"_p0", [a-b for a,b in zip(loc_vec, [0,0,0.2])], 0.35, 0.4)
    O.transform.rotate(value=0.5, orient_axis='X', orient_type='GLOBAL')
    O.rigidbody.object_add(type='PASSIVE')

    unionize_meshes(collector, p0)

    # Create ring around support to keep marbles inside area
    collector_bottom = create_support(name+"_bottom", loc_vec)
    select_object(collector_bottom.name)
    O.transform.resize(value=(3, 3, 0.3))
    O.transform.translate(value=(0,0,-0.525))
    deselect_all_meshes()

    unionize_meshes(collector, collector_bottom)

    # Create small ramp in collector bottom area so marbles don't bunch near entrance
    c0 = create_cylinder(name+"_c0", [a-b for a,b in zip(loc_vec, [0,0,0.425])])
    O.transform.resize(value=(1.3,1.3,0.01))
    O.transform.rotate(value=-0.08, orient_axis='X', orient_type='GLOBAL')
    O.rigidbody.object_add(type='PASSIVE')

    unionize_meshes(collector, c0)

    # Also want to add small < shape so marbles coming in don't stay stuck at entrance

    return collector

# Creates track at given location
# Params:
#   name - name for object
#   loc_vec - location of object
# Return:
#   created object
def create_track(name, loc_vec):
    track_length = 2.45
    mod_loc_vec = [a + b for a, b in zip(loc_vec, [0,0,0])]

    # Create track portion first
    track = create_support(name, mod_loc_vec)

    # Cut off top half of cylinder to create open track
    select_object(track.name)
    O.object.mode_set(mode = 'EDIT')
    O.mesh.select_mode(type = 'EDGE')
    O.mesh.select_all(action = 'SELECT')
    O.mesh.bisect(plane_co=loc_vec, plane_no=(0, 1, 0), use_fill=True, clear_inner=True, clear_outer=False, xstart=287, xend=361, ystart=219, yend=217)
    O.object.mode_set(mode = 'OBJECT')

    O.transform.rotate(value=1.65, orient_axis='X', orient_type='GLOBAL')
    O.transform.resize(value=(0.8,track_length+0.3,0.8))
    O.transform.translate(value=(0,-0.25,0))

    hole_cutter = create_cylinder(name+"_hole_cutter", mod_loc_vec)
    select_object(hole_cutter.name)
    O.transform.rotate(value=1.65, orient_axis='X', orient_type='GLOBAL')
    O.transform.resize(value=(0.375,track_length-0.6,0.375))

    # Create two end supports
    e0 = create_support(name+"_e0", [a - b for a, b in zip(loc_vec, [0,track_length-0.45,0])])
    e1 = create_support(name+"_e1", [a - b for a, b in zip(loc_vec, [0,0.45-track_length,0])])

    # "Cut" holes in supports so marble can roll into one from the top, across track, down other.
    select_object(hole_cutter.name)
    bool_meshes(e0, hole_cutter, 'DIFFERENCE')
    deselect_all_meshes()

    select_object(hole_cutter.name)
    bool_meshes(e1, hole_cutter, 'DIFFERENCE')
    deselect_all_meshes()

    select_object(hole_cutter.name)
    O.object.delete()

    # Merge end supports to track to create single track object.
    unionize_meshes(track, e0)
    unionize_meshes(track, e1)
    
    # Add small plane at an angle inside start of track to add starting momentum
    p0 = create_plane(name+"_p0", [a - b for a, b in zip(loc_vec, [0,track_length-0.45,0])], 0.35, 0.45)
    O.transform.rotate(value=0.7, orient_axis='X', orient_type='GLOBAL')
    O.rigidbody.object_add(type='PASSIVE')
    
    unionize_meshes(track, p0)
    
    return track

def main():
    print("\n\n\n\n\nGenerating Marble Maze...")

    # There are many different piece types, but will start with basics.
    # Support Tube: (Hollow Cylinder) Used as supports, also allow marble to fall through.
    # Support Base: (Cylinder with wider bottom) Always placed at bottom of support tower.
    # Track: (Two hollow cylinders, connected by u-shaped track angled down) Straight path from one tower to another
    # Start Funnel: (Hollow cylinder with wider top) starting point of maze.
    # End Collector: (Wide cylinder with circular path and support-sized entrance at top) for marbles to end in.

    # Planned order for creating:
    # Supports first
    # Bases at bottom of each support stack
    # Any connecting tracks placed at certain levels between stacks
    # Funnel at top of maze stack
    # Collector at end of maze
    
    # All pieces shoud have rigid body simulation; for now, none will be allowed to move.
    # A sphere (marble) should be able to roll down maze from start to end.

    # Set to object mode if it already isn't
    try:
        O.object.mode_set(mode='OBJECT', toggle=False)
    except:
        pass

    # Clear scene
    remove_all_meshes()

    base_size = 75

    # Details of camera to be used; placed at edge of plane, 4 times higher than biggest mountain level
    cam1_loc = [0, 0, 0]
    cam1_name = "Camera 1"

    # Delete and unlink camera 1 if it exists
    try:
        D.objects[cam1_name].select_set(True)
        O.object.delete() 
        O.outliner.id_operation(type='UNLINK')
    except:
        pass

    # Add camera 1 to scene
    # cam1 = add_camera("Camera 1", cam1_loc)

    # Create plane as base for maze
    base = create_plane("Base", [0,0,-0.5], base_size, base_size)
    O.rigidbody.object_add(type='PASSIVE')

    # Point camera at maze
    # look_at(cam1, base.matrix_world.to_translation())

    print("Creating supports...")
    s_0 = create_support("S_0", [0,0,0])

    print("Creating marble...")
    m_0 = create_marble("M_0", [0,0,3], 0.275)
    m_1 = create_marble("M_1", [0,0,4], 0.275)
    m_2 = create_marble("M_2", [0,0,5], 0.275)

    print("Creating track...")
    t_0 = create_track("T_0", [0,2,1])

    print("Creating start funnel...")
    f_0 = create_start_funnel("F_0", [0,0,2])

    print("Creating end collector...")
    c_0 = create_end_collector("E_0", [0,4,0])

    return

if __name__ == "__main__":
    main()
