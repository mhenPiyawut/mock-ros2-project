#!/usr/bin/env python3
"""
ROS2 Service Client Example

This node demonstrates how to create a service client that calls
the AddTwoInts service.
"""

import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class ServiceClient(Node):
    """Service client node that calls addition service."""
    
    def __init__(self):
        super().__init__('service_client')
        
        # Create client
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        
        # Wait for service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        """Send a request to the service."""
        self.req.a = a
        self.req.b = b
        
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        
        return self.future.result()


def main(args=None):
    """Main function to run the service client."""
    rclpy.init(args=args)
    
    service_client = ServiceClient()
    
    # Use command line arguments or default values
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 41
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    response = service_client.send_request(a, b)
    
    service_client.get_logger().info(
        f'Result of add_two_ints: {a} + {b} = {response.sum}'
    )
    
    service_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
