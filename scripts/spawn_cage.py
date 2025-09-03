#
"""Launch Isaac Sim Simulator first."""


import argparse
from isaaclab.app import AppLauncher

# create argparser
parser = argparse.ArgumentParser(description="Food Cage Scene Design")
# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()
# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""

import isaacsim.core.utils.prims as prim_utils

import isaaclab.sim as sim_utils
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR

from pxr import Usd, UsdGeom, UsdShade, UsdLux, UsdPhysics, Gf, Sdf, PhysxSchema
import omni.usd

def design_scene():
    """Designs the scene by spawning ground plane, light, objects and meshes from usd files."""
    
    stage = omni.usd.get_context().get_stage()
    
    # Ground-plane
    cfg_ground = sim_utils.GroundPlaneCfg()
    cfg_ground.func("/World/defaultGroundPlane", cfg_ground)

    # spawn distant light
    cfg_light_distant = sim_utils.DistantLightCfg(
        intensity=5000.0,
        color=(0.80, 0.80, 0.80),
    )
    cfg_light_distant.func("/World/lightDistant", cfg_light_distant, translation=(1, 0, 10))
    
    #Dome Light
    dome = UsdLux.DomeLight.Define(stage, Sdf.Path("/World/LightDome"))
    dome.CreateIntensityAttr(5000.0)
    dome.CreateColorAttr(Gf.Vec3f(1.0, 1.0, 1.0))

    # Thor Table - Static Base No Collision Not movable
    cfg = sim_utils.UsdFileCfg(usd_path=f"../usd_assets/cage/thor_table.usd")
    cfg.func("/World/Objects/Table", cfg, translation=(0.0, 0.0, 0.792))
    
    table_prim = stage.GetPrimAtPath("/World/Objects/Table")   
    looks_path = Sdf.Path("/World/Looks")
    if not stage.GetPrimAtPath(looks_path):
        stage.DefinePrim(looks_path, "Scope")

    mat_path = Sdf.Path("/World/Looks/Aluminum")
    mat = UsdShade.Material.Define(stage, mat_path)
    shader = UsdShade.Shader.Define(stage, mat_path.AppendPath("PreviewSurface"))
    shader.CreateIdAttr("UsdPreviewSurface")
    # UsdShade.CreateInput requires Sdf.ValueTypeName, not AttributeType
    shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(1.0)
    shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.25)
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.85, 0.85, 0.85))
    # Connect the material surface output to the shader's surface output
    shader_surface_output = shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)
    mat_surface_output = mat.CreateSurfaceOutput()
    mat_surface_output.ConnectToSource(shader_surface_output)
    UsdShade.MaterialBindingAPI(table_prim).Bind(mat)

    # Deactivate specific unwanted subprims without modifying the source USD
    # 1) Explicit path provided by user
    mount_plate_path = Sdf.Path("/World/Objects/Table/Thor_table/Top/mount_plate")
    mount_plate_prim = stage.GetPrimAtPath(mount_plate_path)
    if mount_plate_prim and mount_plate_prim.IsValid():
        mount_plate_prim.SetActive(False)
    # 2) Fallback: also deactivate any 'mount' under 'Top' if structure changes slightly
    for prim in Usd.PrimRange(table_prim):
        path_lower = str(prim.GetPath()).lower()
        name_lower = prim.GetName().lower()
        if "/top/" in path_lower and "mount" in name_lower:
            prim.SetActive(False)


def main():
    """Main function."""

    # Initialize the simulation context
    sim_cfg = sim_utils.SimulationCfg(dt=0.01, device=args_cli.device)
    sim = sim_utils.SimulationContext(sim_cfg)
    # Set main camera
    sim.set_camera_view([-0.05, 0.0, 2.5], [-0.5, 0.0, 0.5])
    # Design scene
    design_scene()
    # Play the simulator
    sim.reset()
    # Now we are ready!
    print("[INFO]: Setup complete...")

    # Simulate physics
    while simulation_app.is_running():
        # perform step
        sim.step()


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
