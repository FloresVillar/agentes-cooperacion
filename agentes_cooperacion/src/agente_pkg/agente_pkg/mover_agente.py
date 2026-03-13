import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist, TransformStamped
from tf2_ros import TransformBroadcaster
import math

class MoverAgente(Node):
    def __init__(self):
        super().__init__('mover_agente')
        self.ns = self.get_namespace().strip('/')             # Obtiene namespace (carro1, etc)
        
        # Estado del robot
        self.x = 0.0                                          # Posicion inicial X
        try:
            index = int(''.join(filter(str.isdigit, self.ns))) # Extrae numero para carril
            self.y = float(index - 1) * 1.5                   # Posicion inicial Y
        except: self.y = 0.0
        
        self.theta = 0.0                                      # Orientacion (yaw)
        self.v = 0.0                                          # Velocidad lineal actual
        self.w = 0.0                                          # Velocidad angular actual
        self.wheel_angle = 0.0                                # Angulo del timon (ruedas frontales)

        # Suscripcion a comandos de velocidad
        self.sub = self.create_subscription(Twist, 'cmd_vel', self.cmd_callback, 10) # Escucha ordenes
        
        # Publicadores
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)       # Mueve piezas
        self.tf_broadcaster = TransformBroadcaster(self)                             # Ubica en mapa
        self.timer = self.create_timer(0.05, self.update_physics)                    # Ciclo de fisica

    def cmd_callback(self, msg):
        self.v = msg.linear.x                                 # Guarda velocidad lineal recibida
        self.wheel_angle = msg.angular.z                                # Guarda velocidad angular recibida

    def update_physics(self):
        dt = 0.05                                             # Paso de tiempo
        L = 0.5
        if abs(self.v) > 0.01:
            self.w = (self.v / L) * math.tan(self.wheel_angle)
        else:
            self.w = 0.0
        # Logica de "Timon" simple (Direccion)
        #self.wheel_angle = self.w * 0.5                       # El angulo visual de las ruedas
        
        # Actualizacion de odometria (Movimiento en el plano)
        self.theta += self.w * dt                             # Actualiza orientacion
        self.x += self.v * math.cos(self.theta) * dt          # Movimiento en X
        self.y += self.v * math.sin(self.theta) * dt          # Movimiento en Y

        # 1. Enviar Transformada (TF) para RViz
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'
        t.child_frame_id = f'{self.ns}/base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.rotation.z = math.sin(self.theta / 2.0)   # Conversion simple a quaternion
        t.transform.rotation.w = math.cos(self.theta / 2.0)
        self.tf_broadcaster.sendTransform(t)

        # 2. Enviar Joints (Incluyendo el giro de las ruedas delanteras)
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        # Nota: Asegurate que estos nombres coincidan con tu URDF
        js.name = [
            f'{self.ns}/left_wheel_joint_a',  # Delantera Izq
            f'{self.ns}/right_wheel_joint_a', # Delantera Der
            f'{self.ns}/left_wheel_joint_p',  # Trasera Izq
            f'{self.ns}/right_wheel_joint_p'  # Trasera Der
        ]
        # Las frontales usan wheel_angle (timon), las traseras 0.0 (giro de traccion omitido por simpleza)
        js.position = [self.wheel_angle, self.wheel_angle, 0.0, 0.0] 
        self.joint_pub.publish(js)

def main(args=None):
    rclpy.init(args=args)
    node = MoverAgente()
    rclpy.spin(node)
    rclpy.shutdown()