from .agente import AgenteCarrito

def main():
    flota = { 
        "1":AgenteCarrito(id_carro=1),
        "2":AgenteCarrito(id_carro=2),
        "3":AgenteCarrito(id_carro=3)
    }
    while(True):
        entrada = input("\n usuario (ej: '1:avanza'):")
        if ":" in entrada:
            id_ , orden = entrada.split(":",1)   #" 1: avanza" separa la primera vez
            if id_.strip() in flota:
                res = flota[id_.strip()].interactuar(orden.strip())
                print(f"Robot {id_}: {res}")
if __name__=='__main__':
    main()