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
        self.mpc_twist_command = Twist()
        self.action = Twist()
        self.mpc_twist_command.linear.x = 0.0
        self.mpc_twist_command.angular.z = 0.0
        self.publish_action_timer = self.create_timer(0.01, self.publish_cmd)

        self.start_pressed = False
        self.stop_pressed = False

        
    def publish_cmd(self):
        # publish commands based on condition of ps4 here
        # callback always reads in MPC action 
        # previosuly I had this always publishing and I had the condtional in the mpc action callback
        # why did that create an issue where even though i pressed stop, it wouldnt stop? ==> i think it because u recieve the MPC at some freq,
        #  by the time the aciton to be published is set, it will get published but then I press the stop button, 
        # it is too late at that point bc the publish cmd function was called with the mpc action instead of the zero action
        # now, the action that is published is defined by a diff variable and that variable only get set depending on the curr state of the buttons 
        # previously, the mpc twist command was the one being published 
        if self.start_pressed and not self.stop_pressed:
            self.action = self.mpc_twist_command
        else: 
            self.action.linear.x = 0.0
            self.action.angular.z = 0.0
        self.cmd_pub.publish(self.action)

    def mpc_action_callback(self, msg: Path):
        self.mpc_twist_command.linear.x = msg.linear.x
        self.mpc_twist_command.angular.z = msg.angular.z 
        self.get_logger().debug("Updated MPC command")



    def teleop_sub_callback(self, msg: Joy):
        stop_buttton_idx = 1 # red circle, ie stop 
        start_button_idx = 3
        if msg.buttons[stop_buttton_idx] == 1:
            self.stop_pressed = True
        else:
            self.stop_pressed = False

        if msg.buttons[start_button_idx] == 1: # this stays true for the entire duration
            self.start_pressed = True

            
        if self.start_pressed or self.stop_pressed:
            self.get_logger().info("Joystick override active — suppressing MPC")



def main(args=None):
    rclpy.init(args=args)
    node = MPCActionNode()
    rclpy.spin(node)
    rclpy.shutdown()
        