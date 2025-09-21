#!/usr/bin/env python3
"""
ROS2 Action Client Example

This node demonstrates how to create an action client that calls
the Fibonacci action and handles feedback.
"""

import sys
from typing import Optional

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class ActionClientNode(Node):
    """Action client node that requests Fibonacci sequences."""
    
    def __init__(self) -> None:
        """Initialize the action client node."""
        super().__init__('action_client')
        
        # Create action client for Fibonacci action
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order: int) -> None:
        """Send a goal to the action server.
        
        Args:
            order: The order of the Fibonacci sequence to generate
        """
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        
        if not self._action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Action server not available after waiting')
            return
        
        self.get_logger().info(f'Sending goal: order={order}')
        
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future) -> None:
        """Handle goal response from action server.
        
        Args:
            future: Future object containing the goal response
        """
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return
        
        self.get_logger().info('Goal accepted :)')
        
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future) -> None:
        """Handle result from action server.
        
        Args:
            future: Future object containing the action result
        """
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg) -> None:
        """Handle feedback from action server.
        
        Args:
            feedback_msg: Feedback message from the action server
        """
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback.partial_sequence}')


def main(args=None) -> None:
    """Main function to run the action client.
    
    Args:
        args: Command line arguments (optional)
    """
    rclpy.init(args=args)
    
    action_client_node = ActionClientNode()
    
    try:
        # Use command line argument or default value with validation
        if len(sys.argv) > 1:
            try:
                order = int(sys.argv[1])
                if order <= 0:
                    action_client_node.get_logger().error('Order must be a positive integer')
                    return
            except ValueError:
                action_client_node.get_logger().error('Invalid order value. Please provide an integer.')
                return
        else:
            order = 10  # Default value
        
        action_client_node.send_goal(order)
        
        rclpy.spin(action_client_node)
    except KeyboardInterrupt:
        action_client_node.get_logger().info('Action client interrupted by user')
    except Exception as e:
        action_client_node.get_logger().error(f'Unexpected error: {e}')
    finally:
        action_client_node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
