#!/usr/bin/env python3
"""
ROS2 Publisher Node Example

This node demonstrates how to create a simple publisher that sends
string messages at regular intervals.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PublisherNode(Node):
    """Simple publisher node that publishes string messages."""
    
    def __init__(self):
        super().__init__('publisher_node')
        
        # Create publisher
        self.publisher_ = self.create_publisher(String, 'send_topic', 10)
        
        # Create timer to publish messages periodically
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        # Initialize counter
        self.i = 0
        
        self.get_logger().info('Publisher node has been started.')

    def timer_callback(self):
        """Timer callback function that publishes messages."""
        msg = String()
        msg.data = f'Hello World: {self.i}'
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        
        self.i += 1


def main(args=None):
    """Main function to run the publisher node."""
    rclpy.init(args=args)
    
    publisher_node = PublisherNode()
    
    try:
        rclpy.spin(publisher_node)
    except KeyboardInterrupt:
        pass
    finally:
        publisher_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
