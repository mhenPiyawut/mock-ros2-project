#!/usr/bin/env python3
"""
ROS2 Subscriber Node Example

This node demonstrates how to create a simple subscriber that listens
to string messages and processes them.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SubscriberNode(Node):
    """Simple subscriber node that listens to string messages."""
    
    def __init__(self):
        super().__init__('subscriber_node')
        
        # Create subscription
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        
        self.get_logger().info('Subscriber node has been started.')

    def listener_callback(self, msg):
        """Callback function that processes received messages."""
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    """Main function to run the subscriber node."""
    rclpy.init(args=args)
    
    subscriber_node = SubscriberNode()
    
    try:
        rclpy.spin(subscriber_node)
    except KeyboardInterrupt:
        pass
    finally:
        subscriber_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
