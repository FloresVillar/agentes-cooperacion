import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/esau/agentes-cooperacion/agentes_cooperacion/install/agente_pkg'
