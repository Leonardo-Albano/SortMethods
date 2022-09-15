#problema e otimizacao de busca em A*
#o problema de otimização é o de encontrar o menor caminho dentro de um labirinto de 10x10 casas (1600 casas)
#o labirinto é representado por uma matriz de 10x10 casas, cada casa pode ser livre ou ocupada
#o agente começa na casa (0,0) e tem que chegar na casa (9,9)
#o agente pode se mover para cima, baixo, esquerda ou direita
#o agente não pode sair do labirinto
#o agente não pode passar por uma casa ocupada
from random import randrange 
import math
import copy
import time
from xmlrpc.client import boolean

# variavel que ocupa lugar
# livre  = 0
# ocupado= 1

#funçao para inicializar o labirinto
#-----------------------------aleatorização do labirinto-----------------------------#  
def criaLabirinto (): 
    labirinto = []
    labirinto.append(0)
    for x in range(1, 99):
        if randrange(0, 2) == 0:
            labirinto.append(0)
        else: labirinto.append(x)
    labirinto.append(0)

#------------------faz a verificação dos adjascentes de cada posição-----------------#
    for x in range(len(labirinto)):
        contadorAdjasc = 0
    
        if x<99:
            if labirinto[x+1] == 0:
                contadorAdjasc+=1

        if x>0:
            if labirinto[x-1] == 0:
                contadorAdjasc+=1
            
        if x<90:    
            if labirinto[x+10] == 0:
                contadorAdjasc+=1
                
        if x>10:    
            if labirinto[x-10] == 0:
                contadorAdjasc+=1
                
#---caso a posição tenha menos que 2 adjascentes, o programa aleatoriza novamente---#                
        if contadorAdjasc<2:
            while(True):
                numAleatorio= randrange(1, 5)
                
                if numAleatorio == 1 and (x % 10!=0):
                    labirinto[x-1] = 0
                    break

                if numAleatorio == 2 and ((x + 1) % 10!=0):
                    labirinto[x+1] = 0
                    break
                
                if numAleatorio == 3 and not x in range(90, 100):
                    labirinto[x+10] = 0
                    break
                    
                if numAleatorio == 4 and not x in range(0, 10):
                    labirinto[x-10] = 0
                    break
        
    return labirinto

#funçao para imprimir o labirinto
def imprimeLabirinto(labirinto):
    cont = 0
    print("_________________________________________\n|", end="")
    for x in labirinto:
        if x==0:
            print("   ", end="")
        else:
            print("XXX", end = "")
        cont+=1
        if cont%10!=0:
            print(" ", end = "")
        else:
            print("|\n|", end = "")
    print("̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ")
#funçao de adjacente para o labirinto
def adjacente (labirinto, ponto):
    x, y = ponto
    adjacente = []
    if x > 0:
        adjacente.append((x - 1, y))
    if x < 9:
        adjacente.append((x + 1, y))
    if y > 0:
        adjacente.append((x, y - 1))
    if y < 9:
        adjacente.append((x, y + 1))
    return adjacente
#funçao de custo
def custo (Labirinto, ponto):
    return 1
#funçao de heuristica
def heuristica (Labirinto, ponto):
    x, y = ponto
    #declara a variavel heuristica
    heuristica = math.sqrt((x - 9) * 2 + (y - 9) * 2)
    return heuristica
#funçao de busca em A*
def busca (Labirinto, ponto_inicial, ponto_final):
    #declara a variabel ponto inicial
    ponto_inicial = (0, 0)
    #declara a variabel ponto final
    ponto_final = (9, 9)
    #declara a variavel fechado
    fechado = set()
    #declara a variavel aberto
    aberto = set([ponto_inicial])
    #declara a variavel caminho
    caminho = {}
    #declara a variavel g
    g = {ponto_inicial: 0}
    #declara a variavel f
    h = {ponto_inicial: heuristica(Labirinto, ponto_inicial)}
    #enquanto o aberto for diferente de vazio
    f = {ponto_inicial: g[ponto_inicial] + h[ponto_inicial]}

print("Temos que ajudar o nosso pato encontrar o caminho mais curto para chegar a em seu lago")
print("O nosso pato está no ponto (0,0) e tem que chegar no ponto (9,9)")
print("O nosso pato não pode sair do labirinto")
print("O nosso pato não pode passar por uma casa ocupada")
print("O nosso pato pode se mover para cima, baixo, esquerda ou direita")

labirinto = []
labirinto = criaLabirinto()
imprimeLabirinto(labirinto)