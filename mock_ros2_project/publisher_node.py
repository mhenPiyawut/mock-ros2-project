#!/usr/bin/env python3
"""
ROS2 Publisher Node Example

This node demonstrates how to create a simple publisher that sends
string messages at regular intervals to demonstrate basic pub/sub communication.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PublisherNode(Node):
    """Simple publisher node that publishes string messages.
    
    This node creates a publisher that sends string messages containing
    a counter value at regular intervals.
    """
    
    def __init__(self) -> None:
        """Initialize the publisher node."""
        super().__init__('publisher_node')
        
        # Create publisher for string messages
        self.publisher_ = self.create_publisher(String, 'send_topic', 10)
        
        # Create timer to publish messages periodically
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        # Initialize message counter
        self.i = 0
        
        self.get_logger().info('Publisher node has been started.')

    def timer_callback(self) -> None:
        """Timer callback function that publishes messages.
        
        Creates and publishes a string message with an incrementing counter.
        """
        msg = String()
        msg.data = f'Hello World: {self.i}'
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        
        self.i += 1


def main(args=None) -> None:
    """Main function to run the publisher node.
    
    Args:
        args: Command line arguments (optional)
    """
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
