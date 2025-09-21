#!/usr/bin/env python3
"""
ROS2 Service Server Example

This node demonstrates how to create a service server that provides
an addition service using the AddTwoInts service type.
"""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class ServiceServer(Node):
    """Service server node that provides addition service.
    
    This node creates a service server that accepts two integers
    and returns their sum using the AddTwoInts service interface.
    """
    
    def __init__(self) -> None:
        """Initialize the service server node."""
        super().__init__('service_server')
        
        # Create service for adding two integers
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_two_ints_callback
        )
        
        self.get_logger().info('Service server ready to add two integers.')

    def add_two_ints_callback(self, request: AddTwoInts.Request, 
                             response: AddTwoInts.Response) -> AddTwoInts.Response:
        """Service callback that adds two integers.
        
        Args:
            request: Service request containing two integers (a and b)
            response: Service response to populate with the sum
            
        Returns:
            AddTwoInts.Response: Response containing the sum of the two integers
        """
        response.sum = request.a + request.b
        
        self.get_logger().info(
            f'Incoming request: a={request.a}, b={request.b}, '
            f'sending back response: sum={response.sum}'
        )
        
        return response


def main(args=None) -> None:
    """Main function to run the service server.
    
    Args:
        args: Command line arguments (optional)
    """
    rclpy.init(args=args)
    
    service_server_node = ServiceServer()
    
    try:
        rclpy.spin(service_server_node)
    except KeyboardInterrupt:
        pass
    finally:
        service_server_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
