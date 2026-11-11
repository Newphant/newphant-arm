#!/usr/bin/env python3
import rclpy 
from rclpy.node import Node
from sensor_msgs.msg import JointState

class test_node(Node):
    def __init__(self):
        super().__init__("test_node")
        self.joint_states = self.create_subscription(
            JointState,"/joint_states",self.joint_state_callBack,10)
        

    def joint_state_callBack(self,msg:JointState):
        # self.get_logger().info(str(msg))
        self.get_logger().info(f"Shoulder_Link: {msg.position[0]}")
        
        

def main(args=None):
    rclpy.init(args=args)
    node = test_node()
    rclpy.spin(node)
    rclpy.shutdown()

