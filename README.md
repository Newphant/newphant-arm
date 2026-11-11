# newphant-arm

A 6-DOF, fully 3D-printable robot arm for physical-AI experiments: CAD, URDF, an
Isaac Sim scene and a complete ROS 2 control stack.

The arm is driven by six Feetech STS3215 serial-bus servos (30 kg·cm stall torque,
magnetic encoder) and uses a parallel four-bar linkage for the gripper. Five joints
position the arm, the sixth drives the gripper; the linkage's seven dependent finger
joints are computed in software, so a single gripper command keeps the two fingers
synchronised.

## Hardware

| Item | Specification |
|---|---|
| Servos | 6 × Feetech STS3215 (30 kg·cm, 360° magnetic encoder, TTL serial bus) |
| Degrees of freedom | 5 arm joints + 1 gripper (four-bar linkage, 7 dependent joints) |
| Structure | PLA, FDM printed |
| Design tool | Autodesk Fusion 360 |
| Control | ROS 2 Humble, `ament_python` package |
| Simulation | NVIDIA Isaac Sim (USD stage + OmniGraph Action Graph) |

## Repository layout

| Path | Contents |
|---|---|
| `src/newphant_arm_isaac/` | ROS 2 package: slider GUI, joint-command bridge, diagnostics |
| `assets/urdf/main_arm/` | `main_arm.urdf` and STL meshes for every link |
| `assets/usd/` | Isaac Sim scene (`NewPhant_arm_usd.usd`) and Action Graph reference image |
| `cad/` | STEP files for all printed parts, including the gripper and servo reference model |

## Joint model

The URDF contains 21 links. The published `JointState` always has 12 entries, in this
order:

```
shoulder_baselink_0  sArm_shoulder_0  shoulder_elbow_0  wrist_elbow_0  wrist_roll_0
Revolute_2_0  Revolute_3_0  Revolute_4_0  Revolute_5_0  Revolute_1_0  Revolute_9_0  Revolute_7_0
```

* The first five are the arm joints.
* `Revolute_1_0` is the gripper input.
* `Revolute_2_0` … `Revolute_9_0` are linkage joints derived from the input
  (`Revolute_2_0 = 0.52 × Revolute_1_0`, with sign conventions per joint), so the
  fingers stay parallel and the four-bar stays closed.

The command bridge (`control_node.py`) performs this mapping; there is no separate
gripper controller.

## ROS 2 interface

| Topic | Type | Direction | Notes |
|---|---|---|---|
| `/newphant_arm/raw_angles` | `std_msgs/Float32MultiArray` | slider → bridge | 6 values: 5 arm angles + gripper, ~60 Hz |
| `/joint_command` | `sensor_msgs/JointState` | bridge → simulator / driver | 12 named positions |
| `/joint_states` | `sensor_msgs/JointState` | simulator / driver → bridge | feedback, logged by the bridge |

| Node | Executable | Behaviour |
|---|---|---|
| Command bridge | `control_node` | subscribes to raw angles, expands the 12-joint command, publishes `/joint_command`, logs `/joint_states` |
| Slider GUI | `slider_node` | Pygame window with six sliders, publishes raw angles at ~60 Hz |
| State monitor | `test_node` | logs the first joint position from `/joint_states` |
| Fixed-pose publisher | `dummy_control_node` | publishes a hard-coded 12-joint pose at 10 Hz, useful for wiring checks |

### Slider ranges

| Slider | Range (rad) |
|---|---|
| shoulder baselink | −1.57 … 1.57 |
| sArm shoulder | 0 … 3.14 |
| shoulder elbow | 0 … 3.14 |
| wrist elbow | 0 … 3.14 |
| wrist roll | −3.14 … 3.14 |
| gripper action | 0 … 1.57 |

## Build

```bash
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

The package lives directly under `src/`, so `colcon build` works from the repository
root. Python 3.10 and `pygame` (`pip install pygame`) are required for the slider GUI.

## Run

Terminal 1 — command bridge:

```bash
ros2 run newphant_arm_isaac control_node
```

Terminal 2 — slider GUI:

```bash
ros2 run newphant_arm_isaac slider_node
```

Quick wiring check without the GUI:

```bash
ros2 run newphant_arm_isaac dummy_control_node
ros2 topic echo /joint_states
```

## Isaac Sim

1. Open `assets/usd/NewPhant_arm_usd.usd`.
2. Press **Play** — the Action Graph only runs on playback ticks.
3. The graph subscribes to `/joint_command` (position targets), drives the articulated
   arm and publishes `/joint_states` back.
4. Start `control_node` and `slider_node` afterwards; the same topics drive the real arm.

If the arm does not move, check that the graph's ROS 2 nodes use the same topic names
as the package and that playback is running.

## Printing

All structural parts print on a standard FDM printer; no machined components are needed.

| Setting | Value |
|---|---|
| Material | PLA |
| Layer height | 0.2 mm |
| Infill | 15–20 % |
| Supports | Yes, for servo mounts and overhangs |

STEP files in `cad/` can be edited for custom mounts or extra cameras. The STL meshes
used by the URDF are in `assets/urdf/main_arm/asset/`.

## Real hardware

The same ROS 2 topics used in Isaac Sim apply to the physical arm: a serial-bus driver
publishes `/joint_states` and consumes `/joint_command`. Before running on hardware,
verify joint direction and zero offsets, keep the arm supported, and provide an
independent power cut-off.

## License

MIT. See [LICENSE](LICENSE).
