import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math


#===================================================================
class MoverAgente(Node):
    #---------------------------------------------------------------
    def __init__(self):
        super().__init__('mover_agente')
        # Sin la barra '/' inicial para que sea relativo al namespace
        self.ns = self.get_namespace().strip('/') 
        try:
            # Extrae el número del nombre (ej: 'carro2' -> 2)
            index = int(''.join(filter(str.isdigit, self.ns)))
            self.y = float(index - 1) * 1.5
        except (ValueError, IndexError):
            self.y = 0.0

        self.x = 0.0
        self.theta = 0.0
        self.t = 0.0
        self.pub = self.create_publisher(JointState, 'joint_states', 10)  # QoS history depth, guarda 10 mensajes antes de descartar--
        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.05,self.mover)
       
        # Obtenemos el nombre del carro (carro1, carro2...)
        
        # Los nombres deben coincidir EXACTAMENTE con el prefijo del launch
        self.joint_names = [
            f'{self.ns}/left_wheel_joint_a',
            f'{self.ns}/left_wheel_joint_p', 
            f'{self.ns}/right_wheel_joint_a',
            f'{self.ns}/right_wheel_joint_p'
        ]   
    #-----------------------------------------------------------
    def mover(self):
        velocidad = 0.2
        dt = 0.05
        self.x += velocidad * math.cos(self.theta) * dt
        self.y += velocidad * math.sin(self.theta) * dt
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'
        t.child_frame_id = f'{self.ns}/base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.w = 1.0
        self.tf_broadcaster.sendTransform(t)
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        self.t += 0.1
        val = math.sin(self.t)
        msg.position = [val, val, val, val]
        self.pub.publish(msg) 


#==============================================================
def main(args=None):
    rclpy.init()
    node = MoverAgente()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
#-------------------------------------------------------------

if __name__ == '__main__':
    main()