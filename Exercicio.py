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
from re import X
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
                numAleatorio = randrange(1, 5)
                
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
    labirinto = atribuiCusto(labirinto)    
    return labirinto

#funçao para imprimir o labirinto
def imprimeLabirinto(labirinto):
    cont = 0
    print("_________________________________________\n|", end="")
    for x in labirinto:
        print('{:03}'.format(x), end = "")
        cont+=1
        if cont%10!=0:
            print(" ", end = "")
        else:
            print("|\n|", end = "")
    print("̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ")
#funçao de adjacente para o labirinto
# def adjacente (labirinto, ponto):
#     x, y = ponto
#     adjacente = []
#     if x > 0:
#         adjacente.append((x - 1, y))
#     if x < 9:
#         adjacente.append((x + 1, y))
#     if y > 0:
#         adjacente.append((x, y - 1))
#     if y < 9:
#         adjacente.append((x, y + 1))
#     return adjacente
#funçao para aleatorizar os custos de cada casa)
def atribuiCusto (labirinto):
    for x in range(len(labirinto)):
        if labirinto[x] != 0:
            labirinto[x] = "|-|"
        else:
            labirinto[x] = randrange(1, 5)
    labirinto[0] = "^)>"
            
    return labirinto
#funçao alterar o tabuleiro com o caminho do pato
def movimentaPato (labirinto, localizacaoAtual, proximaLocalizacao):
    valorHeuristica = 0
    posicaoCerta = False
    
#-------Verifica se a localizacao atual bate com a localização do pato-------#
    for x in range(len(labirinto)):
        if x == localizacaoAtual and labirinto[x] == "^)>":
            posicaoCerta = True
            break
    
#---------Verifica se a proxima posição é possível dentro do sistema---------#
    if labirinto[proximaLocalizacao] != "|-|" and posicaoCerta == True:
        if (localizacaoAtual-proximaLocalizacao)==1:
            labirinto[localizacaoAtual] = "<<<"
        if (localizacaoAtual-proximaLocalizacao)==-1:
            labirinto[localizacaoAtual] = ">>>"
        if (localizacaoAtual-proximaLocalizacao)==10:
            labirinto[localizacaoAtual] = "^^^"
        if (localizacaoAtual-proximaLocalizacao)==-10:
            labirinto[localizacaoAtual] = "vvv"
        
        valorHeuristica = labirinto[proximaLocalizacao]
        labirinto[proximaLocalizacao] = "^)>"
#--------testes para saber se o sistema está funcionando corretamente--------#
    elif posicaoCerta == False:
        print("O pato não está nessa posição")
    else:
        print("A posição %d está bloqueada!" % proximaLocalizacao)
        
    imprimeLabirinto(labirinto)
    return valorHeuristica
#funçao busca gulosa
def buscaGulosa(labirinto, posicaoAtual):
    labirintoTeste = []
    labirintoTeste = labirinto
    caminhoTotal = 0
    
    while True:
        menorDistancia = 5

        if (posicaoAtual+1)%10!=0 and type(labirinto[posicaoAtual+1]) != str:            #direita
            if menorDistancia>labirinto[posicaoAtual+1]:
                menorDistancia = labirinto[posicaoAtual+1]
                movimento = "d"

        if posicaoAtual%10!=0 and type(labirinto[posicaoAtual-1]) != str:                #esquerda
            if menorDistancia>labirinto[posicaoAtual-1]:
                menorDistancia = labirinto[posicaoAtual-1]
                movimento = "e"
            
        if posicaoAtual<90 and type(labirinto[posicaoAtual+10]) != str:                  #baixo
            if menorDistancia>labirinto[posicaoAtual+10]:
                menorDistancia = labirinto[posicaoAtual+10]
                movimento = "b"
            
        if posicaoAtual>10 and type(labirinto[posicaoAtual-10]) != str:                  #cima
            if menorDistancia>labirinto[posicaoAtual-10]:
                menorDistancia = labirinto[posicaoAtual-10]
                movimento = "c"

        if type(labirinto[posicaoAtual+1]) == str and type(labirinto[posicaoAtual-1]) == str and type(labirinto[posicaoAtual+10]) == str and type(labirinto[posicaoAtual-10]) == str:
            print("O pato ficou preso, meus pesâmes...")
            exit(1)
            
        if movimento == "d":
            caminhoTotal += movimentaPato(labirintoTeste, posicaoAtual, posicaoAtual+1)
            posicaoAtual+=1
        if movimento == "e":
            caminhoTotal += movimentaPato(labirintoTeste, posicaoAtual, posicaoAtual-1)
            posicaoAtual-=1
        if movimento == "b":
            caminhoTotal += movimentaPato(labirintoTeste, posicaoAtual, posicaoAtual+10)
            posicaoAtual+=10
        if movimento == "c":
            caminhoTotal += movimentaPato(labirintoTeste, posicaoAtual, posicaoAtual-10)
            posicaoAtual-=10

        # imprimeLabirinto(labirintoTeste)

        if(posicaoAtual == 99):
            break

#funçao de heuristica
#funçao de heuristica
# def heuristica (Labirinto, ponto):
#     x, y = ponto
#     #declara a variavel heuristica
#     heuristica = math.sqrt((x - 9) * 2 + (y - 9) * 2)
#     return heuristica
# #funçao de busca em A*
# def busca (Labirinto, ponto_inicial, ponto_final):
#     #declara a variavel ponto inicial
#     ponto_inicial = (0, 0)
#     #declara a variavel ponto final
#     ponto_final = (9, 9)
#     #declara a variavel fechado
#     fechado = set()
#     #declara a variavel aberto
#     aberto = set([ponto_inicial])
#     #declara a variavel caminho
#     caminho = {}
#     #declara a variavel g
#     g = {ponto_inicial: 0}
#     #declara a variavel f
#     h = {ponto_inicial: heuristica(Labirinto, ponto_inicial)}
#     #enquanto o aberto for diferente de vazio
#     f = {ponto_inicial: g[ponto_inicial] + h[ponto_inicial]}

print("Temos que ajudar o nosso pato encontrar o caminho mais curto para chegar a em seu lago")
print("O nosso pato está no ponto (0,0) e tem que chegar no ponto (9,9)")
print("O nosso pato não pode sair do labirinto")
print("O nosso pato não pode passar por uma casa ocupada")
print("O nosso pato pode se mover para cima, baixo, esquerda ou direita")

labirinto = []
labirinto = criaLabirinto()
imprimeLabirinto(labirinto)
buscaGulosa(labirinto, 0)

# contEuristica = movimentaPato(labirinto, 0, 10)
# print(contEuristica)
# imprimeLabirinto(labirinto)