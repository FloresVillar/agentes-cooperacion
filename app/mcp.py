import subprocess

def ejecutar_herramienta(nombre,parametros):
    if nombre == "mover_carro":
        idx = parametros.get("id")
        v = parametros.get("v")
        deg = parametros.get("deg")
        cmd = ["bash","./agentes_cooperacion/ordenes.sh",str(idx),str(v),str(deg)]
        res = subprocess.run(cmd,capture_output=True,text=True)
        return res.stdout
    return "herramienta no encontrada"
def obtener_esquema_tools():
    return """
    - mover_carro: {"id":int , "v":float, "deg":int}.
      mueve el carro ID a velocidad y angulo DEG.
    """
