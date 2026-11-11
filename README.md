# newphant-arm

6-DOF 3D-printed arm (Feetech STS3215 servos) with URDF/USD assets, CAD parts and a
ROS 2 Humble control package for Isaac Sim and real hardware.

## Layout

| Path | Contents |
|---|---|
| `src/newphant_arm_isaac/` | ROS 2 ament_python package: slider GUI, joint-command bridge, diagnostics |
| `assets/urdf/main_arm/` | URDF and STL meshes |
| `assets/usd/` | Isaac Sim scene and Action Graph screenshot |
| `cad/` | STEP files for every printed part |

## Build

```bash
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

## Run

```bash
ros2 run newphant_arm_isaac control_node
ros2 run newphant_arm_isaac slider_node
```

Topics: `/newphant_arm/raw_angles` (slider output), `/joint_command` (targets),
`/joint_states` (state). Open `assets/usd/NewPhant_arm_usd.usd` in Isaac Sim and
press play before starting the nodes.
