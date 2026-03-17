import json 
from .llm import llamada_a_modelo
from .mcp import ejecutar_herramienta

class AgenteCarrito:
    def __init__(self, id_carro):
        self.id = id_carro
        self.h_t = []
        # Prompt ultra-directo: Prohibimos las disculpas
        self.prompt_sistema = f"""SISTEMA DE CONTROL CARRO {self.id}.
        REGLA: SOLO RESPONDE JSON. NO HABLES.
        COMANDO: {{"herramienta":"mover_carro","parametros":{{"id":{self.id},"v":0.5,"deg":0}}}}
        """

    def interactuar(self, mensaje_usuario):
        self.h_t.append({"role": "user", "content": mensaje_usuario})
        ya_ejecuto = False
        
        while True:
            a_t = llamada_a_modelo(self.h_t, self.prompt_sistema)
            try:
                # LIMPIEZA QUIRÚRGICA: Buscamos el JSON real ignorando el texto de la IA
                inicio = a_t.find('{')
                fin = a_t.rfind('}') + 1
                
                if inicio != -1 and fin > 0:
                    json_str = a_t[inicio:fin].strip()
                    data = json.loads(json_str)
                    
                    if data.get("herramienta") in ["mover_carro", "avanzar", "mover"] and not ya_ejecuto:
                        ya_ejecuto = True 
                        
                        # REFUERZO DE IDENTIDAD: Forzamos el ID del objeto
                        if "parametros" not in data: data["parametros"] = {}
                        data["parametros"]["id"] = self.id
                        
                        # Ejecución
                        o_t = ejecutar_herramienta("mover_carro", data["parametros"])
                        print(f"output del entorno: {o_t}")
                        
                        self.h_t.append({"role": "assistant", "content": a_t})
                        self.h_t.append({"role": "user", "content": f"resultado: {o_t}"})
                        continue 

            except Exception as e:
                # Si falla el JSON, imprimimos el error para saber qué pasó
                print(f"DEBUG ERROR PARSE: {e}")
                pass

            self.h_t.append({"role": "assistant", "content": a_t})
            return a_t