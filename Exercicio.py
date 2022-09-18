#o agente pode se mover para cima, baixo, esquerda ou direita
#o agente não pode sair do labirinto
#o agente não pode passar por uma casa ocupada
from random import randrange
import math
import copy
from re import X
import time
from xmlrpc.client import boolean

 
#funçao para inicializar o labirinto
def criaLabirinto ():
    labirinto = []
    labirinto.append(0)                     #adiciona 0 na casa inicial
    
#-----------------------------aleatorização do labirinto-----------------------------#  
    for x in range(1, 99):                  #aleatoriza todas as casas, menos a inicial e final
        if randrange(0, 2) == 0:            #aleatoriza entre 0(livre) e 1(obstáculo)
            labirinto.append(0)
        else: labirinto.append(x)           #caso 1, insere o número da casa no vetor
        
    labirinto.append(0)                     #adiciona 0 na casa final
 
#------------------faz a verificação dos adjascentes de cada posição-----------------#
    for x in range(len(labirinto)):
        contadorAdjasc = 0
   
        if (x+1)%10!=0:                     #coluna do 9-19-29-...
            if labirinto[x+1] == 0:
                contadorAdjasc+=1
 
        if x%10!=0:                         #coluna do 0-10-20-...
            if labirinto[x-1] == 0:
                contadorAdjasc+=1
           
        if x<90:                            #linha do 90-99
            if labirinto[x+10] == 0:
                contadorAdjasc+=1
               
        if x>10:                            #linha do 0-9
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
        print('{:03}'.format(x), end = "")              #imprime todos os valores com 3 caracteres
        cont+=1
        if cont%10!=0:                                  #imprime as divisões
            print(" ", end = "")
        else:
            print("|\n|", end = "")
    print("̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ̅ ")
 
#funçao para aleatorizar os custos de cada casa)
def atribuiCusto (labirinto):
    for x in range(len(labirinto)):
        if labirinto[x] != 0:
            labirinto[x] = "|-|"                    #insere a barreira caso o número seja diferente de 0
        else:
            labirinto[x] = randrange(1, 5)          #atribui um valor de 1-4
    labirinto[0] = "°)<"                            #coloca o pato na posição 0 (pato = °)> )
           
    return labirinto
#funçao alterar o tabuleiro com o caminho do pato
def movimentaPato (labirinto, localizacaoAtual, proximaLocalizacao):
    valorHeuristica = 0
    posicaoCerta = False
   
#--Verifica se a localizacao atual informada bate com a localização do pato--#
    for x in range(len(labirinto)):
        if x == localizacaoAtual and labirinto[x] == "°)<":
            posicaoCerta = True
            break
   
#-----Verifica a possibilidade e insere o pato na localização informada-----#
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

    imprimeLabirinto(labirinto)
    return valorHeuristica
#funçao para verificar se o pato está preso
def verificaPatoPreso(labirinto, posicaoAtual):

    if (posicaoAtual+1)%10==0 and type(labirinto[posicaoAtual-1]) == str and type(labirinto[posicaoAtual+10]) == str and type(labirinto[posicaoAtual-10]) == str:
        print("O pato ficou preso na direita.. Quase que chega lá...")
        return(1)
    
    if posicaoAtual>89 and type(labirinto[posicaoAtual-1]) == str and type(labirinto[posicaoAtual+1]) == str and type(labirinto[posicaoAtual-10]) == str:
        print("O pato ficou preso embaixo.. coitado dele...")
        return(1)
    
    if posicaoAtual<10 and type(labirinto[posicaoAtual-1]) == str and type(labirinto[posicaoAtual+10]) == str and type(labirinto[posicaoAtual+1]) == str:
        print("O pato ficou preso lá encima, meio longe da lagoa, não acha?")
        return(1)
    
    if posicaoAtual%10==0 and type(labirinto[posicaoAtual+1]) == str and type(labirinto[posicaoAtual+10]) == str and type(labirinto[posicaoAtual-10]) == str:
        print("O pato ficou preso na esquerda.. looonge.. tadinho...")
        return(1)
    
    if posicaoAtual>89 and posicaoAtual%10==0 and type(labirinto[posicaoAtual-10]) == str and type(labirinto[posicaoAtual+1]) == str:
        print("O pato está preso para sempre no cantinho de baixo.")
        return(1)
    
    if (posicaoAtual+1)%10==0 and posicaoAtual<10 and type(labirinto[posicaoAtual+10]) == str and type(labirinto[posicaoAtual-1]) == str:
        print("Na busca pela lagoa, o pato só encontrou a perdição no topo do mapa..")
        return(1)
    
    if type(labirinto[posicaoAtual+1]) == str and type(labirinto[posicaoAtual-1]) == str and type(labirinto[posicaoAtual+10]) == str and type(labirinto[posicaoAtual-10]) == str:
        print("O pato ficou preso bem no meio... Lagoa fica pra proxima.")
        return(1)
    
    return(0)               #retorna 0 caso o pato não esteja preso

def verificaMenorCaminho(labirinto, posicaoAtual):
    menorDistancia = 5              #inicia o valor mais que qualquer custo
 
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
    
    return melhorMovimento          #retorna a casa possível e com menor custo
    
#funçao busca gulosa
def buscaGulosa(labirinto):
    posicaoAtual = 0
    labirintoTeste = []
    labirintoTeste = labirinto
    caminhoTotal = 0
   
    while True:
        if(verificaPatoPreso(labirinto, posicaoAtual)==1):      #caso o pato esteja preso, finaliza a tentativa com falha
            break
            
        movimento = verificaMenorCaminho(labirinto, posicaoAtual)
 
#-----------------movimenta o pato de acordo com o resultado obtido pela função-----------------#
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
 
        if(posicaoAtual == 99):                         #caso o pato chegue no final, finaliza a tentativa com sucesso                                      
            print("O pato chegou até a lagoa!! \o/\nO número da heurística foi de %d." % caminhoTotal)
            print("Agora ele pode nadar feliz em sua lagoinha!")
            break

 
 #----------------------------------------------------Início da função Main----------------------------------------------------#
print("Temos que ajudar o nosso pato encontrar o caminho mais curto para chegar a em seu lago")
print("O nosso pato está no ponto (0,0) e tem que chegar no ponto (9,9)")
print("O nosso pato não pode sair do labirinto")
print("O nosso pato não pode passar por uma casa ocupada")
print("O nosso pato pode se mover para cima, baixo, esquerda ou direita")
print("Dependendo da busca, nosso pato pode não chegar na lagoa")
print("O caminho pode ser traiçoeiro, não permitindo o pato chegar no seu objetivo")

labirinto = []

while True:
    print("\nQual forma de busca você deseja fazer?")
    escolha = int(input("Busca gulosa (1) / Busca A* (2): "))
    
    labirinto = criaLabirinto()
    imprimeLabirinto(labirinto)
    
    if escolha == 1: 
        buscaGulosa(labirinto)
    elif escolha == 2:
        print("a")
        #buscaA(labirinto)#
        #IMPLEMENTAR
    else:
        print("Escolha inválida.")
        
    if int(input("Deseja jogar novamente?\n(0-Não/1-Sim): ")) == 0:
        print("Obrigado por jogar!")
        break