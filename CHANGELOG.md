# AGENTES-COOPERACION 

Para instalar ROS2 kilted 
seguir la guia de instalacion 

https://docs.ros.org/en/kilted/Installation/Alternatives/Ubuntu-Development-Setup.html

## PRIMEROS COMANDOS
```bash 
# importante
esau@DESKTOP-A3RPEKP:~$ source /opt/ros/kilted/setup.sh
```
Obtenemos el script bash desde esa ruta y lo activamos (ejecutamos) , de modo que importamos las variables PATH, LD_LIBRARY_PATH, PYTHONPATH,ROS_DISTRO al shell (terminal) actual donde se ejecuta , luego las librerias y paquetes de ROS2 se ejecutaran correctamente en el terminal actual, hace estas entre otras exportaciones
```bash
export ROS_DISTRO=kilted
export PATH=/opt/ros/kilted/bin:$PATH
```

Se realiza una prueba rapida para ver el mecanismo piblisher - suscriptor 
```bash
ros2 run demo_nodes_cpp talker
[INFO] [1764453104.711036905] [talker]: Publishing: 'Hello World: 3030'
[INFO] [1764453109.265536838] [talker]: Publishing: 'Hello World: 3031'
....
ros2 run demo_nodes_py listener
[INFO] [1764453104.712581219] [listener]: I heard: [Hello World: 3030]
[INFO] [1764453109.266554404] [listener]: I heard: [Hello World: 3031]
```
### turtlesim
Seguir los pasos de instalacion
```bash
sudo apt install ros-kilted-turtlesim
# ros2 <verbo-principal> <subcomando> [argumentos] [opciones]
ros2 pkg executables turtlesim
```
A sabe **ros2** es el ejecutable principal , **pkg** es el comando de alto nivel(grupo de operaciones) para trabajar con paquetes equivalente a un **namespace** pues CLI esta organizado jerarquicamente 
```bash
ros2
 └── pkg
      ├── list
      ├── executables
      ├── prefix
      ├── xml
      └── create
# se obtiene la lista de funciones del modulo
turtlesim turtle_teleop_key
turtlesim turtlesim_node
...
```
en tanto que el subcomando **executable** y **turtlesim** indiacan la operacion y el argumento posicional(paquete). OSea ejecutamos el paquete turtlesim via ros2 pkg executable.<br>
Ahora 
```bash
# ros2 comando_principal paquete ejecutable
# llamamos a las funciones listadas antes
ros2 run turtlesim turtlesim_node
# en otro terminal
ros2 run turtlesim turtle_teleop_key
```
El primero crea el nodo donde se encuentra la tortuga y el otro manipula sus movimientos


Se esta trabajando en **wsl**, debido a que QT(la libreria que dibuja la ventana de turtlesim) espera que **/run/user/1000**  tenga permisos 0700 solo el usuario puede acceder, pero en wsl tenemos 0755 todos pueden leer/ejecutar, con **sudo chmod 700 /run/user/1000** remediamos eso.

Como bien indica el tutorial al ejecutar **ros2 run turtlesim turtle_teleop_key** en un nueva terminal se crea un nodo desde donde controlamos a la tortuga en el nodo ejecutado antes, con las flechas es posible hacer mover a la tortuga en la ventana QT
<p align="center">
    <img src="qt.png" width="60%">
</p>

### qrt
Se sigue luego las indicaciones para la instalacion de **rqt**, un framework grafico modular para manipular y visualizar los componentes del grafo ROS2(nodos,topicos,servicios,parametros,acciones,etc)<br>

Al ejecutar **rqt** tenemos una ventana para el manejo de las tortugas, pero cómo esta ventana  localiza los nodos de donde estan las tortuga ?<br>
Del siguiente modo : al ejecutar **rqt** este reconocera al nodo ejecutado via **ros2 run turtlesim turtlesim_node**, puesto que este ultimo se registra en el grado ROS2 anunciando su informacion correspondiente: 
```bash 
nodo : **/turtlesim**   yo publico: **/turtle1/pose** suscribo  : **/turtle1/cmd_vel** → tengo : **/reset/clear..** 
```
Este anuncio es manejado por DDS(descubrimiento automaticamente peer-to-peer) , luego rqt escucha el grafo ROS2  y ubica el nodo **turtlesim**, es cuando **rqt_graph** dibuja ese nodo. 

Ya se tiene la GUI luego  **Plugins / Services / Service caller** , ya en runnnig , para agregar una nueva seleccionamos **/spawn** en el menu desplegable al lado de **Service**.Le asignamos un nombre y posicion, finalmente presionamos el boton **call** 
Observar que la venta qt creado por **ros2 run turtlesim turtlesim_node**, ahora tenemos 2 tortugas

Probando los servicios , ahora modificamos algunos servicios,  otorgamos un pen **/turtle1/set_pen** asignando los valores a R=255 G =0 B=0, actualizamos la llamada **call** y el color del pen ahora es ROJO. 

Sin embargo nuestra **nueva_tortuga(el nombre que se asigne)** aun no puede moverse , necesitamos un segundo nodo para controlarlo.
```bash
# en una nueva terminal
ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=turtle2/cmd_vel
```
<p align="center">
    <img src="dos_tortugas.png" 
    width="35%">
</p>

Entonces desde la terminal donde se ejecutó **ros2 run turtlesim turtle_teleop_key** se manipula a la primera tortuga y desde el terminal donde ejecutamos **ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=tortuga_2/cmd_vel** controlamos a la segunda.

Pero como ? que pasó?
Detallemos, el ultimo comando ejecuta el nodo que lee el teclado **turtle_teleop_key** pero luego pasa los comandos(--ros-args --remap) a la tortuga_2 , el comando **turtle1/cmd_vel** ahora es cambiado a **turtle2/cmd_vel**(remapeo), esto ocurre en el sistema de nombres del grafo de ROS2,de modo que el nodo turtlesim , donde viven las dos instancias "tortugas" quedan diferenciadas.

Un breve resumen de los comandos
```bash
# se recomienda ejecutar la preparacion del entorno en todas las terminales, por las razones mecionadas
source /opt/ros/kilted/setup.sh
ros2 pkg executables turtlesim 
ros2 run turtlesim turtlesim_node
ros2 run turtlesim turttle_teleop_key
qrt
# deshovar 
ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=tortuga_2/cmd_vel
```
Se datalla en forma grafica el sistema anterior
### nodos (nodes)
<p align="center">
    <img src="grafo_ros2.png"
    width="50%">
</p>

Para obtener informacion de algun nodo: **ros2 node info /my_turtle** , cambiar el nombre : **ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle**

### temas(topicos)
Los tópicos son los canales por donde fluyen los mensajes de un nodo a otro. Es un canal de flujo unidireccional si bien un nodo puede estar suscrito a muchos topicos , no puede enviar info en el sentido contrario. Para realizar eso se necesitaria otro topic
```bash
              Topic: /wheel/status
    Rueda (Publisher)  ------------------>  Control (Subscriber)

             Topic: /wheel/commands
 Control (Publisher)  ------------------>   Rueda (Subscriber)

```
<p align="center">
    <img src="topic.png"
    width="50%">
</p>

### rqt_graph
### topicos
En la ventana rqt **Plugins/Introspection/Node graph** para visualizar de forma introspectiva los nodos ,temas y conexiones.
<p align="center">
    <img src="rqt_graph.png"
    width="60%">
</p>

Comandos para listas los temas(topics) , el tipo de tema , datos que publican 
```bash
ros2 topic list 
ros2 topic list -t
ros2 topic echo /turtle1/cmd_vel
```
El ultimo muestra los datos de la posicion de la primera tortuga.
Ademas **ros2 topic info /turtle1/cmd_vel** muestra los publisher y subscriptors que usan ese topico(canal de comunicacion)
```bash
ros2 topic list -t
ros2 interface show geometry_msgs/msg/Twist
```
**ros2 topic list -t** da una salida **geometry_msgs/msg/Twist** esto es que en el paquete **geometry_msgs** hay un **msg** llamado **Twist** ; otro comando util **ros2 interface show geometry_msgs/msg/Twist** para ver la estructura que espera el mensaje.

Para publicar datos en un tema directamente desde linea de comandos se usa 
```bash
ros2 topic pub <topic_name> <msg_type> '<args>'
# datos en formato YAML 
# publicamos ---- en canal----el tipo de mensaje----mensaje
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
#mensaje vacio
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" --rate 1
# autocompletar
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist <TAB>...
# una alternativa a YAML
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist \'linear:\^J\ \ x:\ 0.0\^J\ \ y:\ 0.0\^J\ \ z:\ 0.0\^Jangular:\^J\ \ x:\ 0.0\^J\ \ y:\ 0.0\^J\ \ z:\ 0.0\^J\'
```
Para que nuestro robot(en este caso la tortuga ) se mueva de manera constante se usaria el siguiente comando
```bash
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
```
O para publicar solo una vez
```bash
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.8}}"
```
<p align="center">
    <img src="comandos.png"
    width ="35%">
</p>

Para ver las posiciones **ros2 topic echo /turtle1/pose** . O publicar mensajees con marca de tiempo **ros2 topic pub /pose geometry_msgs/msg/PoseStamped '{header: "auto", pose: {position: {x: 1.0, y: 2.0, z: 3.0}}}'**, y para observar info adicional:
```bash
# velocidad de mensajes
ros2 topic hz /turtle1/pose 
#ancho de banda usado
ros2 topic bw /turtle1/pose
#encontrar tpicos que usen el tipo de mensaje
ros2 topic find <topic_type>
```
### servicios 
Los servicios son otro modo de comunicacion,dan respuestas solo  cuando el cliente lo solicita.
Bueno en este punto tenemos cierto bagaje, hay mucha teoria y muy interesante , pero con lo visto podemos afrontar la implementacion del proyecto (calificada) como tal.


## SIMULACION EN RVIZ mediante ros2

En changelog.md se describen la teoria de ros2 , nodos, mensajes, canales. 

Sin embargo se detalla (hasta este punto) la teoria pertienente.

La estructura de paquetes 
```bash
.
├── ejecucion.sh
├── limpieza.sh
└── src
    └── agente_pkg
        ├── action
        │   └── MoveJoint.action
        ├── agente_pkg
        │   ├── __init__.py
        │   └── mover_agente.py
        ├── launch
        │   └── agente_sim.launch.py
        ├── package.xml
        ├── resource
        │   └── agente_pkg
        ├── setup.cfg
        ├── setup.py
        └── urdf
            └── agente.xacro
```

El directorio raiz del workspace es **agentes_cooperacion** , es el espacio global de trabajo , el codigo fuente reside en **src/** , los binarios resultantes (construidos luego de **colcon build**) se almacenan en **build/ install/ log/** .

- **src/agente_pkg/urdf/agente.xacro** : define la estructura fisica de los carritos , se diseña como una plantilla parametrizada que acepta un prefijo **(arg perfix)** para permiten la creacion de multiples carritos sin piezas que colisionen el sistema.

- **src/agente_pkg/launch/agente_sim.launch.py** es el orquestador, inicia la simulacion lanzando tres copias del robot, gestiona los namespaces y las posiciones iniciales en el mapa

- **src/agente_pkg/agente_pkg/mover_agente.py** Nodo de control en python, calcula la rotacion de las ruedas

**NODOS**<br>
- **mover_agente** : este nodo publica en el topico /carro{i}/joint_states. Obtiene su propio namespace (**self.get_namespace()**) para saber a que carro pertenecen las ruedas.

- **robot_state_publisher** Se lanza una instancia por cada carro desde .launch.py , recibe la descripcion del robot procesada desde xacro(mapping={'prefix':prefijo}). Escucha los **joint_states** de su respectivo carro y publica TF (transform frames) que define donde esta cad rueda respecto al cuerpo del robot.

- **static_transform_publisher** un nodo de utilidad que actua como un "clavo" fisico. Conecta el origen del mundo (map) con el **base_link** de cada carro, permitiendo el renderizado de los carritos.

- **rviz** es el nodo de visualizacion , suscrito a los topicos **/tf** muestra los modelos 3D.

**TOPICOS**<br>
Los canales de comunicacion asincronos. 
- /caroo{i}/joint_states , publicado por mover_agente.py, contiene el arreglo **self.joint_names** con los nombres de las articulaciones y sus posiciones.

- /tf y /tf_static , el canal universal de las coordenadas, 
**robot_state_publisher** y el **static_transform_publisher**escriben la ubicación de cada pieza. RViz lee este tópico para saber dónde dibujar cada link.

- **/carro{i}/robot_descripcion** topico de tipo **latched** donde se publica el xmñl del robot. Rviz lo lee para saber que forma tiene el modelo (cajas, cilindro,etc)

**MENSAJES**<br>
El tipo de mensajes principal es **sensor_msgs/jontState**.Este paquete tiene 
- **header** , estampa de tiempo para sincronizacion

- **name** , los nombres de los joints ( carro1/left_wheel_joint_a)
- **position** , el valor angular en radianes 



**MOVIMIENTOS DE LOS AGENTES**<br>
el giro de las ruedas se define en mover() , val = math.sin(self.t).

Este mensaje se asigna a 4 articulaciones  **msg.position = [val,val,val,val]**

**self.t** incrementa el paso , lo que genera un movimiento continuo


**LAUNCH FILE(agente_sim.launch.py)**<br>
- El bucle for crea 3 grupos de nodos
- se parametriza **agente.xacro** para cada grupo (carrito).

- Encadenamiento , mover_agente crea un publicadoren el topico **joint_states** . Este topico es el puente , transporta la informacion cinematica (angulos) hacia el nodo **robot_state_publisher** ,quien traduce estos valores en TF(transformadas de coordenadas) , para que rviz los represente visualmente.


 
**package.xml**<br> 
Se define el nombre , version y las dependencias, <build_type>ament_python</build_type> indica que se usa ament_python como build type,de modo que colcon sabe que no el paquete no necesita compilarse solo se copiaran los scripts de python y archivos de recursos (urdf , launch) a la carpeta de instalacion

**setup.py**<br> 
Es donde se registran los archivos. Entry_points detalla que cuando se escriba **mover_agente** en la terminal se ejecuta la funcion main que esta en **mover_agente.py**

En lugar de python3 mover_agente.py ,en ros2 se usará el comando **ros2 agente_pkg mover_agente**
los entry points permiten que colcon (el constructor de ROS) genere un enlace simbolico en la carpeta install,de modo que el script se vuelve parte del PATH

La lista **data_files** define la estructura de busquedas. ROS2 no busca en la carpeta src cuando se ejcuta algo.Lo busca en install . Setup.py es el mapa que indica a colcon como mover **.xacro** y los **launch.py** desde src hacia **install/agente_pkg/share/..** .Si un archivo no esta en setup.py Ros no los encuentra.

Resumiendo, el proyecto es **escalable**, al usar xacro parametrizado , si queremos mas carritos , solo se necesitaria modificar el for en agente_sim.launch.py.

Es **modular**, pues separamos la logica de calculo (mover_agente) del calculo de la transformada **robot_state_publisher** es un nodo externo de ros2 quien usa la estructura del archivo xacro.
 
**Aislamiento** , los namespaces garantizan que cada agente sea un escosistema difirente.

Ahora que se dispone de los carritos se les otorga movimiento, en un primer momento un movimiento infinito hacia adelante.

```bash
SISTEMA DE ARCHIVOS          PROCESOS EN MEMORIA (NODOS)          VISUALIZACIÓN (RViz)
-------------------          ---------------------------          --------------------

agente_sim.launch.py
  |
  |-- (Bucle for 1..3) ----> [ robot_state_publisher ] --------> Carga el URDF/Modelo 3D
  |                                     ^                        (Sabe cómo se ve el carro)
  |                                     |
  |-- ld.add_action() -----> [ mover_agente (Script) ]           
                               |        |
                               |        |-- self.create_timer(0.05, self.mover)
                               |        |   (Cada 50ms llama a la función mover)
                               |        |
                               |        +--> self.tf_broadcaster.sendTransform(t)
                               |             (Publica: "carroX/base_link está en X, Y")
                               |             |
                               |             v
                               +---------- [ TF TREE ] <--------- RViz lee esto para saber 
                                             (Mapa de           DÓNDE dibujar cada modelo.
                                            coordenadas)
```

**ld = LaunchDescription()** Ros2 llena el pool de nodos y los lanza en paralelo. Mientras que **ld.load_action()** prepara un proceso para el ejecutable. Solo arranca el programa en python

En mover agente **self.create_time** interrumpe y ejecuta la funcion **mover** cada cierto tiempo.

**self.tf_broadcaster.sendTransform(t_msg)** envia la coordenada calculada al sitema global de ROS

RVIZ no lee directamente el script, sino que escucha al canl **Transformada TF**. Es el script quien publica alli, rviz mueve el dibujo del carro basandose en eso.

**rclpy** El spin es un bucle infinito , mantiene el programa vivo para para que el timer pueda seguir saltando cad  0.05s de lo contrario el programa terminaria en 1 segundo.

El launch crea 3 copias del nodo **mover_agente** en memoria. Cada uno tiene sus atributos,publicando cada uno una posicion diferente.


Se tiene como referencia el modelo cinematico de ackerman (coche convencional) 

Otro detalle es que "infundir moviminento" no implica desplazamiento, se calcula la nueva posicion de acuerdo a **x_nuevo = X_anterior + v*cos(theta)* delta T** v: velocidad, theta : angulo del timon.


Con nuevas modificaciones en **mover_agente** al usar la suscripcion a cmd_val ademas de aislar por espacio de nombres ( encapsular recursos), conseguimos topicos relativos haciendo que cuando el script se suscribe a **cmd_vel** (relativo) , el middleware (DDS) registra en el grafo los nombres **/carro1/cmd_vel  /carro2/cmd_vel**.

Ademas a nivel de red , cada  topico tiene su propia **GUID(global unique indetifier)** , entonces cuando enviamos un mensaje desde .sh al topico carro1 los suscriptores   de los otros carros ignoran el paquete a nivel hardware/kernel  porque el **Topic Name** en la cabecera del paquete no coincide.

```bash
ros2 topic pub -1 /carro$CARRO_NUM/cmd_vel geometry_msgs/msg/Twist "{
    linear: {x: $VEL_LINEAL, y: 0.0, z: 0.0}, 
    angular: {x: 0.0, y: 0.0, z: $RAD}
}"
```

al ejecutar ese bash **bash ordenes.sh 1 0.5 30** por ejemplo, ros2 topic pub -1 crea un nodo temporal (instanciacion del publisher efimero), este nodo anuncia en la red **publicar en /carro1/cmd_vel** el nodo mover_agente responde **estoy escuchando**(descubrimiento) ; la velocidad y el angulo se empaquetan en CDR (serializacion XCDR) ; el mensaje llega al buffer del suscriptor,el script de python no se detiene,la siguiente vez que el ejecutor (rclpy.spin) tiene un hueco , dispara el **cmd_callback**.

De topico a movimiento : 
- Recepcion : callback de interrupcion actualiza self.v y angulo 
- integracion: self.theta += self.w*dt
- transformada: TransformBroadcaster envia la nueva relacion entre frame map y base_link

Un detalle interesante en la sintaxis de ordenes.sh se asigna dos argumentos a bc **scale=4 ; GRADOS*PI/180** al comando bc, quien realiza la operacion matematica (° → radianes). Luego la sustitucion de comandos para asignar ese resultado a RAD = $().


Con las modificaciones del ultimo commit. Se tiene una ejecucion **app/** funcional, a comunicacion entre **main.py** y quien instancia 3 carritos , la clase **AgenteCarrito** cuya funcion **interactuar** referencia a **llm.py** donde el cliente OpenAi es instanciado.Es este modelo quien determina la accion a_t para luego ejecutar la herramienta , llamando a **mcp.py**. 

El target **make shell-app** , resetea los contenedores y abre un shell dentro del contenedor agentes-python. Alli ejecutamos **python -m app.main** y la instruccion 1:avanza

Sin embargo el comando **docker exec -it agentes-python bash ./agentes_cooperacion/ordenes.sh 3 0.5 20** (ej) nos devuelve  **command not found**

Lo que significa que el contenedor python no tiene instalado ROS2. 

