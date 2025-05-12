#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy 



# topic info /vtr/mpc_prediction 
#  /jackal_velocity_controller/cmd_vel_unstamped 
# /j100_0365/joy_teleop/joy
#  what msg do I need to publish and to what topic


class MPCActionNode(Node):

    def __init__(self):
        super().__init__("mpc_action_node")
        self.get_logger().info("MPC Action Node started")
        self.mpc_action_sub = self.create_subscription(Path, "/vtr/mpc_prediction", self.mpc_action_callback, 10)
        self.cmd_pub = self.create_publisher(Twist,"/jackal_velocity_controller/cmd_vel_unstamped ", 10)
        self.teleop_sub = self.create_subscription(Joy, "/j100_0365/joy_teleop/joy", self.teleop_sub_callback, 10)

        self.start_pressed = False
        self.stop_pressed = False

    def mpc_action_callback(self, msg: Path):
        if not self.start_pressed and not self.stop_pressed:
            twist_command = Twist()
            twist_command.linear.x = msg.linear.x
            twist_command.linear.y = msg.linear.y
            twist_command.angular.z = msg.angular.z 
            self.get_logger().debug("Updated MPC command")
        if self.stop_pressed:
            twist_command = Twist()
            twist_command.linear.x = 0
            twist_command.linear.y = 0
            twist_command.angular.z = 0
            self.get_logger().debug("Updated MPC command")

        self.cmd_pub.publish(twist_command)
        self.get_logger().info("Published MPC command")


    def teleop_sub_callback(self, msg: Joy):
        stop_buttton_idx = 3
        if msg.button[stop_buttton_idx] == 1:
            self.stop_pressed = True
        else:
            self.stop_pressed = False
            
        if self.start_pressed or self.stop_pressed:
            self.get_logger().info("Joystick override active — suppressing MPC")



def main(args=None):
    rclpy.init(args=args)
    node = MPCActionNode()
    rclpy.spin(node)
    rclpy.shutdown()
        