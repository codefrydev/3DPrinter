import bpy
import math

def clear_scene():
    """Clears all existing objects in the scene to start fresh."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_materials():
    """Creates the materials used for the key holder."""
    # 1. Dark Navy/Slate Blue Paint
    mat_base = bpy.data.materials.new(name="DarkBase_Mat")
    mat_base.use_nodes = True
    bsdf_base = mat_base.node_tree.nodes["Principled BSDF"]
    bsdf_base.inputs["Base Color"].default_value = (0.015, 0.03, 0.05, 1.0)
    bsdf_base.inputs["Roughness"].default_value = 0.8
    
    # 2. Wooden Accent / Orange
    mat_wood = bpy.data.materials.new(name="WoodAccent_Mat")
    mat_wood.use_nodes = True
    bsdf_wood = mat_wood.node_tree.nodes["Principled BSDF"]
    bsdf_wood.inputs["Base Color"].default_value = (0.55, 0.28, 0.05, 1.0)
    bsdf_wood.inputs["Roughness"].default_value = 0.6
    
    # 3. Metal (for hooks)
    mat_metal = bpy.data.materials.new(name="MetalHook_Mat")
    mat_metal.use_nodes = True
    bsdf_metal = mat_metal.node_tree.nodes["Principled BSDF"]
    bsdf_metal.inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1.0)
    bsdf_metal.inputs["Metallic"].default_value = 1.0
    bsdf_metal.inputs["Roughness"].default_value = 0.25

    return mat_base, mat_wood, mat_metal

def create_pill_shape(name, loc, width, height, depth, mat):
    """Generates a rounded rectangle (pill shape) out of a cube and two cylinders."""
    core_width = width - height
    
    # Main center rectangular body
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.dimensions = (core_width, depth, height)
    obj.data.materials.append(mat)

    # Left semi-circle cap
    bpy.ops.mesh.primitive_cylinder_add(radius=height/2, depth=depth, location=(loc[0] - core_width/2, loc[1], loc[2]))
    cap1 = bpy.context.active_object
    cap1.name = name + "_LeftCap"
    cap1.rotation_euler = (math.radians(90), 0, 0)
    cap1.data.materials.append(mat)

    # Right semi-circle cap
    bpy.ops.mesh.primitive_cylinder_add(radius=height/2, depth=depth, location=(loc[0] + core_width/2, loc[1], loc[2]))
    cap2 = bpy.context.active_object
    cap2.name = name + "_RightCap"
    cap2.rotation_euler = (math.radians(90), 0, 0)
    cap2.data.materials.append(mat)

def create_hook(name, loc, mat):
    """Creates a realistic metal J-hook using a 3D Bezier curve."""
    curve_data = bpy.data.curves.new(name, type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = 0.035
    curve_data.bevel_resolution = 6
    curve_data.use_fill_caps = True

    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(3) # 4 points total for the J shape
    pts = spline.bezier_points

    # P0: Attachment to the board
    pts[0].co = loc
    pts[0].handle_left = (loc[0], loc[1] + 0.1, loc[2])
    pts[0].handle_right = (loc[0], loc[1] - 0.2, loc[2])

    # P1: Bottom curve of the J
    pts[1].co = (loc[0], loc[1] - 0.25, loc[2] - 0.4)
    pts[1].handle_left = (loc[0], loc[1] - 0.15, loc[2] - 0.4)
    pts[1].handle_right = (loc[0], loc[1] - 0.35, loc[2] - 0.4)

    # P2: Front lip ascending
    pts[2].co = (loc[0], loc[1] - 0.4, loc[2] - 0.2)
    pts[2].handle_left = (loc[0], loc[1] - 0.4, loc[2] - 0.3)
    pts[2].handle_right = (loc[0], loc[1] - 0.4, loc[2] - 0.1)

    # P3: Hook tip
    pts[3].co = (loc[0], loc[1] - 0.3, loc[2] - 0.1)
    pts[3].handle_left = (loc[0], loc[1] - 0.35, loc[2] - 0.1)
    pts[3].handle_right = (loc[0], loc[1] - 0.25, loc[2] - 0.1)

    hook_obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(hook_obj)
    hook_obj.data.materials.append(mat)

    # Base knob (where it connects to wood)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.06, location=(loc[0], loc[1] - 0.02, loc[2]))
    knob = bpy.context.active_object
    knob.rotation_euler = (math.radians(90), 0, 0)
    knob.data.materials.append(mat)
    
    # Tip sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.038, location=(loc[0], loc[1] - 0.3, loc[2] - 0.1))
    tip = bpy.context.active_object
    tip.data.materials.append(mat)

def create_roof(name, loc, width, depth, height, mat):
    """Creates a triangular prism for the house roof."""
    verts = [
        (-width/2, -depth/2, 0), (width/2, -depth/2, 0), (0, -depth/2, height),
        (-width/2, depth/2, 0), (width/2, depth/2, 0), (0, depth/2, height)
    ]
    faces = [(0,1,2), (3,5,4), (0,3,4,1), (1,4,5,2), (2,5,3,0)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.data.materials.append(mat)
    return obj

def create_roof_trim(loc, width, height, thickness, mat):
    """Creates the wooden V-shaped trim on the front of the roof."""
    angle = math.atan2(height, width/2)
    slope_len = math.sqrt((width/2)**2 + height**2)

    # Left slope
    bpy.ops.mesh.primitive_cube_add(location=(loc[0] - width/4, loc[1], loc[2] + height/2))
    left = bpy.context.active_object
    left.dimensions = (slope_len, thickness, 0.08)
    left.rotation_euler = (0, -angle, 0)
    left.data.materials.append(mat)

    # Right slope
    bpy.ops.mesh.primitive_cube_add(location=(loc[0] + width/4, loc[1], loc[2] + height/2))
    right = bpy.context.active_object
    right.dimensions = (slope_len, thickness, 0.08)
    right.rotation_euler = (0, angle, 0)
    right.data.materials.append(mat)

def create_arched_window(loc, mat_wood, mat_base):
    """Builds the window using distinct parts (base, frame, mullions) without boolean glitches."""
    # Dark glass background
    bpy.ops.mesh.primitive_cube_add(location=(loc[0], loc[1], loc[2] + 0.4))
    glass = bpy.context.active_object
    glass.dimensions = (0.8, 0.02, 0.8)
    glass.data.materials.append(mat_base)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.02, location=(loc[0], loc[1], loc[2] + 0.8))
    glass_arch = bpy.context.active_object
    glass_arch.rotation_euler = (math.radians(90), 0, 0)
    glass_arch.data.materials.append(mat_base)

    # Wooden Grid Frame Elements
    f_parts = [
        # loc_offset, dimensions
        (( -0.35, -0.02, 0.4 ), (0.1, 0.04, 0.8)), # Left edge
        ((  0.35, -0.02, 0.4 ), (0.1, 0.04, 0.8)), # Right edge
        ((  0.0,  -0.02, 0.0 ), (0.8, 0.04, 0.1)), # Bottom edge
        ((  0.0,  -0.02, 0.5 ), (0.8, 0.04, 0.08)),# Middle horizontal
        ((  0.0,  -0.02, 0.4 ), (0.08, 0.04, 0.8)),# Middle vertical (lower half)
        ((  0.0,  -0.02, 0.95), (0.08, 0.04, 0.3)),# Middle vertical (arch section)
    ]
    for offset, dim in f_parts:
        bpy.ops.mesh.primitive_cube_add(location=(loc[0]+offset[0], loc[1]+offset[1], loc[2]+offset[2]))
        part = bpy.context.active_object
        part.dimensions = dim
        part.data.materials.append(mat_wood)

    # Wooden Arch Torus Top
    bpy.ops.mesh.primitive_torus_add(major_radius=0.35, minor_radius=0.05, location=(loc[0], loc[1] - 0.02, loc[2] + 0.8))
    f_arch = bpy.context.active_object
    f_arch.rotation_euler = (math.radians(90), 0, 0)
    f_arch.data.materials.append(mat_wood)

    # Extruding Bottom Sill
    bpy.ops.mesh.primitive_cube_add(location=(loc[0], loc[1] - 0.04, loc[2] - 0.05))
    sill = bpy.context.active_object
    sill.dimensions = (1.0, 0.1, 0.06)
    sill.data.materials.append(mat_wood)

def create_tree(loc, mat):
    """Creates a stylized silhouette tree out of overlapping cylinders."""
    # Trunk
    bpy.ops.mesh.primitive_cube_add(location=(loc[0], loc[1], loc[2] + 0.8))
    trunk = bpy.context.active_object
    trunk.dimensions = (0.3, 0.15, 1.6)
    trunk.data.materials.append(mat)

    # Leaf canopy clusters relative to trunk base
    centers = [
        (0, 0, 1.6), (-0.6, 0, 1.3), (0.6, 0, 1.3),
        (-0.8, 0, 1.8), (0.8, 0, 1.8), (-0.4, 0, 2.2),
        (0.4, 0, 2.2), (0, 0, 2.5)
    ]
    for cx, cy, cz in centers:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=0.15, location=(loc[0]+cx, loc[1]+cy, loc[2]+cz))
        leaf = bpy.context.active_object
        leaf.rotation_euler = (math.radians(90), 0, 0)
        leaf.data.materials.append(mat)

def create_text(loc, mat):
    """Adds the extruded 'Sweet Home' 3D text."""
    # Top Text: "Sweet"
    bpy.ops.object.text_add(location=(loc[0] + 0.3, loc[1] + 0.05, loc[2] + 0.7))
    t1 = bpy.context.active_object
    t1.data.body = "Sweet"
    t1.data.extrude = 0.06
    t1.data.bevel_depth = 0.005 # Adds subtle rounded edge
    t1.data.size = 0.8
    t1.rotation_euler = (math.radians(90), 0, 0)
    t1.data.materials.append(mat)

    # Bottom Text: "Home"
    bpy.ops.object.text_add(location=(loc[0] - 0.4, loc[1], loc[2]))
    t2 = bpy.context.active_object
    t2.data.body = "Home"
    t2.data.extrude = 0.06
    t2.data.bevel_depth = 0.005
    t2.data.size = 1.1
    t2.rotation_euler = (math.radians(90), 0, 0)
    t2.data.materials.append(mat)

def main():
    # 1. Base initialization
    mat_base, mat_wood, mat_metal = create_materials()

    # 2. Main Base Board (Dark Blue)
    create_pill_shape('BaseBoard', (0, 0, -1.5), width=6.5, height=1.8, depth=0.2, mat=mat_base)

    # 3. Shelf
    bpy.ops.mesh.primitive_cube_add(location=(0, -0.3, -0.525))
    shelf = bpy.context.active_object
    shelf.dimensions = (6.8, 1.0, 0.15)
    shelf.data.materials.append(mat_base)

    # 4. Wood Hook Panel
    create_pill_shape('WoodPanel', (0, -0.15, -1.5), width=5.5, height=0.8, depth=0.1, mat=mat_wood)

    # 5. Hooks (x6)
    hook_x_positions = [-2.0, -1.2, -0.4, 0.4, 1.2, 2.0]
    for x in hook_x_positions:
        create_hook(f'Hook_{x}', (x, -0.2, -1.5), mat_metal)

    # 6. House Structure (Left)
    house_loc = (-2.0, 0.05, 0.35)
    bpy.ops.mesh.primitive_cube_add(location=house_loc)
    house_base = bpy.context.active_object
    house_base.dimensions = (1.8, 0.15, 1.6)
    house_base.data.materials.append(mat_base)
    
    # Roof
    create_roof('Roof', (-2.0, 0.05, 1.15), width=2.4, depth=0.15, height=1.0, mat=mat_base)
    create_roof_trim((-2.0, -0.04, 1.15), width=2.4, height=1.0, thickness=0.04, mat=mat_wood)
    
    # Window
    create_arched_window((-2.0, -0.06, 0.0), mat_wood, mat_base)

    # 7. Tree Structure (Middle)
    create_tree((0.2, 0.05, -0.45), mat_base)

    # 8. Text Elements (Right)
    create_text((1.2, -0.05, -0.45), mat_wood)

    # 9. Mounting Screws on the Base Board
    for x in [-2.8, 2.8]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.25, location=(x, -0.05, -0.8))
        screw = bpy.context.active_object
        screw.rotation_euler = (math.radians(90), 0, 0)
        screw.data.materials.append(mat_metal)

    # 10. Parent all to a Master Empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    rig = bpy.context.active_object
    rig.name = "KeyHolder_Rig"
    for obj in bpy.data.objects:
        if obj != rig and obj.parent is None and obj.type in ['MESH', 'CURVE', 'FONT']:
            obj.parent = rig

def setup_lighting_and_camera():
    """Sets up standard studio lighting to nicely visualize the mesh."""
    bpy.ops.object.camera_add(location=(0, -8, 0), rotation=(math.radians(90), 0, 0))
    cam = bpy.context.active_object
    bpy.context.scene.camera = cam

    # Main Soft Light
    bpy.ops.object.light_add(type='AREA', location=(4, -5, 4), rotation=(math.radians(45), 0, math.radians(45)))
    light1 = bpy.context.active_object
    light1.data.energy = 500
    light1.data.size = 5.0

    # Fill Light
    bpy.ops.object.light_add(type='AREA', location=(-4, -3, 0), rotation=(math.radians(90), 0, math.radians(-45)))
    light2 = bpy.context.active_object
    light2.data.energy = 150
    light2.data.size = 5.0

    # Smooth shaded backdrop wall
    bpy.ops.mesh.primitive_plane_add(size=25, location=(0, 0.2, 0))
    wall = bpy.context.active_object
    wall.rotation_euler = (math.radians(90), 0, 0)
    wall_mat = bpy.data.materials.new(name="Wall_Mat")
    wall_mat.use_nodes = True
    wall_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.9, 0.85, 0.75, 1)
    wall.data.materials.append(wall_mat)

if __name__ == "__main__":
    clear_scene()
    main()
    setup_lighting_and_camera()
    print("Key Holder Generation Complete!")