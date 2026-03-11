import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class MoverAgente(Node):
    def __init__(self):
        super().__init__('mover_agente')
        self.pub = self.create_publisher(JointState, '/joint_states', 10)

        self.joint_names = ['left_wheel_joint_a','left_wheel_joint_p', 'right_wheel_joint_a','right_wheel_joint_p']  # azul, rojo, verde

        # Amplitudes máximas (rad)
        self.amplitudes = [math.pi/4, math.pi/6, math.pi/6]  # último para inclinación

        # Velocidades (rad/s)
        self.t = 0.0
        self.timer = self.create_timer(0.02, self.mover)
        
    def mover(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        left = math.sin(self.t)
        right = math.sin(self.t)
        msg.position = [left, left, right, right]
        self.pub.publish(msg)
        self.t +=0.1

def main(args=None):
    rclpy.init(args=args)
    node = MoverAgente()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
 
if __name__ == '__main__':
    main()
