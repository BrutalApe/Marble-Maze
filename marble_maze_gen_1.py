import bpy
from bpy import data as D
from bpy import context as C
from bpy import ops as O

# Creates a plane using given parameters
# Params:
#   name - name of plane
#   x,y,z_loc - location of plane
#   x,y_scl - scale of plane
# Return:
#   Created plane object 
def create_plane(name, x_loc, y_loc, z_loc, x_scl, y_scl):
    print("Creating plane...")
    O.mesh.primitive_plane_add(location=(x_loc,y_loc,z_loc))
    O.transform.resize(value=(x_scl, y_scl, 0))
    
    # Set plane's name to name
    for obj in C.selected_objects:
        if (obj.type == "MESH") and (obj.name == "Plane"):
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

# Removes all meshes in scene
# Params:
#   Nothing
# Return:
#   Nothing
def remove_all_meshes():
    select_all_meshes()
    O.object.delete()

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
    cam1 = add_camera("Camera 1", cam1_loc)

    # Create plane as base for maze
    base = create_plane("Base", 0, 0, 0, base_size, base_size)

    # Point camera at maze
    look_at(cam1, base.matrix_world.to_translation())

if __name__ == "__main__":
    main()