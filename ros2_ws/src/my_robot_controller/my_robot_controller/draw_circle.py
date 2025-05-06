#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CircleNode(Node):

    def __init__(self):
        super().__init__("draw_circle_node")
        self.get_logger().info("Draw circle started")
        self.cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.5, self.send_vel)

    def send_vel(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        self.cmd_vel_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = CircleNode()
    rclpy.spin(node)
    rclpy.shutdown()