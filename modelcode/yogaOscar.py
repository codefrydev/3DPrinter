bl_info = {
    "name": "Stylized Trophy Generator",
    "author": "Gemini",
    "version": (2, 0),
    "blender": (3, 0, 0),
    "location": "View3D > N-Panel > Trophy Maker",
    "description": "Procedurally generates highly stylized, faceless human trophy figures.",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy
import bmesh
import math
from mathutils import Vector, Matrix
from bpy_extras.io_utils import ExportHelper

# --- PROCEDURAL POSE GENERATOR (100+ POSES) ---
CORE_POSES = {
    # --- BASICS & CLASSICS ---
    "NEUTRAL": {"spine": (0,0,1), "l_uparm": (0.2,0,-0.9), "r_uparm": (-0.2,0,-0.9), "l_loarm": (0.1,0.1,-0.9), "r_loarm": (-0.1,0,-0.9), "l_thigh": (0.1,0,-1), "r_thigh": (-0.1,0,-1), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "T_POSE": {"spine": (0,0,1), "l_uparm": (1,0,0), "r_uparm": (-1,0,0), "l_loarm": (1,0,0), "r_loarm": (-1,0,0), "l_thigh": (0.1,0,-1), "r_thigh": (-0.1,0,-1), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "A_POSE": {"spine": (0,0,1), "l_uparm": (0.6,0,-0.6), "r_uparm": (-0.6,0,-0.6), "l_loarm": (0.6,0,-0.6), "r_loarm": (-0.6,0,-0.6), "l_thigh": (0.2,0,-1), "r_thigh": (-0.2,0,-1), "l_calf": (0.1,0,-1), "r_calf": (-0.1,0,-1)},

    # --- YOGA & ZEN ---
    "YOGA_TREE_POSE": {"spine": (0,0,1), "l_uparm": (0.5,0,0.8), "r_uparm": (-0.5,0,0.8), "l_loarm": (-0.5,0,0.8), "r_loarm": (0.5,0,0.8), "l_thigh": (0.1,0,-1), "r_thigh": (-0.8,0.2,-0.2), "l_calf": (0,0,-1), "r_calf": (0.8,-0.2,-0.8)},
    "YOGA_WARRIOR": {"spine": (0,0.2,0.9), "l_uparm": (1,0,0), "r_uparm": (-1,0,0), "l_loarm": (1,0,0), "r_loarm": (-1,0,0), "l_thigh": (0,0.8,-0.5), "r_thigh": (0,-0.8,-0.8), "l_calf": (0,0.2,-1), "r_calf": (0,-0.2,-1)},
    "YOGA_DOWNWARD_DOG": {"spine": (0,0.8,-0.5), "l_uparm": (0.2,0.6,-0.8), "r_uparm": (-0.2,0.6,-0.8), "l_loarm": (0,0.2,-1), "r_loarm": (0,0.2,-1), "l_thigh": (0.1,-0.8,-0.8), "r_thigh": (-0.1,-0.8,-0.8), "l_calf": (0,-0.2,-1), "r_calf": (0,-0.2,-1)},
    "YOGA_LOTUS": {"spine": (0,0,1), "l_uparm": (0.5,0.5,-0.5), "r_uparm": (-0.5,0.5,-0.5), "l_loarm": (-0.3,0.5,0), "r_loarm": (0.3,0.5,0), "l_thigh": (0.8,0.5,-0.2), "r_thigh": (-0.8,0.5,-0.2), "l_calf": (-0.8,-0.5,0.2), "r_calf": (0.8,-0.5,0.2)},
    "YOGA_COBRA": {"spine": (0,-0.6,0.8), "l_uparm": (0.3,-0.2,-0.8), "r_uparm": (-0.3,-0.2,-0.8), "l_loarm": (0,0.2,-1), "r_loarm": (0,0.2,-1), "l_thigh": (0.2,-0.8,-0.2), "r_thigh": (-0.2,-0.8,-0.2), "l_calf": (0,-1,-0.1), "r_calf": (0,-1,-0.1)},

    # --- MARTIAL ARTS (KUNG FU, JUJUTSU, KARATE) ---
    "KUNGFU_CRANE": {"spine": (0,0.1,1), "l_uparm": (0.8,0.2,0.5), "r_uparm": (-0.8,0.2,0.5), "l_loarm": (0.5,0.4,0.2), "r_loarm": (-0.5,0.4,0.2), "l_thigh": (0.1,0,-1), "r_thigh": (0,0.8,0), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "KUNGFU_HORSE_STANCE": {"spine": (0,0,1), "l_uparm": (0.2,1,0), "r_uparm": (-0.2,1,0), "l_loarm": (0,1,0), "r_loarm": (0,1,0), "l_thigh": (0.8,0,-0.4), "r_thigh": (-0.8,0,-0.4), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "KUNGFU_MANTIS": {"spine": (0,0.4,0.8), "l_uparm": (0.2,0.8,0.2), "r_uparm": (-0.5,0.2,0.5), "l_loarm": (0.1,0.2,-0.8), "r_loarm": (0.4,0.5,0), "l_thigh": (0,0.5,-0.8), "r_thigh": (0,-0.5,-0.8), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "JUJUTSU_THROW": {"spine": (0,0.6,0.6), "l_uparm": (0.6,0.5,-0.2), "r_uparm": (-0.6,0.8,0.2), "l_loarm": (-0.4,0.8,-0.5), "r_loarm": (0.2,0.8,-0.5), "l_thigh": (0.4,0.6,-0.6), "r_thigh": (-0.2,-0.8,-0.6), "l_calf": (0,-0.2,-1), "r_calf": (0,0.2,-1)},
    "KARATE_KAMA_AE": {"spine": (0,0.1,0.9), "l_uparm": (0.2,0.6,-0.4), "r_uparm": (-0.3,-0.2,-0.6), "l_loarm": (0.1,0.8,0.4), "r_loarm": (-0.2,0.4,0.6), "l_thigh": (0.2,0.6,-0.8), "r_thigh": (-0.4,-0.6,-0.8), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "KARATE_HIGH_BLOCK": {"spine": (0,0,1), "l_uparm": (0.2,0.2,0.8), "r_uparm": (-0.4,0,-0.8), "l_loarm": (-0.5,0.5,0.4), "r_loarm": (0,0.5,0), "l_thigh": (0.3,0.5,-0.8), "r_thigh": (-0.3,-0.5,-0.9), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "MARTIAL_FLYING_KICK": {"spine": (0,-0.4,0.7), "l_uparm": (0.8,-0.2,0.2), "r_uparm": (-0.6,0.4,0.5), "l_loarm": (0.6,0.2,-0.4), "r_loarm": (-0.4,0.5,0), "l_thigh": (0,0.9,0.2), "r_thigh": (0,-0.5,-0.8), "l_calf": (0,0.8,-0.2), "r_calf": (0,0,-1)},

    # --- CULTURAL & CLASSICAL ART ---
    "ART_ATLAS_HOLDING": {"spine": (0,0.5,0.8), "l_uparm": (0.6,0.2,0.8), "r_uparm": (-0.6,0.2,0.8), "l_loarm": (-0.2,0,0.8), "r_loarm": (0.2,0,0.8), "l_thigh": (0.2,0.8,-0.2), "r_thigh": (-0.3,0.2,-1), "l_calf": (0,-0.8,-0.2), "r_calf": (0,0.2,-1)},
    "ART_DISCUS_THROWER": {"spine": (0.4,0.4,0.8), "l_uparm": (0.8,-0.4,0.2), "r_uparm": (-0.4,0.6,-0.6), "l_loarm": (0.8,-0.2,0.2), "r_loarm": (0.4,0.6,0.2), "l_thigh": (0.2,0.5,-0.8), "r_thigh": (-0.4,-0.2,-0.9), "l_calf": (0,0,-1), "r_calf": (0,-0.2,-1)},
    "CULTURE_EGYPTIAN_WALK": {"spine": (0,0,1), "l_uparm": (0,0.8,0), "r_uparm": (0,-0.8,0), "l_loarm": (0,0,1), "r_loarm": (0,0,-1), "l_thigh": (0,0.6,-0.8), "r_thigh": (0,-0.4,-1), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "CULTURE_NAMASTE": {"spine": (0,0.2,0.9), "l_uparm": (0.4,0,-0.6), "r_uparm": (-0.4,0,-0.6), "l_loarm": (-0.5,0.4,0.6), "r_loarm": (0.5,0.4,0.6), "l_thigh": (0.1,0,-1), "r_thigh": (-0.1,0,-1), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "CULTURE_FLAMENCO": {"spine": (0,-0.3,0.9), "l_uparm": (0.6,0,0.8), "r_uparm": (-0.8,0,-0.2), "l_loarm": (-0.4,0,0.8), "r_loarm": (-0.4,0,0.8), "l_thigh": (0.2,0,-1), "r_thigh": (-0.2,-0.5,-0.8), "l_calf": (0,0,-1), "r_calf": (0,-0.2,-1)},

    # --- SPORTS & ATHLETICS ---
    "SPORT_BOXING_GUARD": {"spine": (0,0.2,0.9), "l_uparm": (0.3,0.6,-0.2), "r_uparm": (-0.3,0.5,-0.3), "l_loarm": (-0.2,0.2,0.8), "r_loarm": (0.2,0.2,0.8), "l_thigh": (0.2,0.5,-0.8), "r_thigh": (-0.2,-0.2,-1), "l_calf": (0,-0.2,-1), "r_calf": (0,-0.2,-1)},
    "SPORT_ARCHERY_DRAW": {"spine": (0,0,1), "l_uparm": (0.8,0,0.2), "r_uparm": (-0.6,-0.4,0.2), "l_loarm": (0.8,0,0.2), "r_loarm": (0.6,0.4,0.2), "l_thigh": (0.5,0,-0.8), "r_thigh": (-0.5,0,-1), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "SPORT_FOOTBALL_KICK": {"spine": (0,-0.3,0.8), "l_uparm": (0.6,0,-0.5), "r_uparm": (-0.8,0.4,0.2), "l_loarm": (0.6,0,-0.5), "r_loarm": (-0.8,0.4,0.2), "l_thigh": (0,0,-1), "r_thigh": (0,0.9,0.2), "l_calf": (0,0,-1), "r_calf": (0,0.8,0.4)},
    "SPORT_BASKETBALL_DUNK": {"spine": (0,-0.2,0.9), "l_uparm": (0.4,0,0.9), "r_uparm": (-0.6,0,-0.4), "l_loarm": (0.4,0,0.9), "r_loarm": (-0.6,0,-0.4), "l_thigh": (0.2,0.5,-0.5), "r_thigh": (-0.2,-0.5,-0.8), "l_calf": (0,0.5,-0.8), "r_calf": (0,-0.5,-0.8)},

    # --- EDUCATION & LIFE ---
    "LIFE_THINKER": {"spine": (0,0.4,0.7), "l_uparm": (0.3,0.3,-0.6), "r_uparm": (-0.3,0.6,-0.2), "l_loarm": (0,0.5,-0.5), "r_loarm": (0,0.2,0.8), "l_thigh": (0.2,0.8,0), "r_thigh": (-0.2,0.8,0), "l_calf": (0,-0.5,-0.8), "r_calf": (0,-0.5,-0.8)},
    "LIFE_RAISING_HAND": {"spine": (0,0,1), "l_uparm": (0.2,0,-0.9), "r_uparm": (-0.2,0,0.9), "l_loarm": (0.1,0.1,-0.9), "r_loarm": (-0.2,0,0.9), "l_thigh": (0.1,0,-1), "r_thigh": (-0.1,0,-1), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "LIFE_SITTING": {"spine": (0,-0.2,1), "l_uparm": (0.3,-0.2,-0.8), "r_uparm": (-0.3,-0.2,-0.8), "l_loarm": (0.2,0.5,-0.5), "r_loarm": (-0.2,0.5,-0.5), "l_thigh": (0.2,0.9,0), "r_thigh": (-0.2,0.9,0), "l_calf": (0.2,0.8,-0.8), "r_calf": (-0.2,0.8,-0.8)},
    "LIFE_CROUCHING": {"spine": (0,0.6,0.6), "l_uparm": (0.3,0.5,-0.5), "r_uparm": (-0.3,0.5,-0.5), "l_loarm": (0,0.5,-0.5), "r_loarm": (0,0.5,-0.5), "l_thigh": (0.3,0.8,-0.2), "r_thigh": (-0.3,0.8,-0.2), "l_calf": (0,-0.5,-0.8), "r_calf": (0,-0.5,-0.8)},

    # --- GAMING & POP CULTURE ---
    "GAME_PRAISE_SUN": {"spine": (0,-0.2,0.9), "l_uparm": (0.7,0,0.7), "r_uparm": (-0.7,0,0.7), "l_loarm": (0.7,0,0.7), "r_loarm": (-0.7,0,0.7), "l_thigh": (0.1,0,-1), "r_thigh": (-0.1,0,-1), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "GAME_HERO_LANDING": {"spine": (0,0.7,0.5), "l_uparm": (0.5,0.2,-0.8), "r_uparm": (-0.6,-0.4,0.2), "l_loarm": (0.2,0.2,-0.8), "r_loarm": (-0.6,0.4,0.4), "l_thigh": (0.6,0.5,-0.4), "r_thigh": (-0.2,-0.6,-0.4), "l_calf": (0,-0.8,-0.6), "r_calf": (0,-0.8,-0.6)},
    "GAME_LEAP_OF_FAITH": {"spine": (0,0,1), "l_uparm": (0.9,0,0), "r_uparm": (-0.9,0,0), "l_loarm": (0.8,-0.2,0), "r_loarm": (-0.8,-0.2,0), "l_thigh": (0.1,-0.2,-1), "r_thigh": (-0.1,0.2,-0.9), "l_calf": (0,-0.2,-1), "r_calf": (0,-0.4,-0.6)},

    # --- DANCE & EMOTES ---
    "DANCE_FLOSS": {"spine": (0,0,1), "l_uparm": (-0.6,-0.5,-0.6), "r_uparm": (-0.8,-0.5,-0.4), "l_loarm": (0.2,-0.5,-0.8), "r_loarm": (-0.2,-0.5,-0.8), "l_thigh": (0.3,0,-1), "r_thigh": (-0.3,0,-1), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    "DANCE_MACARENA": {"spine": (0,0,1), "l_uparm": (0.6,0.6,-0.2), "r_uparm": (-0.6,0.6,-0.2), "l_loarm": (-0.6,-0.6,0), "r_loarm": (0.6,-0.6,0), "l_thigh": (0.2,0,-1), "r_thigh": (-0.2,0,-1), "l_calf": (0,0,-1), "r_calf": (0,0,-1)},
    
    # --- MISC ACTION ---
    "ACTION_RUNNING": {"spine": (0,0.3,0.9), "l_uparm": (0.2,-0.8,-0.2), "r_uparm": (-0.2,0.8,-0.2), "l_loarm": (0,-0.8,0.5), "r_loarm": (0,0.5,-0.5), "l_thigh": (0,0.8,-0.2), "r_thigh": (0,-0.5,-0.8), "l_calf": (0,-0.2,-1), "r_calf": (0,0.5,-0.8)},
    "ACTION_FLEXING": {"spine": (0,-0.1,0.9), "l_uparm": (0.8,0,0.2), "r_uparm": (-0.8,0,0.2), "l_loarm": (-0.6,0,0.8), "r_loarm": (0.6,0,0.8), "l_thigh": (0.4,0,-0.9), "r_thigh": (-0.4,0,-0.9), "l_calf": (0.1,0,-1), "r_calf": (-0.1,0,-1)},
}

def generate_100_poses():
    poses = {}
    def mirror_v(v): return Vector((-v[0], v[1], v[2]))
    for name, data in CORE_POSES.items():
        poses[name] = {k: Vector(v) for k, v in data.items()}
        poses[name + "_MIRRORED"] = {
            "spine": Vector(data["spine"]),
            "l_uparm": mirror_v(data["r_uparm"]), "r_uparm": mirror_v(data["l_uparm"]),
            "l_loarm": mirror_v(data["r_loarm"]), "r_loarm": mirror_v(data["l_loarm"]),
            "l_thigh": mirror_v(data["r_thigh"]), "r_thigh": mirror_v(data["l_thigh"]),
            "l_calf":  mirror_v(data["r_calf"]),  "r_calf":  mirror_v(data["l_calf"])
        }
        lean_f = {}
        for k, v in data.items(): lean_f[k] = Vector(v) + Vector((0, 0.4, -0.2)) if k == "spine" else Vector(v)
        poses[name + "_LEAN_FWD"] = lean_f

        lean_b = {}
        for k, v in data.items(): lean_b[k] = Vector(v) + Vector((0, -0.3, -0.1)) if k == "spine" else Vector(v)
        poses[name + "_LEAN_BACK"] = lean_b
    return poses

POSES = generate_100_poses()

def get_pose_items(self, context):
    """Dynamically populates the dropdown with icons and rich tooltips."""
    # Insert an empty placeholder as the very first option
    items = [('NONE', "--- Select a Pose ---", "Please choose a pose to generate the trophy", 'INFO', 0)]
    
    # Track assigned numbers so EnumProperty is valid
    item_idx = 1
    
    for p in sorted(list(POSES.keys())):
        name = p.replace("_", " ").title()
        
        # Default tooltip and icon
        desc = "Procedural pose variation"
        icon = 'USER'
        
        # Categorized Visuals & Rich Tooltips
        if "YOGA" in p:
            desc = "Flexibility & Balance: Smooth, grounded zen posture"
            icon = 'MAT_SPHERE_SKY'
        elif "KUNGFU" in p or "JUJUTSU" in p or "KARATE" in p or "MARTIAL" in p:
            desc = "Combat Stance: Aggressive, sharp angles, and tight guards"
            icon = 'ARMATURE_DATA'
        elif "ART_" in p or "CULTURE_" in p:
            desc = "Historical/Artistic: Expressive, dramatic, classical silhouette"
            icon = 'OUTLINER_OB_FONT'
        elif "SPORT" in p:
            desc = "Athletics: High momentum, explosive energy posture"
            icon = 'BONE_DATA'
        elif "GAME" in p or "DANCE" in p:
            desc = "Pop Culture Emote: Highly recognizable dynamic action"
            icon = 'COMMUNITY'
        elif "LIFE" in p:
            desc = "Everyday Posture: Relaxed, natural resting position"
            icon = 'OUTLINER_OB_META'

        if "MIRRORED" in p: desc += " (Left/Right Swapped)"
        if "LEAN_FWD" in p: desc += " (Leaning Forward)"
        if "LEAN_BACK" in p: desc += " (Leaning Backward)"
            
        items.append((p, name, desc, icon, item_idx))
        item_idx += 1
        
    return items

def create_dark_material():
    mat_name = "Matte_Dark_Trophy"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (0.05, 0.04, 0.045, 1)
            bsdf.inputs['Roughness'].default_value = 0.45
            bsdf.inputs['Specular IOR Level'].default_value = 0.3
    return mat

def trigger_update(self, context):
    if self.live_update:
        try: build_or_update_trophy(context)
        except Exception as e: print(f"Trophy Live Update Error: {e}")

def build_or_update_trophy(context):
    props = context.scene.trophy_props
    
    # If no pose is selected, clear the scene and do nothing
    if props.pose_enum == 'NONE':
        for name in ["TrophyFigure_Live", "TrophyBase_Live", "TrophyRibbon_Live"]:
            obj = bpy.data.objects.get(name)
            if obj: bpy.data.objects.remove(obj)
        return
        
    mat = create_dark_material()
    pose = POSES[props.pose_enum]
    t = props.scale_overall
    
    # Advanced Multipliers
    la_mult = props.arm_length * props.l_arm_scale
    ra_mult = props.arm_length * props.r_arm_scale
    ll_mult = props.leg_length * props.l_leg_scale
    rl_mult = props.leg_length * props.r_leg_scale

    # --- 1. Calculate Anatomical Vertices ---
    v_pelvis = Vector((0, 0, 0))
    
    # Spine (with intelligent arching)
    spine_vec = pose["spine"].normalized()
    arch_offset = Vector((0, props.spine_arch * t, 0))
    
    v_waist = v_pelvis + spine_vec * (props.torso_length * 0.4 * t) + (arch_offset * 0.5)
    v_chest = v_waist + spine_vec * (props.torso_length * 0.5 * t) + arch_offset
    v_neck = v_chest + spine_vec * (props.neck_length * 0.15 * t)
    
    # FIXED: Normalize the head direction so it tilts but never elongates!
    head_dir = Vector((0, spine_vec.y * 0.5, 1.0)).normalized()
    v_head = v_neck + head_dir * (0.25 * props.head_size * t)

    v_l_shldr = v_chest + Vector((props.shoulder_width * 0.5 * t, 0, 0))
    v_r_shldr = v_chest + Vector((-props.shoulder_width * 0.5 * t, 0, 0))
    v_l_hip = v_pelvis + Vector((props.pelvis_width * 0.5 * t, 0, 0))
    v_r_hip = v_pelvis + Vector((-props.pelvis_width * 0.5 * t, 0, 0))

    # Left Arm (With Elbow Flare)
    flare_l_arm = Vector((props.elbow_flare * t, 0, 0))
    v_l_elbow = v_l_shldr + pose["l_uparm"].normalized() * (la_mult * props.uparm_length * 0.9 * t) + flare_l_arm
    v_l_bicep = (v_l_shldr + v_l_elbow) / 2
    v_l_hand = v_l_elbow + pose["l_loarm"].normalized() * (la_mult * props.loarm_length * 0.9 * t) - flare_l_arm
    v_l_forearm = (v_l_elbow + v_l_hand) / 2

    # Right Arm (With Elbow Flare)
    flare_r_arm = Vector((-props.elbow_flare * t, 0, 0))
    v_r_elbow = v_r_shldr + pose["r_uparm"].normalized() * (ra_mult * props.uparm_length * 0.9 * t) + flare_r_arm
    v_r_bicep = (v_r_shldr + v_r_elbow) / 2
    v_r_hand = v_r_elbow + pose["r_loarm"].normalized() * (ra_mult * props.loarm_length * 0.9 * t) - flare_r_arm
    v_r_forearm = (v_r_elbow + v_r_hand) / 2

    # Left Leg (With Knee Flare)
    flare_l_leg = Vector((props.knee_flare * t, 0, 0))
    v_l_knee = v_l_hip + pose["l_thigh"].normalized() * (ll_mult * props.thigh_length * 1.3 * t) + flare_l_leg
    v_l_thigh = (v_l_hip + v_l_knee) / 2
    v_l_foot = v_l_knee + pose["l_calf"].normalized() * (ll_mult * props.calf_length * 1.3 * t) - flare_l_leg
    v_l_calf = (v_l_knee + v_l_foot) / 2

    # Right Leg (With Knee Flare)
    flare_r_leg = Vector((-props.knee_flare * t, 0, 0))
    v_r_knee = v_r_hip + pose["r_thigh"].normalized() * (rl_mult * props.thigh_length * 1.3 * t) + flare_r_leg
    v_r_thigh = (v_r_hip + v_r_knee) / 2
    v_r_foot = v_r_knee + pose["r_calf"].normalized() * (rl_mult * props.calf_length * 1.3 * t) - flare_r_leg
    v_r_calf = (v_r_knee + v_r_foot) / 2

    verts = [
        v_pelvis, v_waist, v_chest, v_neck, v_head,               # 0-4
        v_l_shldr, v_l_bicep, v_l_elbow, v_l_forearm, v_l_hand,   # 5-9
        v_r_shldr, v_r_bicep, v_r_elbow, v_r_forearm, v_r_hand,   # 10-14
        v_l_hip, v_l_thigh, v_l_knee, v_l_calf, v_l_foot,         # 15-19
        v_r_hip, v_r_thigh, v_r_knee, v_r_calf, v_r_foot          # 20-24
    ]

    # Grounding Logic
    lowest_z = min(v.z for v in verts)
    embed_depth = props.base_embed * t
    lift_offset = props.z_offset * t
    
    for v in verts:
        v.z -= lowest_z
        v.z -= embed_depth
        v.z += lift_offset

    edges = [
        (0,1), (1,2), (2,3), (3,4),                 
        (2,5), (5,6), (6,7), (7,8), (8,9),          
        (2,10), (10,11), (11,12), (12,13), (13,14), 
        (0,15), (15,16), (16,17), (17,18), (18,19), 
        (0,20), (20,21), (21,22), (22,23), (23,24)  
    ]

    # --- 2. Build or Update Mesh ---
    obj_name = "TrophyFigure_Live"
    obj = bpy.data.objects.get(obj_name)
    
    if not obj or len(obj.data.vertices) != len(verts):
        if obj: bpy.data.objects.remove(obj)
        mesh = bpy.data.meshes.new(obj_name + "_Mesh")
        mesh.from_pydata(verts, edges, [])
        obj = bpy.data.objects.new(obj_name, mesh)
        bpy.context.collection.objects.link(obj)
        obj.data.materials.append(mat)
    else:
        for i, v in enumerate(verts): obj.data.vertices[i].co = v

    # --- 3. Intelligent Modifiers (Anti-Tearing) ---
    obj.modifiers.clear()

    skin_mod = obj.modifiers.new(name="Skin", type='SKIN')
    skin_mod.use_smooth_shade = True

    subsurf_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf_mod.levels = 3
    subsurf_mod.render_levels = 4
    
    bpy.context.view_layer.update()

    # Apply Radii and explicitly set Root vertex to prevent tree inversion tearing
    tt = props.torso_thick * t
    nt = props.neck_thick * t
    at = props.arm_thick * t
    lt = props.leg_thick * t
    hs = props.head_size * t
    hand = props.hand_size * at
    foot = props.foot_size * lt

    radii_map = {
        0: (tt * 0.22, tt * 0.18), 1: (tt * 0.16, tt * 0.14), 2: (tt * 0.26, tt * 0.18), 
        3: (nt * 0.08, nt * 0.08), 4: (hs * 0.18, hs * 0.20),
        5: (at * 0.12, at * 0.12), 6: (at * 0.10, at * 0.10), 7: (at * 0.08, at * 0.08), 8: (at * 0.06, at * 0.06), 9: (hand * 0.04, hand * 0.03),
        10: (at * 0.12, at * 0.12), 11: (at * 0.10, at * 0.10), 12: (at * 0.08, at * 0.08), 13: (at * 0.06, at * 0.06), 14: (hand * 0.04, hand * 0.03),
        15: (lt * 0.16, lt * 0.16), 16: (lt * 0.14, lt * 0.14), 17: (lt * 0.11, lt * 0.11), 18: (lt * 0.08, lt * 0.08), 19: (foot * 0.05, foot * 0.04),
        20: (lt * 0.16, lt * 0.16), 21: (lt * 0.14, lt * 0.14), 22: (lt * 0.11, lt * 0.11), 23: (lt * 0.08, lt * 0.08), 24: (foot * 0.05, foot * 0.04)
    }

    if len(obj.data.skin_vertices) > 0:
        skin_layer = obj.data.skin_vertices[0].data
        for v in skin_layer: v.use_root = False
        skin_layer[0].use_root = True
        for i, rad in radii_map.items(): skin_layer[i].radius = rad

    for poly in obj.data.polygons: poly.use_smooth = True

    # --- 4. Plinth (Base) ---
    base_name = "TrophyBase_Live"
    base_obj = bpy.data.objects.get(base_name)

    if not props.show_base:
        if base_obj: bpy.data.objects.remove(base_obj)
        base_obj = None
        obj.parent = None
    else:
        if not base_obj:
            mesh = bpy.data.meshes.new(base_name + "_Mesh")
            base_obj = bpy.data.objects.new(base_name, mesh)
            bpy.context.collection.objects.link(base_obj)
            base_obj.data.materials.append(mat)
            obj.parent = base_obj

        bm = bmesh.new()
        bw = props.base_width * t
        bd = props.base_depth * t
        bh = props.base_height * t

        if props.base_enum == 'WEDGE':
            bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(bw, bd, bh), verts=bm.verts)
            bmesh.ops.translate(bm, vec=(0, 0, -bh/2), verts=bm.verts) 
            top_verts = [v for v in bm.verts if v.co.z > -bh * 0.2]
            bottom_verts = [v for v in bm.verts if v.co.z < -bh * 0.8]
            bmesh.ops.scale(bm, vec=(0.2, 1.0, 1.0), verts=[v for v in top_verts if v.co.x > 0])
            bmesh.ops.scale(bm, vec=(0.2, 1.0, 1.0), verts=[v for v in top_verts if v.co.x < 0])
            bmesh.ops.translate(bm, vec=(-bw*0.3, 0, 0), verts=[v for v in bottom_verts if v.co.x < 0])
            
        elif props.base_enum == 'CUBE':
            bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(bw, bd, bh), verts=bm.verts)
            bmesh.ops.translate(bm, vec=(0, 0, -bh/2), verts=bm.verts) 
            
        elif props.base_enum == 'BEVELED_CUBE':
            bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(bw, bd, bh), verts=bm.verts)
            bmesh.ops.translate(bm, vec=(0, 0, -bh/2), verts=bm.verts) 
            if not base_obj.modifiers.get("Bevel"):
                bevel = base_obj.modifiers.new(name="Bevel", type='BEVEL')
                bevel.segments = 4
                bevel.width = 0.08

        elif props.base_enum == 'CYLINDER':
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=64, radius1=0.5, radius2=0.5, depth=1.0)
            bmesh.ops.scale(bm, vec=(bw, bd, bh), verts=bm.verts)
            bmesh.ops.translate(bm, vec=(0, 0, -bh/2), verts=bm.verts) 
            if not base_obj.modifiers.get("Bevel"):
                bevel = base_obj.modifiers.new(name="Bevel", type='BEVEL')
                bevel.segments = 3
                bevel.width = 0.05
                
        elif props.base_enum == 'CONE':
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=64, radius1=0.5, radius2=0.35, depth=1.0)
            bmesh.ops.scale(bm, vec=(bw, bd, bh), verts=bm.verts)
            bmesh.ops.translate(bm, vec=(0, 0, -bh/2), verts=bm.verts) 
            
        elif props.base_enum == 'PYRAMID':
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=4, radius1=0.707, radius2=0.5, depth=1.0)
            bmesh.ops.rotate(bm, cent=(0,0,0), matrix=Matrix.Rotation(math.radians(45), 3, 'Z'), verts=bm.verts)
            bmesh.ops.scale(bm, vec=(bw, bd, bh), verts=bm.verts)
            bmesh.ops.translate(bm, vec=(0, 0, -bh/2), verts=bm.verts) 
            
        elif props.base_enum == 'HEXAGON':
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6, radius1=0.5, radius2=0.5, depth=1.0)
            bmesh.ops.rotate(bm, cent=(0,0,0), matrix=Matrix.Rotation(math.radians(30), 3, 'Z'), verts=bm.verts)
            bmesh.ops.scale(bm, vec=(bw, bd, bh), verts=bm.verts)
            bmesh.ops.translate(bm, vec=(0, 0, -bh/2), verts=bm.verts) 
            
        elif props.base_enum == 'OCTAGON':
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8, radius1=0.5, radius2=0.5, depth=1.0)
            bmesh.ops.rotate(bm, cent=(0,0,0), matrix=Matrix.Rotation(math.radians(22.5), 3, 'Z'), verts=bm.verts)
            bmesh.ops.scale(bm, vec=(bw, bd, bh), verts=bm.verts)
            bmesh.ops.translate(bm, vec=(0, 0, -bh/2), verts=bm.verts) 
            
        elif props.base_enum == 'STEPPED':
            bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(bw, bd, bh*0.5), verts=bm.verts[-8:])
            bmesh.ops.translate(bm, vec=(0, 0, -bh*0.75), verts=bm.verts[-8:])
            bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(bw*0.8, bd*0.8, bh*0.5), verts=bm.verts[-8:])
            bmesh.ops.translate(bm, vec=(0, 0, -bh*0.25), verts=bm.verts[-8:])
                
        if lift_offset > 0.01:
            start_idx = len(bm.verts)
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16, radius1=0.04*t, radius2=0.04*t, depth=lift_offset + 0.1)
            new_verts = bm.verts[start_idx:]
            lowest_v_xy = Vector((verts[min(range(len(verts)), key=lambda i: verts[i].z)].x, verts[min(range(len(verts)), key=lambda i: verts[i].z)].y, 0))
            bmesh.ops.translate(bm, vec=(lowest_v_xy.x, lowest_v_xy.y, lift_offset/2 - 0.05), verts=new_verts)

        bm.to_mesh(base_obj.data)
        bm.free()
        for poly in base_obj.data.polygons: poly.use_smooth = True

    # --- 5. Ribbon ---
    ribbon_name = "TrophyRibbon_Live"
    ribbon_obj = bpy.data.objects.get(ribbon_name)
    
    if "RIBBON" in props.pose_enum or "MACARENA" in props.pose_enum:
        if not ribbon_obj:
            curve_data = bpy.data.curves.new('RibbonCurve', type='CURVE')
            curve_data.dimensions = '3D'
            curve_data.fill_mode = 'FULL'
            ribbon_obj = bpy.data.objects.new(ribbon_name, curve_data)
            bpy.context.collection.objects.link(ribbon_obj)
            ribbon_obj.data.materials.append(mat)
            ribbon_obj.parent = base_obj
            spline = curve_data.splines.new('NURBS')
            spline.use_endpoint_u = True
            spline.points.add(5)
        
        ribbon_obj.data.bevel_depth = 0.04 * t
        ribbon_obj.data.bevel_resolution = 4
        
        pts = [
            verts[9], # L Hand
            verts[9] + Vector((0, 0.5 * t, 0.5 * t)),
            verts[4] + Vector((-0.5 * t, 0.5 * t, 0.8 * t)),
            verts[4] + Vector((0.5 * t, 0.5 * t, 0.8 * t)),
            verts[14] + Vector((0, 0.5 * t, 0.5 * t)),
            verts[14]  # R Hand
        ]
        for i, pt in enumerate(pts):
            ribbon_obj.data.splines[0].points[i].co = (pt.x, pt.y, pt.z, 1)
    else:
        if ribbon_obj: bpy.data.objects.remove(ribbon_obj)

    obj.data.update()

# --- UI & PROPERTIES ---

class TrophyProperties(bpy.types.PropertyGroup):
    live_update: bpy.props.BoolProperty(name="Live Update", default=True)
    
    # FIX: Removed default='NONE' because dynamic items cannot have string defaults in Blender API
    pose_enum: bpy.props.EnumProperty(name="Pose", items=get_pose_items, update=trigger_update)
    
    show_base: bpy.props.BoolProperty(name="Include Base", default=True, update=trigger_update)
    
    base_enum: bpy.props.EnumProperty(
        name="Base Style", 
        items=[
            ('BEVELED_CUBE', "Beveled Box", ""),
            ('CUBE', "Classic Block", ""),
            ('WEDGE', "Angular Wedge", ""), 
            ('CYLINDER', "Round Cylinder", ""),
            ('CONE', "Tapered Cone", ""),
            ('PYRAMID', "Pyramid", ""),
            ('HEXAGON', "Hexagon", ""),
            ('OCTAGON', "Octagon", ""),
            ('STEPPED', "Stepped Pedestal", "")
        ], 
        default='BEVELED_CUBE', 
        update=trigger_update
    )
    
    # Sensible Limits (0.001 to 10.0)
    base_width: bpy.props.FloatProperty(name="Width", default=1.5, min=0.001, max=10.0, update=trigger_update)
    base_depth: bpy.props.FloatProperty(name="Depth", default=1.0, min=0.001, max=10.0, update=trigger_update)
    base_height: bpy.props.FloatProperty(name="Height", default=0.4, min=0.001, max=10.0, update=trigger_update)
    base_embed: bpy.props.FloatProperty(name="Embed Depth", default=0.1, min=-5.0, max=5.0, update=trigger_update)
    z_offset: bpy.props.FloatProperty(name="Vertical Lift", default=0.0, min=-5.0, max=10.0, update=trigger_update)

    scale_overall: bpy.props.FloatProperty(name="Overall Scale", default=1.0, min=0.001, max=10.0, update=trigger_update)
    arm_length: bpy.props.FloatProperty(name="Arm Length", default=1.0, min=0.001, max=10.0, update=trigger_update)
    leg_length: bpy.props.FloatProperty(name="Leg Length", default=1.0, min=0.001, max=10.0, update=trigger_update)
    
    spine_arch: bpy.props.FloatProperty(name="Spine Arch", default=0.0, min=-10.0, max=10.0, update=trigger_update)
    elbow_flare: bpy.props.FloatProperty(name="Elbow Flare", default=0.0, min=-10.0, max=10.0, update=trigger_update)
    knee_flare: bpy.props.FloatProperty(name="Knee Flare", default=0.0, min=-10.0, max=10.0, update=trigger_update)
    
    l_arm_scale: bpy.props.FloatProperty(name="Left Arm Scale", default=1.0, min=0.001, max=10.0, update=trigger_update)
    r_arm_scale: bpy.props.FloatProperty(name="Right Arm Scale", default=1.0, min=0.001, max=10.0, update=trigger_update)
    l_leg_scale: bpy.props.FloatProperty(name="Left Leg Scale", default=1.0, min=0.001, max=10.0, update=trigger_update)
    r_leg_scale: bpy.props.FloatProperty(name="Right Leg Scale", default=1.0, min=0.001, max=10.0, update=trigger_update)

    torso_length: bpy.props.FloatProperty(name="Torso Length", default=1.0, min=0.001, max=10.0, update=trigger_update)
    neck_length: bpy.props.FloatProperty(name="Neck Length", default=1.0, min=0.001, max=10.0, update=trigger_update)
    uparm_length: bpy.props.FloatProperty(name="Upper Arm Length", default=1.0, min=0.001, max=10.0, update=trigger_update)
    loarm_length: bpy.props.FloatProperty(name="Forearm Length", default=1.0, min=0.001, max=10.0, update=trigger_update)
    thigh_length: bpy.props.FloatProperty(name="Thigh Length", default=1.0, min=0.001, max=10.0, update=trigger_update)
    calf_length: bpy.props.FloatProperty(name="Calf Length", default=1.0, min=0.001, max=10.0, update=trigger_update)
    
    head_size: bpy.props.FloatProperty(name="Head Size", default=1.0, min=0.001, max=10.0, update=trigger_update)
    shoulder_width: bpy.props.FloatProperty(name="Shoulder Width", default=1.0, min=0.001, max=10.0, update=trigger_update)
    pelvis_width: bpy.props.FloatProperty(name="Pelvis Width", default=1.0, min=0.001, max=10.0, update=trigger_update)
    hand_size: bpy.props.FloatProperty(name="Hand Size", default=1.0, min=0.001, max=10.0, update=trigger_update)
    foot_size: bpy.props.FloatProperty(name="Foot Size", default=1.0, min=0.001, max=10.0, update=trigger_update)
    
    neck_thick: bpy.props.FloatProperty(name="Neck Thickness", default=1.0, min=0.001, max=10.0, update=trigger_update)
    arm_thick: bpy.props.FloatProperty(name="Arm Thickness", default=1.0, min=0.001, max=10.0, update=trigger_update)
    leg_thick: bpy.props.FloatProperty(name="Leg Thickness", default=1.0, min=0.001, max=10.0, update=trigger_update)
    torso_thick: bpy.props.FloatProperty(name="Torso Girth", default=1.0, min=0.001, max=10.0, update=trigger_update)

class OBJECT_OT_GenerateTrophy(bpy.types.Operator):
    bl_idname = "object.generate_trophy"
    bl_label = "Initialize / Rebuild"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        build_or_update_trophy(context)
        return {'FINISHED'}

class OBJECT_OT_ExportSTL(bpy.types.Operator, ExportHelper):
    bl_idname = "export.trophy_stl"
    bl_label = "Export STL (Print)"
    filename_ext = ".stl"
    
    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        active_set = False
        
        # Select all generated components
        for name in ["TrophyFigure_Live", "TrophyBase_Live", "TrophyRibbon_Live"]:
            obj = bpy.data.objects.get(name)
            if obj: 
                obj.select_set(True)
                if not active_set:
                    context.view_layer.objects.active = obj
                    active_set = True
                    
        if not active_set:
            self.report({'ERROR'}, "No Trophy generated to export.")
            return {'CANCELLED'}
            
        # Handle Blender 4.2+ API changes (Legacy Python exporter vs New C++ exporter)
        try:
            # New C++ STL exporter (Blender 4.1/4.2+)
            bpy.ops.wm.stl_export(filepath=self.filepath, export_selected_objects=True)
        except AttributeError:
            # Legacy Python STL exporter (Blender 3.x to 4.0)
            bpy.ops.export_mesh.stl(filepath=self.filepath, use_selection=True)
            
        self.report({'INFO'}, f"Exported STL to {self.filepath}")
        return {'FINISHED'}

class OBJECT_OT_ExportGLB(bpy.types.Operator, ExportHelper):
    bl_idname = "export.trophy_glb"
    bl_label = "Export GLB (Web)"
    filename_ext = ".glb"
    
    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        active_set = False
        
        for name in ["TrophyFigure_Live", "TrophyBase_Live", "TrophyRibbon_Live"]:
            obj = bpy.data.objects.get(name)
            if obj: 
                obj.select_set(True)
                if not active_set:
                    context.view_layer.objects.active = obj
                    active_set = True
                    
        if not active_set:
            self.report({'ERROR'}, "No Trophy generated to export.")
            return {'CANCELLED'}
            
        # export_apply=True is CRITICAL: it forces the skin, subsurf, and boolean modifiers to bake into the mesh
        bpy.ops.export_scene.gltf(filepath=self.filepath, export_format='GLB', use_selection=True, export_apply=True)
        self.report({'INFO'}, f"Exported GLB to {self.filepath}")
        return {'FINISHED'}

class OBJECT_OT_ExportCode(bpy.types.Operator):
    bl_idname = "export.trophy_code"
    bl_label = "Copy Code to Clipboard"
    
    def execute(self, context):
        props = context.scene.trophy_props
        
        if props.pose_enum == 'NONE':
            self.report({'ERROR'}, "Please select a pose first!")
            return {'CANCELLED'}
        
        pose_data = POSES[props.pose_enum]
        pose_str = str({k: (v.x, v.y, v.z) for k, v in pose_data.items()})
        
        script = f'''import bpy
import bmesh
import math
from mathutils import Vector, Matrix

# --- Configuration Generated from Addon ---
pose_data = {pose_str}
pose = {{k: Vector(v) for k, v in pose_data.items()}}

t = {props.scale_overall}
la_mult = {props.arm_length * props.l_arm_scale}
ra_mult = {props.arm_length * props.r_arm_scale}
ll_mult = {props.leg_length * props.l_leg_scale}
rl_mult = {props.leg_length * props.r_leg_scale}

torso_length = {props.torso_length}
neck_length = {props.neck_length}
head_size = {props.head_size}
shoulder_width = {props.shoulder_width}
pelvis_width = {props.pelvis_width}

uparm_length = {props.uparm_length}
loarm_length = {props.loarm_length}
thigh_length = {props.thigh_length}
calf_length = {props.calf_length}

spine_arch = {props.spine_arch}
elbow_flare = {props.elbow_flare}
knee_flare = {props.knee_flare}

base_embed = {props.base_embed}
z_offset = {props.z_offset}

tt = {props.torso_thick} * t
nt = {props.neck_thick} * t
at = {props.arm_thick} * t
lt = {props.leg_thick} * t
hs = {props.head_size} * t
hand = {props.hand_size} * at
foot = {props.foot_size} * lt

show_base = {props.show_base}
base_enum = '{props.base_enum}'
base_width = {props.base_width} * t
base_depth = {props.base_depth} * t
base_height = {props.base_height} * t

# --- Material ---
def create_dark_material():
    mat_name = "Matte_Dark_Trophy_Standalone"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (0.05, 0.04, 0.045, 1)
            bsdf.inputs['Roughness'].default_value = 0.45
            bsdf.inputs['Specular IOR Level'].default_value = 0.3
    return mat

mat = create_dark_material()

# --- Vertices ---
v_pelvis = Vector((0, 0, 0))
spine_vec = pose["spine"].normalized()
arch_offset = Vector((0, spine_arch * t, 0))

v_waist = v_pelvis + spine_vec * (torso_length * 0.4 * t) + (arch_offset * 0.5)
v_chest = v_waist + spine_vec * (torso_length * 0.5 * t) + arch_offset
v_neck = v_chest + spine_vec * (neck_length * 0.15 * t)
head_dir = Vector((0, spine_vec.y * 0.5, 1.0)).normalized()
v_head = v_neck + head_dir * (0.25 * head_size * t)

v_l_shldr = v_chest + Vector((shoulder_width * 0.5 * t, 0, 0))
v_r_shldr = v_chest + Vector((-shoulder_width * 0.5 * t, 0, 0))
v_l_hip = v_pelvis + Vector((pelvis_width * 0.5 * t, 0, 0))
v_r_hip = v_pelvis + Vector((-pelvis_width * 0.5 * t, 0, 0))

flare_l_arm = Vector((elbow_flare * t, 0, 0))
v_l_elbow = v_l_shldr + pose["l_uparm"].normalized() * (la_mult * uparm_length * 0.9 * t) + flare_l_arm
v_l_bicep = (v_l_shldr + v_l_elbow) / 2
v_l_hand = v_l_elbow + pose["l_loarm"].normalized() * (la_mult * loarm_length * 0.9 * t) - flare_l_arm
v_l_forearm = (v_l_elbow + v_l_hand) / 2

flare_r_arm = Vector((-elbow_flare * t, 0, 0))
v_r_elbow = v_r_shldr + pose["r_uparm"].normalized() * (ra_mult * uparm_length * 0.9 * t) + flare_r_arm
v_r_bicep = (v_r_shldr + v_r_elbow) / 2
v_r_hand = v_r_elbow + pose["r_loarm"].normalized() * (ra_mult * loarm_length * 0.9 * t) - flare_r_arm
v_r_forearm = (v_r_elbow + v_r_hand) / 2

flare_l_leg = Vector((knee_flare * t, 0, 0))
v_l_knee = v_l_hip + pose["l_thigh"].normalized() * (ll_mult * thigh_length * 1.3 * t) + flare_l_leg
v_l_thigh = (v_l_hip + v_l_knee) / 2
v_l_foot = v_l_knee + pose["l_calf"].normalized() * (ll_mult * calf_length * 1.3 * t) - flare_l_leg
v_l_calf = (v_l_knee + v_l_foot) / 2

flare_r_leg = Vector((-knee_flare * t, 0, 0))
v_r_knee = v_r_hip + pose["r_thigh"].normalized() * (rl_mult * thigh_length * 1.3 * t) + flare_r_leg
v_r_thigh = (v_r_hip + v_r_knee) / 2
v_r_foot = v_r_knee + pose["r_calf"].normalized() * (rl_mult * calf_length * 1.3 * t) - flare_r_leg
v_r_calf = (v_r_knee + v_r_foot) / 2

verts = [
    v_pelvis, v_waist, v_chest, v_neck, v_head,
    v_l_shldr, v_l_bicep, v_l_elbow, v_l_forearm, v_l_hand,
    v_r_shldr, v_r_bicep, v_r_elbow, v_r_forearm, v_r_hand,
    v_l_hip, v_l_thigh, v_l_knee, v_l_calf, v_l_foot,
    v_r_hip, v_r_thigh, v_r_knee, v_r_calf, v_r_foot
]

lowest_z = min(v.z for v in verts)
for v in verts:
    v.z -= lowest_z
    v.z -= base_embed * t
    v.z += z_offset * t

edges = [
    (0,1), (1,2), (2,3), (3,4),                 
    (2,5), (5,6), (6,7), (7,8), (8,9),          
    (2,10), (10,11), (11,12), (12,13), (13,14), 
    (0,15), (15,16), (16,17), (17,18), (18,19), 
    (0,20), (20,21), (21,22), (22,23), (23,24)  
]

# --- Mesh Generation ---
mesh = bpy.data.meshes.new("TrophyFigure_Standalone_Mesh")
mesh.from_pydata(verts, edges, [])
obj = bpy.data.objects.new("TrophyFigure_Standalone", mesh)
bpy.context.collection.objects.link(obj)
obj.data.materials.append(mat)

skin_mod = obj.modifiers.new(name="Skin", type='SKIN')
skin_mod.use_smooth_shade = True
subsurf_mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
subsurf_mod.levels = 3
subsurf_mod.render_levels = 4
bpy.context.view_layer.update()

radii_map = {{
    0: (tt * 0.22, tt * 0.18), 1: (tt * 0.16, tt * 0.14), 2: (tt * 0.26, tt * 0.18), 
    3: (nt * 0.08, nt * 0.08), 4: (hs * 0.18, hs * 0.20),
    5: (at * 0.12, at * 0.12), 6: (at * 0.10, at * 0.10), 7: (at * 0.08, at * 0.08), 8: (at * 0.06, at * 0.06), 9: (hand * 0.04, hand * 0.03),
    10: (at * 0.12, at * 0.12), 11: (at * 0.10, at * 0.10), 12: (at * 0.08, at * 0.08), 13: (at * 0.06, at * 0.06), 14: (hand * 0.04, hand * 0.03),
    15: (lt * 0.16, lt * 0.16), 16: (lt * 0.14, lt * 0.14), 17: (lt * 0.11, lt * 0.11), 18: (lt * 0.08, lt * 0.08), 19: (foot * 0.05, foot * 0.04),
    20: (lt * 0.16, lt * 0.16), 21: (lt * 0.14, lt * 0.14), 22: (lt * 0.11, lt * 0.11), 23: (lt * 0.08, lt * 0.08), 24: (foot * 0.05, foot * 0.04)
}}

if len(obj.data.skin_vertices) > 0:
    skin_layer = obj.data.skin_vertices[0].data
    for v in skin_layer: v.use_root = False
    skin_layer[0].use_root = True
    for i, rad in radii_map.items(): skin_layer[i].radius = rad

for poly in obj.data.polygons: poly.use_smooth = True

# --- Base Generation ---
if show_base:
    base_mesh = bpy.data.meshes.new("TrophyBase_Standalone_Mesh")
    base_obj = bpy.data.objects.new("TrophyBase_Standalone", base_mesh)
    bpy.context.collection.objects.link(base_obj)
    base_obj.data.materials.append(mat)
    obj.parent = base_obj

    bm = bmesh.new()
    if base_enum == 'WEDGE':
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(base_width, base_depth, base_height), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, -base_height/2), verts=bm.verts) 
        top_verts = [v for v in bm.verts if v.co.z > -base_height * 0.2]
        bottom_verts = [v for v in bm.verts if v.co.z < -base_height * 0.8]
        bmesh.ops.scale(bm, vec=(0.2, 1.0, 1.0), verts=[v for v in top_verts if v.co.x > 0])
        bmesh.ops.scale(bm, vec=(0.2, 1.0, 1.0), verts=[v for v in top_verts if v.co.x < 0])
        bmesh.ops.translate(bm, vec=(-base_width*0.3, 0, 0), verts=[v for v in bottom_verts if v.co.x < 0])
    elif base_enum == 'CUBE':
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(base_width, base_depth, base_height), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, -base_height/2), verts=bm.verts) 
    elif base_enum == 'BEVELED_CUBE':
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(base_width, base_depth, base_height), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, -base_height/2), verts=bm.verts) 
        bevel = base_obj.modifiers.new(name="Bevel", type='BEVEL')
        bevel.segments = 4
        bevel.width = 0.08
    elif base_enum == 'CYLINDER':
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=64, radius1=0.5, radius2=0.5, depth=1.0)
        bmesh.ops.scale(bm, vec=(base_width, base_depth, base_height), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, -base_height/2), verts=bm.verts) 
        bevel = base_obj.modifiers.new(name="Bevel", type='BEVEL')
        bevel.segments = 3
        bevel.width = 0.05
    elif base_enum == 'CONE':
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=64, radius1=0.5, radius2=0.35, depth=1.0)
        bmesh.ops.scale(bm, vec=(base_width, base_depth, base_height), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, -base_height/2), verts=bm.verts) 
    elif base_enum == 'PYRAMID':
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=4, radius1=0.707, radius2=0.5, depth=1.0)
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=Matrix.Rotation(math.radians(45), 3, 'Z'), verts=bm.verts)
        bmesh.ops.scale(bm, vec=(base_width, base_depth, base_height), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, -base_height/2), verts=bm.verts) 
    elif base_enum == 'HEXAGON':
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6, radius1=0.5, radius2=0.5, depth=1.0)
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=Matrix.Rotation(math.radians(30), 3, 'Z'), verts=bm.verts)
        bmesh.ops.scale(bm, vec=(base_width, base_depth, base_height), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, -base_height/2), verts=bm.verts) 
    elif base_enum == 'OCTAGON':
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=8, radius1=0.5, radius2=0.5, depth=1.0)
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=Matrix.Rotation(math.radians(22.5), 3, 'Z'), verts=bm.verts)
        bmesh.ops.scale(bm, vec=(base_width, base_depth, base_height), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(0, 0, -base_height/2), verts=bm.verts) 
    elif base_enum == 'STEPPED':
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(base_width, base_depth, base_height*0.5), verts=bm.verts[-8:])
        bmesh.ops.translate(bm, vec=(0, 0, -base_height*0.75), verts=bm.verts[-8:])
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(base_width*0.8, base_depth*0.8, base_height*0.5), verts=bm.verts[-8:])
        bmesh.ops.translate(bm, vec=(0, 0, -base_height*0.25), verts=bm.verts[-8:])
        
    if z_offset * t > 0.01:
        start_idx = len(bm.verts)
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16, radius1=0.04*t, radius2=0.04*t, depth=z_offset*t + 0.1)
        new_verts = bm.verts[start_idx:]
        lowest_v_xy = Vector((verts[min(range(len(verts)), key=lambda i: verts[i].z)].x, verts[min(range(len(verts)), key=lambda i: verts[i].z)].y, 0))
        bmesh.ops.translate(bm, vec=(lowest_v_xy.x, lowest_v_xy.y, z_offset*t/2 - 0.05), verts=new_verts)

    bm.to_mesh(base_obj.data)
    bm.free()
    for poly in base_obj.data.polygons: poly.use_smooth = True

# Force scene update to apply skin radii
bpy.context.view_layer.update()
'''
        context.window_manager.clipboard = script
        self.report({'INFO'}, "Standalone script copied to clipboard!")
        return {'FINISHED'}

class VIEW3D_PT_TrophyMaker(bpy.types.Panel):
    bl_label = "Trophy Maker Tools"
    bl_idname = "VIEW3D_PT_trophy_maker"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Trophy Maker'

    def draw(self, context):
        layout = self.layout
        props = context.scene.trophy_props

        # Header controls
        row = layout.row()
        row.prop(props, "live_update", toggle=True, icon='FILE_REFRESH')
        row.operator(OBJECT_OT_GenerateTrophy.bl_idname, text="Force Rebuild")
        
        layout.separator()
        layout.prop(props, "pose_enum", text="")

        # Organised into layout boxes to save space and look clean
        box = layout.box()
        box.label(text="Base Configuration", icon='MESH_CUBE')
        box.prop(props, "show_base")
        if props.show_base:
            box.prop(props, "base_enum", text="")
            col = box.column(align=True)
            col.prop(props, "base_width")
            col.prop(props, "base_depth")
            col.prop(props, "base_height")
            col.separator()
            col.prop(props, "base_embed")
            col.prop(props, "z_offset")

        box = layout.box()
        box.label(text="Posture & Joints", icon='ARMATURE_DATA')
        col = box.column(align=True)
        col.prop(props, "spine_arch")
        col.prop(props, "elbow_flare")
        col.prop(props, "knee_flare")

        box = layout.box()
        box.label(text="Overall Proportions", icon='CON_SIZELIKE')
        col = box.column(align=True)
        col.prop(props, "scale_overall", slider=True)
        col.prop(props, "arm_length", slider=True)
        col.prop(props, "leg_length", slider=True)

        box = layout.box()
        box.label(text="Bone Lengths", icon='BONE_DATA')
        col = box.column(align=True)
        col.prop(props, "torso_length", slider=True)
        col.prop(props, "neck_length", slider=True)
        col.separator()
        col.prop(props, "uparm_length", slider=True)
        col.prop(props, "loarm_length", slider=True)
        col.separator()
        col.prop(props, "thigh_length", slider=True)
        col.prop(props, "calf_length", slider=True)

        box = layout.box()
        box.label(text="Asymmetry (Mutations)", icon='MOD_MIRROR')
        col = box.column(align=True)
        col.prop(props, "l_arm_scale")
        col.prop(props, "r_arm_scale")
        col.separator()
        col.prop(props, "l_leg_scale")
        col.prop(props, "r_leg_scale")

        box = layout.box()
        box.label(text="Structural Scales", icon='MESH_DATA')
        col = box.column(align=True)
        col.prop(props, "head_size", slider=True)
        col.prop(props, "hand_size", slider=True)
        col.prop(props, "foot_size", slider=True)
        col.prop(props, "shoulder_width", slider=True)
        col.prop(props, "pelvis_width", slider=True)

        box = layout.box()
        box.label(text="Muscle / Thickness", icon='MOD_THICKNESS')
        col = box.column(align=True)
        col.prop(props, "torso_thick", slider=True)
        col.prop(props, "neck_thick", slider=True)
        col.prop(props, "arm_thick", slider=True)
        col.prop(props, "leg_thick", slider=True)

        layout.separator()
        box = layout.box()
        box.label(text="Export & Save", icon='EXPORT')
        col = box.column(align=True)
        col.operator(OBJECT_OT_ExportSTL.bl_idname, icon='MESH_CUBE')
        col.operator(OBJECT_OT_ExportGLB.bl_idname, icon='WORLD')
        col.operator(OBJECT_OT_ExportCode.bl_idname, icon='COPYDOWN')

classes = (TrophyProperties, OBJECT_OT_GenerateTrophy, OBJECT_OT_ExportSTL, OBJECT_OT_ExportGLB, OBJECT_OT_ExportCode, VIEW3D_PT_TrophyMaker)

def register():
    for cls in classes: bpy.utils.register_class(cls)
    bpy.types.Scene.trophy_props = bpy.props.PointerProperty(type=TrophyProperties)

def unregister():
    for cls in reversed(classes): bpy.utils.unregister_class(cls)
    del bpy.types.Scene.trophy_props

if __name__ == "__main__": register()