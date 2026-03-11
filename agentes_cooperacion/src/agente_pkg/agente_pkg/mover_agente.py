import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class MoverAgente(Node):
    def __init__(self):
        super().__init__('mover_agente')
        # Sin la barra '/' inicial para que sea relativo al namespace
        self.pub = self.create_publisher(JointState, 'joint_states', 10)
        
        # Obtenemos el nombre del carro (carro1, carro2...)
        self.ns = self.get_namespace().strip('/')
        
        # Los nombres deben coincidir EXACTAMENTE con el prefijo del launch
        self.joint_names = [
            f'{self.ns}/left_wheel_joint_a',
            f'{self.ns}/left_wheel_joint_p', 
            f'{self.ns}/right_wheel_joint_a',
            f'{self.ns}/right_wheel_joint_p'
        ]

        self.t = 0.0
        self.timer = self.create_timer(0.02, self.mover)
        
    def mover(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        val = math.sin(self.t)
        msg.position = [val, val, val, val]
        self.pub.publish(msg)
        self.t += 0.1

def main(args=None):
    rclpy.init(args=args)
    node = MoverAgente()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()