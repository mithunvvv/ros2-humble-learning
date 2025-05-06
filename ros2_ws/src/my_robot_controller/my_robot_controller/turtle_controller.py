#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute
from functools import partial


class TurtleContNode(Node):

    def __init__(self):
        super().__init__("turtle_controller_node")
        # 2nd arg is the name of the topic 
        self.cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10 )
        self.pose_sub = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)

    def pose_callback(self, pose: Pose):
        cmd = Twist()
        if pose.x > 9.0:
            cmd.linear.x = 1.0
            cmd.angular.z = 0.9
        self.cmd_vel_pub.publish(cmd)

        if pose.x > 5.5:
            self.call_set_pen_service()

    def call_set_pen_service(self):
        client = self.create_client(TeleportAbsolute, "/turtle1/teleport_absolute" ) # service type and name
        while not client.wait_for_service(1.0):
            self.get_logger().info("waiting for service to start")

        request = TeleportAbsolute.Request()
        request.theta = 6.0
        request.x = 1.0
        request.y = 2.0

        future = client.call_async(request) # non blocking (can be issue in case where you have multiple threads)

        future.add_done_callback(partial(self.callnack_set_pen))

        # add_done_callback used with async methods like call_async, registers a function to be called when the async tasks complete 

    def callnack_set_pen(self, future):
        try:
            response = future.result()
        except Exception as e:
            pass



def main(args=None):
    rclpy.init(args=args)
    node = TurtleContNode()
    rclpy.spin(node)
    rclpy.shutdown()