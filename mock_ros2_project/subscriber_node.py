#!/usr/bin/env python3
"""
ROS2 Subscriber Node Example

This node demonstrates how to create a simple subscriber that listens
to string messages and processes them to show basic pub/sub communication.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SubscriberNode(Node):
    """Simple subscriber node that listens to string messages.
    
    This node creates a subscription to receive and process string messages
    from the 'send_topic' topic.
    """
    
    def __init__(self) -> None:
        """Initialize the subscriber node."""
        super().__init__('subscriber_node')
        
        # Create subscription to receive string messages
        self.subscription = self.create_subscription(
            String,
            'send_topic',  # Fixed: Match publisher topic name
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        
        self.get_logger().info('Subscriber node has been started.')

    def listener_callback(self, msg: String) -> None:
        """Callback function that processes received messages.
        
        Args:
            msg: The received String message
        """
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None) -> None:
    """Main function to run the subscriber node.
    
    Args:
        args: Command line arguments (optional)
    """
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
