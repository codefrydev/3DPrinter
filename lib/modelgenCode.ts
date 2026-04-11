export const LUNAR_SPACESUIT_CODE = `import bpy
import math

# Clear existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Create Lunar Spacesuit base structure
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=64,
    ring_count=32,
    radius=1.5,
    location=(0, 0, 1.5)
)
spacesuit = bpy.context.active_object
spacesuit.name = "Lunar_Spacesuit"

# Apply subsurface modifier for smooth rendering
bpy.ops.object.modifier_add(type='SUBSURF')
spacesuit.modifiers["Subdivision"].levels = 2

# Add composite PBR material
mat = bpy.data.materials.new(name="Space_Polymer")
mat.use_nodes = True
nodes = mat.node_tree.nodes

# Configure Material Nodes
bsdf = nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1)
bsdf.inputs['Metallic'].default_value = 0.1
bsdf.inputs['Roughness'].default_value = 0.4
bsdf.inputs['Transmission'].default_value = 0.0

spacesuit.data.materials.append(mat)
print("Model generated successfully.")
`;
