# Mechanism simulation

Use the smallest model that answers the requested motion question. Show one useful sweep or response early, then add detail only where it changes the answer. A simulation task does not require a general audit or assembly/disassembly walkthrough.

## Pick the right evidence

- **Prescribed animation:** poses or joint coordinates are assigned over time. Useful for explaining intended travel; it does not prove that a connected mechanism can achieve it.
- **Solved kinematics:** grounded bodies and joint constraints determine dependent motion from the chosen input. Useful for degrees of freedom, linkage closure and travel.
- **Dynamics:** motion follows from actuation, mass/inertia, external forces and modeled contacts. Useful for load response, controls and contact behavior under stated assumptions.

Label the result accordingly. Never rename a scripted pose sweep as solver-validated or physically validated motion.

## FreeCAD Assembly: constraints and driven motion

Verify the installed FreeCAD version, Assembly workbench, solver and available driving/simulation commands. The [official Assembly documentation](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Assembly_Workbench.md) describes grounding and joint types; [Create Simulation](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Assembly_CreateSimulation.md) is documented for version 1.1. Earlier successful STEP import is not evidence that this feature is present. Check current commands rather than copying an API from another version.

1. Import or link revision-matched CAD bodies with explicit units and stable joint frames. Ground the intended base/reference body.
2. Connect rigid groups with fixed joints; use revolute, slider or other joints only for real relative motion. Check axes, attachment locations and intended degrees of freedom. Avoid redundant constraints and accidentally grounding moving links.
3. Solve the static assembly, then drive the intended independent input with a supported joint motion. Let the solver determine dependent bodies; do not directly assign every body's pose and call it a solved mechanism.
4. Generate a short sweep. Check solver failures, branch flips, detached parts and joint closure at representative positions. Inspect relevant CAD interference separately; a joint solve does not guarantee collision-free travel.
5. Save the native assembly and joint definitions, drive settings and a short result/limit note. When a driven solver is unavailable, report that gap and label any fallback as prescribed animation.

## MuJoCo: physics when required

Use a model tied to the CAD revision, with consistent units and coordinate transforms. The [official modeling guide](https://mujoco.readthedocs.io/en/stable/modeling.html) and [simulation guide](https://mujoco.readthedocs.io/en/stable/programming/simulation.html) are the implementation references.

Define bodies and joint axes/limits, positive mass and valid inertia, actuator/control behavior, gravity, damping/friction and relevant contacts. Separate visual meshes from collision approximations; record simplifications. Map closed-loop mechanisms explicitly using suitable constraints rather than silently cutting the loop. Match actuator effort/speed limits to evidence when making load claims; an ideal position command is not a real servo qualification.

Compile the model and run a short controlled input first. Inspect warnings, finite states, constraint error, contact behavior and the requested output. Check time-step sensitivity or uncertain friction/inertia only when it affects the conclusion. If positions are overwritten each frame, describe the result as a pose demonstration rather than force-driven dynamics.

## Lightweight handoff

Provide the model/native assembly, input or control settings, source revision, tool version and useful playback or result plot. State what was prescribed, solved or measured and which material, actuator, contact or load assumptions remain provisional. Solver convergence does not establish strength, fatigue, physical fit, real actuator capacity or safe hardware operation. Physical testing remains a separate authorized step.
