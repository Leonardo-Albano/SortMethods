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
 
#funçao para aleatorizar os custos de cada casa)
def atribuiCusto (labirinto):
    for x in range(len(labirinto)):
        if labirinto[x] != 0:
            labirinto[x] = "|-|"
        else:
            labirinto[x] = randrange(1, 5)
    labirinto[0] = "°)<"
           
    return labirinto
#funçao alterar o tabuleiro com o caminho do pato
def movimentaPato (labirinto, localizacaoAtual, proximaLocalizacao):
    valorHeuristica = 0
    posicaoCerta = False
   
#-------Verifica se a localizacao atual bate com a localização do pato-------#
    for x in range(len(labirinto)):
        if x == localizacaoAtual and labirinto[x] == "°)<":
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
        labirinto[proximaLocalizacao] = "°)<"
#--------testes para saber se o sistema está funcionando corretamente--------#
    elif posicaoCerta == False:
        print("O pato não está nessa posição")
    else:
        print("A posição %d está bloqueada!" % proximaLocalizacao)
       
    imprimeLabirinto(labirinto)
    return valorHeuristica
#funçao para verificar se o pato está preso
def verificaPatoPreso(labirinto, posicaoAtual):
    if posicaoAtual%10==0 and type(labirinto[posicaoAtual+1]) == str and type(labirinto[posicaoAtual+10]) == str and type(labirinto[posicaoAtual-10]) == str:
        print("O pato ficou preso na esquerda.. looonge.. tadinho...")
        return(1)
    
    if (posicaoAtual+1)%10==0 and type(labirinto[posicaoAtual-1]) == str and type(labirinto[posicaoAtual+10]) == str and type(labirinto[posicaoAtual-10]) == str:
        print("O pato ficou preso na direita.. Quase que chega lá...")
        return(1)
    
    if posicaoAtual>89 and type(labirinto[posicaoAtual-1]) == str and type(labirinto[posicaoAtual+1]) == str and type(labirinto[posicaoAtual-10]) == str:
        print("O pato ficou preso embaixo.. coitado dele...")
        return(1)
    
    if posicaoAtual<10 and type(labirinto[posicaoAtual-1]) == str and type(labirinto[posicaoAtual+10]) == str and type(labirinto[posicaoAtual+1]) == str:
        print("O pato ficou preso lá encima, meio longe da lagoa, não acha?")
        return(1)
    
    if type(labirinto[posicaoAtual+1]) == str and type(labirinto[posicaoAtual-1]) == str and type(labirinto[posicaoAtual+10]) == str and type(labirinto[posicaoAtual-10]) == str:
        print("O pato ficou preso bem no meio... Lagoa fica pra proxima.")
        return(1)
    
    if posicaoAtual>89 and posicaoAtual%10==0 and type(labirinto[posicaoAtual-10]) == str and type(labirinto[posicaoAtual+1]) == str:
        print("O pato está preso para sempre no cantinho de baixo.")
        return(1)
    
    if (posicaoAtual+1)%10==0 and posicaoAtual<10 and type(labirinto[posicaoAtual+10]) == str and type(labirinto[posicaoAtual-1]) == str:
        print("Na busca pela lagoa, o pato só encontrou a perdição no topo do mapa..")
        return(1)
    
    return(0)

def verificaMenorCaminho(labirinto, posicaoAtual):
    menorDistancia = 5
 
    if (posicaoAtual+1)%10!=0 and type(labirinto[posicaoAtual+1]) != str:            #direita
        if menorDistancia>labirinto[posicaoAtual+1]:
            menorDistancia = labirinto[posicaoAtual+1]
            melhorMovimento = "d"

    if posicaoAtual%10!=0 and type(labirinto[posicaoAtual-1]) != str:                #esquerda
        if menorDistancia>labirinto[posicaoAtual-1]:
            menorDistancia = labirinto[posicaoAtual-1]
            melhorMovimento = "e"
        
    if posicaoAtual<90 and type(labirinto[posicaoAtual+10]) != str:                  #baixo
        if menorDistancia>labirinto[posicaoAtual+10]:
            menorDistancia = labirinto[posicaoAtual+10]
            melhorMovimento = "b"
        
    if posicaoAtual>10 and type(labirinto[posicaoAtual-10]) != str:                  #cima
        if menorDistancia>labirinto[posicaoAtual-10]:
            menorDistancia = labirinto[posicaoAtual-10]
            melhorMovimento = "c"
    
    return melhorMovimento        
    
#funçao busca gulosa
def buscaGulosa(labirinto):
    posicaoAtual = 0
    labirintoTeste = []
    labirintoTeste = labirinto
    caminhoTotal = 0
   
    while True:
        if(verificaPatoPreso(labirinto, posicaoAtual)==1):
            break
            
        movimento = verificaMenorCaminho(labirinto, posicaoAtual)
 
           
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
 
        if(posicaoAtual == 99):
            print("O pato chegou até a lagoa!! \o/\nO número da heurística foi de %d." % caminhoTotal)
            print("Agora ele pode nadar feliz em sua lagoinha!")
            break
#funçao heuristica
def heuristica(posicaoAtual):
    g=0
    h=99-posicaoAtual
    f=g+h
    return f

 
#funçao busca A*
def buscaA(labirinto):
    aberta=[]
    fechada=[]
    posicaoAtual = 0
    labirintoTeste = []
    labirintoTeste = labirinto
    caminhoTotal = 0
    aberta.append(posicaoAtual)
    while True:
        if(verificaPatoPreso(labirinto, posicaoAtual)==1):
            break
        posicaoAtual = 0
        # aberta.remove(posicaoAtual)
        fechada.append(posicaoAtual)
        heuristica(posicaoAtual)
        if(posicaoAtual == 99):
            print("O pato chegou até a lagoa!! \o/\nO número da heurística foi de %d." % caminhoTotal)
            print("Agora ele pode nadar feliz em sua lagoinha!")
            break
        if (posicaoAtual+1)%10!=0 and type(labirinto[posicaoAtual+1]) != str and labirinto[posicaoAtual+1] not in fechada:            #direita
            aberta.append(posicaoAtual)
            fechada.append(posicaoAtual)
            caminhoTotal += movimentaPato(labirintoTeste, posicaoAtual, posicaoAtual+1)
            posicaoAtual+=1
            fechada.append(posicaoAtual)
            caminhoTotal += movimentaPato(labirintoTeste, posicaoAtual, posicaoAtual+1)
        if posicaoAtual%10!=0 and type(labirinto[posicaoAtual-1]) != str and labirinto[posicaoAtual-1] not in fechada:                #esquerda
            aberta.append(posicaoAtual)
            fechada.append(posicaoAtual)
            caminhoTotal += movimentaPato(labirintoTeste, posicaoAtual, posicaoAtual-1)
            posicaoAtual-=1
            fechada.append(posicaoAtual)
            caminhoTotal += movimentaPato(labirintoTeste, posicaoAtual, posicaoAtual-1)
        if posicaoAtual<9 and type(labirinto[posicaoAtual+10]) != str and labirinto[posicaoAtual+10] not in fechada:                  #baixo
            aberta.append(posicaoAtual)
            fechada.append(posicaoAtual)
            caminhoTotal += movimentaPato(labirintoTeste, posicaoAtual, posicaoAtual+10)
            posicaoAtual+=10
            fechada.append(posicaoAtual)
            caminhoTotal += movimentaPato(labirintoTeste, posicaoAtual, posicaoAtual+10)
        if posicaoAtual>10 and type(labirinto[posicaoAtual-10]) != str and labirinto[posicaoAtual-10] not in fechada:                  #cima
            aberta.append(posicaoAtual)
            fechada.append(posicaoAtual)
            caminhoTotal += movimentaPato(labirintoTeste, posicaoAtual, posicaoAtual-10)
            posicaoAtual-=10
            fechada.append(posicaoAtual)
            caminhoTotal += movimentaPato(labirintoTeste, posicaoAtual, posicaoAtual-10)
        if fechada == 99:
            print("O pato chegou até a lagoa!! \o/\nO número da heurística foi de %d." % caminhoTotal)
            print("Agora ele pode nadar feliz em sua lagoinha!")
            exit()
            break
        aberta.sort(key=lambda x: labirinto[x])
        print(aberta)
        print(fechada)
        print(labirinto)
     



   
        
#funçao principal
print("Bem vindo ao jogo do pato!")
print("O nosso pato está preso em um labirinto e tem que chegar até a lagoa")
print("Temos que ajudar o nosso pato encontrar o caminho mais curto para chegar a em seu lago")
print("O nosso pato está no ponto (0,0) e tem que chegar no ponto (9,9)")
print("O nosso pato não pode sair do labirinto")
print("O nosso pato não pode passar por uma casa ocupada")
print("O nosso pato pode se mover para cima, baixo, esquerda ou direita")

labirinto = []
while True:
    print("\nQual forma de busca você deseja fazer?")
    escolha = int(input("Busca gulosa (1) / Busca A* (2): "))
    
    labirinto = criaLabirinto()
    imprimeLabirinto(labirinto)
    
    if escolha == 1: 
        buscaGulosa(labirinto)
    elif escolha == 2:
       buscaA(labirinto)
    else:
        print("Escolha inválida.")
        
    if int(input("Deseja jogar novamente?\n(0-Não/1-Sim): ")) == 0:
        print("Obrigado por jogar!")
        break
