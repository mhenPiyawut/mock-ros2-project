#!/usr/bin/env python3
"""
ROS2 Action Client Example

This node demonstrates how to create an action client that calls
the Fibonacci action and handles feedback.
"""

import sys
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class ActionClientNode(Node):
    """Action client node that requests Fibonacci sequences."""
    
    def __init__(self):
        super().__init__('action_client')
        
        # Create action client
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        """Send a goal to the action server."""
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        
        self._action_client.wait_for_server()
        
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Handle goal response from action server."""
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return
        
        self.get_logger().info('Goal accepted :)')
        
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """Handle result from action server."""
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        """Handle feedback from action server."""
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback.partial_sequence}')


def main(args=None):
    """Main function to run the action client."""
    rclpy.init(args=args)
    
    action_client = ActionClientNode()
    
    # Use command line argument or default value
    order = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    
    action_client.send_goal(order)
    
    try:
        rclpy.spin(action_client)
    except KeyboardInterrupt:
        pass
    finally:
        action_client.destroy_node()


if __name__ == '__main__':
    main()
