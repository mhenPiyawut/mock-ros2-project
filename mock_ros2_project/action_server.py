#!/usr/bin/env python3
"""
ROS2 Action Server Example

This node demonstrates how to create an action server that provides
a Fibonacci sequence generation action.
"""

import time
from typing import Optional

import rclpy
from rclpy.action import ActionServer, GoalResponse
from rclpy.action.server import ServerGoalHandle
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class ActionServerNode(Node):
    """Action server node that generates Fibonacci sequences."""
    
    def __init__(self) -> None:
        """Initialize the action server node."""
        super().__init__('action_server')
        
        # Create action server
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )
        
        self.get_logger().info('Action server ready to generate Fibonacci sequences.')

    def execute_callback(self, goal_handle: ServerGoalHandle) -> Fibonacci.Result:
        """Execute callback for the Fibonacci action.
        
        Args:
            goal_handle: Handle for the goal being processed
            
        Returns:
            Fibonacci.Result: The complete Fibonacci sequence
        """
        self.get_logger().info('Executing goal...')
        
        # Validate the goal
        if goal_handle.request.order <= 0:
            self.get_logger().error('Order must be positive')
            goal_handle.abort()
            return Fibonacci.Result()
        
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]
        
        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()
            
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1]
            )
            
            self.get_logger().info(f'Feedback: {feedback_msg.partial_sequence}')
            goal_handle.publish_feedback(feedback_msg)
            
            time.sleep(1)  # Simulate work
        
        goal_handle.succeed()
        
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        
        return result


def main(args=None) -> None:
    """Main function to run the action server.
    
    Args:
        args: Command line arguments (optional)
    """
    rclpy.init(args=args)
    
    action_server_node = ActionServerNode()
    
    try:
        rclpy.spin(action_server_node)
    except KeyboardInterrupt:
        pass
    finally:
        action_server_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
