# FoodCage — Isaac Lab + Isaac Sim Bimanual Manipulation

This repository contains an Isaac Lab external project plus a small USD asset stack for a bimanual food-manipulation cage. It supports:
- Isaac Sim scene composition (cage, camera+light, robot placeholder)
- Quick reach testing of the YAM arm
- Baseline RL training scripts (RSL-RL and skrl)

## Repository layout
- `source/FoodCage/`: Isaac Lab external project package
  - `FoodCage/tasks/manager_based/foodcage/`: env config, MDP glue, agent configs
- `usd_assets/`: lightweight placeholder USDs you can replace with your own
  - `robots/yam_arm.usd`: placeholder prim `YamArm`
  - `cage/cage.usd`: placeholder prim `FoodCage`
  - `scenes/cam_light.usd`: simple camera and distant light
- `scripts/`: utilities and training/playing entry points

## Prerequisites
- Windows with recent NVIDIA GPU drivers
- Isaac Sim installed (version matching your local environment)
- Python matching Isaac Sim’s Python (commonly 3.10 for recent releases)



### RSL-RL
- Train
```powershell
python .\scripts\rsl_rl\train.py
```
- Play/evaluate
```powershell
python .\scripts\rsl_rl\play.py
```

### skrl
- Train
```powershell
python .\scripts\skrl\train.py
```
- Play/evaluate
```powershell
python .\scripts\skrl\play.py
```

## Notes
- The placeholder USDs define simple `Xform` prims and a basic scene. They are safe to commit.
- When you drop in real assets, verify scene composition works by opening in Isaac Sim or by running the reach check script.

## Acknowledgements
- Built on Isaac Sim and Isaac Lab.
