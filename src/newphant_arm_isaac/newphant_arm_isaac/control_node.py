#!/usr/bin/env python3
import rclpy 
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float32MultiArray
import numpy as np


def r(x):
    return float(np.round(x, 5)) 

class control_node(Node):
    def __init__(self):
        super().__init__("control_node")
        self.joint_states = self.create_subscription(
            JointState,"/joint_states",self.joint_state_callBack,10)
        self.input_joint_states = self.create_subscription(
            Float32MultiArray,'/newphant_arm/raw_angles',self.publish_input,10)
        self.cmd_joint_states = self.create_publisher(
            JointState,"/joint_command",10)
        # self.create_timer(0.1,self.send_dummy_msg)


    @staticmethod
    def compute_mimic_joints(rev1):
        joints = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]

        # Revolute_1_0 (input)
        joints[4] = -r(rev1)

        # Revolute_2_0 = -0.52 * R1
        joints[0] = -r(-0.52 * joints[4])

        # Revolute_3_0 = -1.0 * R2
        joints[1] = -r(-1.0 * joints[0])

        # Revolute_4_0 = 1.0 * R3
        joints[2] = -r(1.0 * joints[1])
        # Revolute_5_0 = -1.0 * R2 - 2π
        joints[3] = -r(-1.0 * joints[0] )

        # Revolute_7_0 = -1.0 * R2 + 2π
        joints[5] = -r(-1.0 * joints[0] )

        # Revolute_9_0 = -1.0 * R3 + 2π
        joints[6] = -r(-1.0 * joints[1])

        return joints

    def joint_state_callBack(self,msg:JointState):
        self.get_logger().info(f"shoulder_baselink: {msg.position[0]}\nsArm_shoulder: {msg.position[1]}\nelbow_shoulder: {msg.position[2]}\nwrist_elbow: {msg.position[3]}\nwrist_roll: {msg.position[4]}")
    
    def slider_print(self,msg:Float32MultiArray):
        msg_ = msg.data[:-1]
        rev1 = msg.data[-1]
        gripper_list = self.compute_mimic_joints(rev1)
        self.get_logger().info(str(list(msg_)+gripper_list))
        
    def publish_input(self, msg:Float32MultiArray):
        msg_ = list(msg.data[:-1])
        msg_[2] = -msg_[2]
        rev1 = msg.data[-1]
        gripper_list = self.compute_mimic_joints(rev1)
        msg_to_publish = JointState()
        msg_to_publish.name = ['shoulder_baselink_0',
                    'sArm_shoulder_0',
                    'shoulder_elbow_0',
                    'wrist_elbow_0',
                    'wrist_roll_0',
                    'Revolute_2_0',
                    'Revolute_3_0',
                    'Revolute_4_0',
                    'Revolute_5_0',
                    'Revolute_1_0',
                    'Revolute_9_0',
                    'Revolute_7_0']
        msg_to_publish.position = msg_+gripper_list

        self.cmd_joint_states.publish(msg_to_publish)
    
    
    # def send_dummy_msg(self):
    #     msg = JointState()
    #     msg.position = [
    #                 1.57, 
    #                 1.57,
    #                 0.0041,
    #                 -0.0046,
    #                 -0.003,
    #                 0.0015,
    #                 0.0039,
    #                 -0.0506,
    #                 -0.0589,
    #                 -0.0059,
    #                 -0.0197,
    #                 0.0001]
        
    #     self.cmd_joint_states.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = control_node()
    rclpy.spin(node)
    rclpy.shutdown()


'''
name=[
    'shoulder_baselink_0',
    'sArm_shoulder_0',
    'shoulder_elbow_0',
    'wrist_elbow_0',
    'wrist_roll_0',
    'Revolute_2_0',
    'Revolute_3_0',
    'Revolute_4_0',
    'Revolute_5_0',
    'Revolute_1_0',
    'Revolute_9_0',
    'Revolute_7_0'],
    position=[
    0.0107, 
    0.0042,
    0.0041,
    -0.0046,
    -0.003,
    0.0015,
    0.0039,
    -0.0506,
    -0.0589,
    -0.0059,
    -0.0197,
    0.0001],
    velocity=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], effort=[-2.0507, 0.0026, -0.5014, -0.0243, -0.5649, 0.0972, -0.156, 0.1745, 0.2295, 1.9163, 0.0655, -0.0823]


'''