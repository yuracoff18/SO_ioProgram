from sys import argv
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

MAXCILINDROS = 4999
MINCILINDROS = 0

def graficar_recorrido(nombre, recorrido, carpeta):
    plt.figure(figsize=(11, 4.5))
    plt.plot(
        range(len(recorrido)),
        recorrido,
        linewidth=1.2
    )

    plt.xlabel("Paso del recorrido")
    plt.ylabel("Posicion del cabezal (cilindro)")
    plt.title(f"Movimiento del cabezal - {nombre}")
    plt.ylim(-100, 5100)
    plt.grid(alpha=0.25)
    plt.tight_layout()

    archivo = f"movimiento_{nombre.lower().replace('-', '_')}.png"
    plt.savefig(carpeta / archivo, dpi=160)
    plt.close()
    
def graficar_comparacion(totales, carpeta):
    nombres = list(totales)
    valores = [totales[nombre] for nombre in nombres]

    plt.figure(figsize=(8, 5))
    barras = plt.bar(nombres, valores)

    for barra, valor in zip(barras, valores):
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            valor,
            f"{valor:,}",
            ha="center",
            va="bottom"
        )

    plt.ylabel("Distancia total (cilindros)")
    plt.title("Comparacion de algoritmos")
    plt.ylim(0, max(valores) * 1.13)
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()

    plt.savefig(carpeta / "comparacion.png", dpi=160)
    plt.close()

# ======================================================================================================================

def fcfs(init, req):
    ans = [init] + req
    return ans

def scan(init, req: list):
    ans = [init]
    mayores = sorted(x for x in req if x >= init)
    menores = sorted((x for x in req if x < init), reverse=True)
    
    ans += mayores
    
    if menores:
        if ans[-1] != MAXCILINDROS:
            ans.append(MAXCILINDROS)
        ans.extend(menores)
        
    return ans

def c_scan(init, req: list):
    ans = [init]
    mayores = sorted(x for x in req if x >= init)
    menores = sorted(x for x in req if x < init)
    
    ans += mayores
    
    if menores:
        if ans[-1] != MAXCILINDROS:
            ans.append(MAXCILINDROS)
        ans.append(0)
        ans.extend(menores)
        
    return ans

def totMovimiento(recorrido):
    ans = 0
    aux = recorrido[0]
    for i in range(1, len(recorrido)):
        ans += abs(aux - recorrido[i])
        aux = recorrido[i]
    return ans


def main():
    if len(argv) > 1:
        initialPos = int(argv[1])
        
        if initialPos > MAXCILINDROS or initialPos < MINCILINDROS:
            print('Posicion inicial del disco no valida')
        else:
            # Programa principal
            rng = random.Random()
            rng.seed(67)
            requests = [rng.randrange(MAXCILINDROS) for _ in range(1000)]
            
            carpeta = Path('resultados')
            carpeta.mkdir(parents=True, exist_ok=True)
            
            recorridos = {
                "FCFS": fcfs(initialPos, requests),
                "SCAN": scan(initialPos, requests),
                "C_SCAN": c_scan(initialPos, requests)
            }
            
            totales = {
                nombre: totMovimiento(rec) for nombre, rec in recorridos.items()
            }
            
            for nombre, tot in totales.items():
                print(f'{nombre}: {tot} cilindros')
            
            with (carpeta/'solicitudes.txt').open('w') as archivo:
                for sol in requests:
                    archivo.write(f"{sol}\n")
                archivo.close()
            
            with (carpeta/'resultados.txt').open('w') as archivo:
                for nombre, res in totales.items():
                    archivo.write(f"{nombre}: {res} cilindros\n")
                archivo.close()

            for nombre, recorrido in recorridos.items():
                graficar_recorrido(nombre, recorrido, carpeta)

            graficar_comparacion(totales, carpeta)

            print(f"\nArchivos guardados en: {carpeta.resolve()}")
            
    else:
        print("Posicion inicial del disco es requerido.")
        

if __name__ == "__main__":
    main()