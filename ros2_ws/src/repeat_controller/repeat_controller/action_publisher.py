#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy 



# topic info /vtr/mpc_prediction 
#  /jackal_velocity_controller/cmd_vel_unstamped /j100_0365/platform/cmd_vel_unstamped
# /j100_0365/joy_teleop/joy
#  /j100_0365/joy_teleop/cmd_vel
#  what msg do I need to publish and to what topic


class MPCActionNode(Node):

    def __init__(self):
        super().__init__("mpc_action_node")
        self.get_logger().info("MPC Action Node started")
        self.mpc_action_sub = self.create_subscription(Twist, "/vtr/command", self.mpc_action_callback, 10)
        # self.mpc_action_sub = self.create_subscription(Twist, "/j100_0365/joy_teleop/cmd_vel", self.mpc_action_callback, 10)
        self.cmd_pub = self.create_publisher(Twist,"/j100_0365/platform/cmd_vel_unstamped", 10)
        self.teleop_sub = self.create_subscription(Joy, "/j100_0365/joy_teleop/joy", self.teleop_sub_callback, 10)
        self.twist_command = Twist()
        self.twist_command.linear.x = 0.0
        self.twist_command.linear.y = 0.0
        self.twist_command.angular.z = 0.0
        self.publish_action_timer = self.create_timer(0.01, self.publish_cmd)

        self.start_pressed = False
        self.stop_pressed = False

        
    def publish_cmd(self):
        self.cmd_pub.publish(self.twist_command)

    def mpc_action_callback(self, msg: Path):
        if self.start_pressed and not self.stop_pressed:
            self.twist_command.linear.x = msg.linear.x
            self.twist_command.linear.y = msg.linear.y
            self.twist_command.angular.z = msg.angular.z 
            self.get_logger().debug("Updated MPC command")
        if self.stop_pressed:
            self.twist_command.linear.x = 0.0
            self.twist_command.linear.y = 0.0
            self.twist_command.angular.z = 0.0
            self.get_logger().debug("Updated MPC command")


    def teleop_sub_callback(self, msg: Joy):
        stop_buttton_idx = 1 # red circle, ie stop 
        start_button_idx = 3
        if msg.buttons[stop_buttton_idx] == 1:
            self.stop_pressed = True
        else:
            self.stop_pressed = False

        if msg.buttons[start_button_idx] == 1:
            self.start_pressed = True

            
        if self.start_pressed or self.stop_pressed:
            self.get_logger().info("Joystick override active — suppressing MPC")



def main(args=None):
    rclpy.init(args=args)
    node = MPCActionNode()
    rclpy.spin(node)
    rclpy.shutdown()
        