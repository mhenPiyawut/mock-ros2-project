#!/usr/bin/env python3
"""
ROS2 Action Server Example

This node demonstrates how to create an action server that provides
a Fibonacci sequence generation action.
"""

import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class ActionServerNode(Node):
    """Action server node that generates Fibonacci sequences."""
    
    def __init__(self):
        super().__init__('action_server')
        
        # Create action server
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )
        
        self.get_logger().info('Action server ready to generate Fibonacci sequences.')

    def execute_callback(self, goal_handle):
        """Execute callback for the Fibonacci action."""
        self.get_logger().info('Executing goal...')
        
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]
        
        for i in range(1, goal_handle.request.order):
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


def main(args=None):
    """Main function to run the action server."""
    rclpy.init(args=args)
    
    action_server = ActionServerNode()
    
    try:
        rclpy.spin(action_server)
    except KeyboardInterrupt:
        pass
    finally:
        action_server.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
