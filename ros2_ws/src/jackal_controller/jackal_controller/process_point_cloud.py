#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import time 

class PointCloudNode(Node):
    
    def __init__(self):
        super().__init__("point_cloud_process_node")
        self.get_logger().info("starting point cloud processing")
        self.point_cloud_sub = self.create_subscription(PointCloud2,
                                                        "/ouster/points",
                                                        self.process_point_cloud_callback,
                                                        10)
        # self.downsample_point_pub = self.create_publisher(PointCloud2,"/ouster/points",10)
        self.idx = 0 
        
    def process_point_cloud_callback(self, msg: PointCloud2):
        # self.get_logger().info(f"Recieved point cloud msg {str(msg)}")
        self.get_logger().info(f"started processing with idx {self.idx}")
        # do some processing. ex downsampling 
        time.sleep(4)
        self.idx += 1
        # create a service that responds with point cloud 
        self.get_logger().info(f"finished processesing with idx: {self.idx}")

    


def main(args=None):
    rclpy.init()
    node = PointCloudNode()
    rclpy.spin(node)
    rclpy.shutdown()