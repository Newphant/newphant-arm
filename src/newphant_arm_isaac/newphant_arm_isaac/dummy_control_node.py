#!/usr/bin/env python3
import rclpy 
from rclpy.node import Node
from sensor_msgs.msg import JointState

class test_node(Node):
    def __init__(self):
        super().__init__("dummy_node")
        self.joint_states = self.create_subscription(
            JointState,"/joint_states",self.joint_state_callBack,10)
        self.cmd_joint_states = self.create_publisher(
            JointState,"/joint_command",10)
        
        self.create_timer(0.1,self.send_dummy_msg)

    def joint_state_callBack(self,msg:JointState):
        # self.get_logger().info(str(msg))
        self.get_logger().info(f"Positions: {msg.position}")
        
    def send_dummy_msg(self):
        msg = JointState()
        msg.name = ['shoulder_baselink_0',
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
        msg.position = [
                    1.57, 
                    1.57,
                    0.0041,
                    -0.0046,
                    -0.003,
                    0.0015,
                    0.0039,
                    -0.0506,
                    -0.0589,
                    -0.0059,
                    -0.0197,
                    0.0001]
        
        self.cmd_joint_states.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = test_node()
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