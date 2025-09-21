#!/usr/bin/env python3
"""
ROS2 Service Client Example

This node demonstrates how to create a service client that calls
the AddTwoInts service.
"""

import sys
from typing import Optional

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class ServiceClient(Node):
    """Service client node that calls addition service.
    
    This node creates a service client that sends requests to the
    AddTwoInts service and handles the responses.
    """
    
    def __init__(self) -> None:
        """Initialize the service client node."""
        super().__init__('service_client')
        
        # Create client for the AddTwoInts service
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        
        # Wait for service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        
        self.req = AddTwoInts.Request()

    def send_request(self, a: int, b: int) -> Optional[AddTwoInts.Response]:
        """Send a request to the service.
        
        Args:
            a: First integer to add
            b: Second integer to add
            
        Returns:
            Optional[AddTwoInts.Response]: Service response or None if failed
        """
        self.req.a = a
        self.req.b = b
        
        self.get_logger().info(f'Sending request: {a} + {b}')
        
        try:
            self.future = self.cli.call_async(self.req)
            rclpy.spin_until_future_complete(self, self.future)
            
            if self.future.result() is not None:
                return self.future.result()
            else:
                self.get_logger().error('Service call failed')
                return None
        except Exception as e:
            self.get_logger().error(f'Error calling service: {e}')
            return None


def main(args=None) -> None:
    """Main function to run the service client.
    
    Args:
        args: Command line arguments (optional)
    """
    rclpy.init(args=args)
    
    service_client_node = ServiceClient()
    
    try:
        # Use command line arguments or default values with validation
        if len(sys.argv) > 1:
            try:
                a = int(sys.argv[1])
            except ValueError:
                service_client_node.get_logger().error('Invalid value for first argument. Please provide an integer.')
                return
        else:
            a = 41  # Default value
        
        if len(sys.argv) > 2:
            try:
                b = int(sys.argv[2])
            except ValueError:
                service_client_node.get_logger().error('Invalid value for second argument. Please provide an integer.')
                return
        else:
            b = 1  # Default value
        
        response = service_client_node.send_request(a, b)
        
        if response is not None:
            service_client_node.get_logger().info(
                f'Result of add_two_ints: {a} + {b} = {response.sum}'
            )
        else:
            service_client_node.get_logger().error('Failed to get response from service')
    
    except KeyboardInterrupt:
        service_client_node.get_logger().info('Service client interrupted by user')
    except Exception as e:
        service_client_node.get_logger().error(f'Unexpected error: {e}')
    finally:
        service_client_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
