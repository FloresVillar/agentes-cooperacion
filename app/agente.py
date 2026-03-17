import json 
from .llm import llamada_a_modelo
from .mcp import ejecutar_herramienta, obtener_esquema_tools

class AgenteCarrito:
    def __init__(self,id_carro):
        self.id = id_carro
        self.historial = []
        self.prompt_sistema = f"""Solo JSON.
        Ejemplo:
        {{"herramienta":"mover_carro","parametros":{{"id":{self.id},"v":0.5,"deg":0}}}} 
        
        Respuesta:
        {{"respuesta":"texto"}}
        """
    def interactuar(self,mensaje_usuario):
        self.historial.append({"role":"user","content":mensaje_usuario})
        ya_ejecuto = False
        respuesta_raw = llamada_a_modelo(self.historial,self.prompt_sistema)
        try:
            limpio = respuesta_raw
            if "```" in limpio:
                partes = limpio.split("```")
                if len(partes)>3:
                    limpio = limpio[1]
                    if limpio.startswith("json"):
                        limpio = limpio[4:]
            inicio_json = limpio.find('{')
            fin_json = limpio.rfind('}') + 1
            limpio = limpio.strip()
            if inicio_json != -1 and fin_json != 0:
                str_ = limpio[inicio_json:fin_json]
                data = json.loads(str_)
                if data.get("herramienta") in ["mover_carro","avanzar","mover"]:
                    nombre_real = "mover_carro"
                    resultado_fisico = ejecutar_herramienta(nombre_real,data["parametros"])
                    self.historial.append({"role":"assistant","content":respuesta_raw})
                    return f"Accion ejecutada:{resultado_fisico}"
        except Exception as e:
            return f"respuesta IA : {respuesta_raw}\n error: {e}"
        return respuesta_raw
